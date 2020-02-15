# -*- coding:utf-8 -*-
import logging

from mavic.http import Request


class Spider(object):
    name = None
    custom_settings = None

    def __init__(self, name=None, *args, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError('%s must have a name' % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, "start_urls"):
            self.start_urls = []

    @property
    def logger(self):
        logger = logging.getLogger(self.name)
        return logging.LoggerAdapter(logger, {'spider': self})

    def log(self, message, level=logging.DEBUG, **kwargs):
        self.logger.log(level, message, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def _set_crawler(self, crawler):
        self.crawler = crawler
        self.settings = crawler.settings

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(cls.custom_settings or {}, priority='spider')

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True)

    def parse(self, response):
        raise NotImplementedError

    @staticmethod
    def close(spider, reason):
        pass

    def __str__(self):
        return "<%s %r at 0x%0x>" % (type(self).__name__, self.name, id(self))

    __repr__ = __str__
