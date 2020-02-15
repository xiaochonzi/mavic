# -*- coding:utf-8 -*-
import asyncio

from baidu import settings
from mavic.conf.settings import Settings
from mavic.core.crawler import Crawler
from mavic.http.request import Request
from mavic.spiders import Spider


class BaiduSpider(Spider):
    name = 'baidu'

    async def parse(self, response):
        print(response.url)

    def start_requests(self):
        for i in range(9):
            yield Request(url='https://baidu.com?_=%d' % (i,), callback=self.parse_content)

    def parse_content(self, response):
        return {'url': response.url}


loop = asyncio.get_event_loop()
s = Settings()
s.setmodule(settings)
crawler = Crawler(BaiduSpider, s, loop)


async def start():
    await crawler.crawl()
    await crawler.start()


loop.run_until_complete(start())
loop.close()
