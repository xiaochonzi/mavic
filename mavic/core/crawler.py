# -*- coding:utf-8 -*-
import asyncio
import logging
import traceback

from mavic.conf.settings import Settings
from mavic.core.engine import Engine
from mavic.log import (get_mavic_root_handler,
                       install_mavic_root_handler,
                       configure_logging)
from mavic.spiders import Spider
from mavic.utils.misc import load_object

logger = logging.getLogger(__name__)


class Crawler(object):

    def __init__(self, spidercls, settings=None, loop=None, *args, **kwargs):
        if isinstance(spidercls, Spider):
            raise ValueError("the spidercls argument must be a class, not an object")

        if isinstance(settings, dict) or settings is None:
            settings = Settings()

        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop

        self.spidercls = spidercls
        self.settings = settings.copy()
        self.spidercls.update_settings(self.settings)

        self.crawling = False
        self.spider = None
        self.engine = None

        configure_logging(self.settings, True)

        lf_cls = load_object(self.settings['LOG_FORMATTER'])
        self.logformatter = lf_cls.from_crawler(self)

        self.settings.freeze()

    def _create_spider(self, *args, **kwargs):
        return self.spidercls.from_crawler(self, *args, **kwargs)

    def _create_engine(self):
        return Engine(self, self.loop)

    async def crawl(self, *args, **kwargs):
        try:
            self.spider = self._create_spider(*args, **kwargs)
            self.engine = self._create_engine()
            start_requests = iter(self.spider.start_requests())
            await self.engine.open_spider(self.spider, start_requests)
        except Exception as e:
            traceback.print_exc()

    async def start(self):
        self.crawling = True
        task = asyncio.create_task(self.engine.start())
        await task

    async def stop(self):
        self.crawling = False
        await self.engine.stop()

    async def finish(self, feture):
        pass
