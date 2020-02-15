# -*- coding:utf-8 -*-
import asyncio
import logging
from time import time

from mavic.core.scraper import Scraper
from mavic.http import Request
from mavic.log import logformatter_adapter
from mavic.utils.misc import load_object

logger = logging.getLogger(__name__)


class CallLaterOnce(object):

    def __init__(self, func, loop=None, *args, **kwargs):
        self._func = func
        self.args = args
        self.kwargs = kwargs
        self.canced = False
        self.loop = loop

    async def schedule(self):
        if not self.canced:
            await self._func(*self.args, **self.kwargs)

    def cancel(self):
        self.canced = True


class Slot(object):
    def __init__(self, start_requests, close_if_idle, nextcall, scheduler):
        self.closing = False
        self.inprogress = set()
        self.start_requests = iter(start_requests)
        self.close_if_idle = close_if_idle
        self.nextcall = nextcall
        self.scheduler = scheduler

    def add_request(self, request):
        self.inprogress.add(request)

    def remove_request(self, request):
        self.inprogress.remove(request)

    async def close(self):
        self.closing = True
        if self.closing:
            if self.nextcall:
                self.nextcall.cancel()


class Engine(object):

    def __init__(self, crawler, loop=None):
        self.settings = crawler.settings
        self.crawler = crawler
        self.logformatter = crawler.logformatter
        self.loop = loop
        self.slot = None
        self.spider = None
        self.running = False
        self.paused = False
        self.scheduler_cls = load_object(self.settings['SCHEDULER'])
        self.downloader_cls = load_object(self.settings['DOWNLOADER'])
        self.downloader = self.downloader_cls.from_crawler(crawler)
        self.scraper = Scraper(crawler)

    def _loader_spider(self):
        self.spider = self.crawler.spider

    async def open_spider(self, spider, start_requests=(), close_if_idle=True):
        logger.info('spider opened', extra={'spider': spider})
        nextcall = CallLaterOnce(self._next_request, self.loop, spider)
        scheduler = self.scheduler_cls.from_crawler(self.crawler)
        slot = Slot(start_requests, close_if_idle, nextcall, scheduler)
        self.slot = slot
        self.spider = spider
        await scheduler.open_spider(spider)

    async def start(self):
        logger.debug("engine start")
        self.start_time = time()
        self.running = True
        routines = [self.slot.nextcall.schedule()]
        await asyncio.gather(*routines)

    async def stop(self):
        assert self.running, 'Engine not running'
        self.running = False
        await self._close_all_spiders()

    async def close(self):
        if self.running:
            await self.stop()
        elif self.open_spiders:
            await self._close_all_spiders()
        else:
            self.downloader.close()

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    @property
    def open_spiders(self):
        return [self.spider] if self.spider else []

    async def _close_all_spiders(self):
        pass

    async def _next_request(self, spider):
        slot = self.slot

        request = await slot.scheduler.next_request()
        if request:
            response = await self.download(request, spider)
            logkws = self.logformatter.crawled(request, response, spider)
            if logkws is not None:
                logger.log(*logformatter_adapter(logkws), extra={'spider': spider})
            await self._handle_downloader_output(response, request, spider)
        try:
            request = next(slot.start_requests)
        except StopIteration:
            slot.start_requests = None
        except Exception:
            pass
        else:
            await self.crawl(request, spider)

        if self.spider_is_idle(spider):
            await self._spider_idle(spider)

        await slot.nextcall.schedule()

    async def crawl(self, request, spider):
        await self.slot.scheduler.enqueue_request(request)

    async def download(self, request, spider):
        task = asyncio.create_task(self.downloader.fetch(request, spider))
        return await task

    async def _handle_downloader_output(self, response, request, spider):
        if isinstance(response, Request):
            await self.crawl(request, spider)
            return
        await self.scraper.enqueue_scrape(response, request, spider)

    def spider_is_idle(self, spider):
        if self.downloader.active:
            return False
        if self.slot.scheduler.has_pending_requests():
            return False
        return True

    async def _spider_idle(self, spider):
        if self.spider_is_idle(spider):
            await self.close_spider(spider, reason='finished')

    async def close_spider(self, spider, reason='cancelled'):
        slot = self.slot
        if slot.closing:
            return

        logger.info("Closing spider (%(reason)s)",
                    {'reason': reason},
                    extra={'spider': spider})

        await slot.close()
        await self.downloader.close()
        await self.scraper.close_spider(spider)
        await slot.scheduler.close(reason)
