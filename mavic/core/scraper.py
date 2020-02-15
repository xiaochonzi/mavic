# -*- coding:utf-8 -*-
import asyncio

from mavic.http import Request
from mavic.item import BaseItem
from mavic.utils.misc import load_object
from mavic.utils.python import get_result_list


class Scraper(object):

    def __init__(self, crawler):
        self.crawler = crawler
        itemproc_cls = load_object(crawler.settings['ITEM_PROCESSOR'])
        self.itemproc = itemproc_cls.from_crawler(crawler)
        self.concurrent_items = crawler.settings.getint('CONCURRENT_ITEMS')

    async def open_spider(self, spider):
        await self.itemproc.open_spider(spider)

    async def close_spider(self, spider):
        await self.itemproc.close_spider(spider)

    async def enqueue_scrape(self, response, request, spider):
        callback = request.callback or spider.parse
        result = callback(response)
        if asyncio.iscoroutine(result):
            task = asyncio.create_task(result)
            result = await task
        ret = get_result_list(result)
        await self.handle_spider_output(ret, request, response, spider)

    async def handle_spider_output(self, result, request, response, spider):

        for each in result:
            if each is None:
                continue
            elif isinstance(each, Request):
                await self.crawler.engine.crawl(request, spider)
            elif isinstance(each, ((BaseItem, dict))):
                await self.itemproc.process_item(each, spider)
            else:
                pass
