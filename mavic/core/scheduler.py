# -*- coding:utf-8 -*-

from mavic.utils.misc import load_object, create_instance


class Scheduler(object):

    def __init__(self, dupefilter, pqclass=None):
        self.df = dupefilter
        self.queue = pqclass()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dupefilter_cls = load_object(settings['DUPEFILTER_CLASS'])
        dupefilter = create_instance(dupefilter_cls, settings, crawler)
        pqclass = load_object(settings['SCHEDULER_PRIORITY_QUEUE'])
        return cls(dupefilter, pqclass)

    async def open_spider(self, spider):
        self.df.open(spider)

    async def enqueue_request(self, request):
        if not request.dont_filter and not await self.df.request_seen(request):
            await self.queue.put(request)

    async def next_request(self):
        if self.queue.empty():
            return None
        return await self.queue.get()

    def __len__(self):
        return self.queue.qsize()

    def has_pending_requests(self):
        return len(self) > 0

    async def close(self, reason):
        self.df.close(reason)
