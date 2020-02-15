# -*- coding:utf-8 -*-
from itertools import chain

from mavic.core.middleware import MiddlewareManager
from mavic.utils.conf import build_component_list


def _isiterable(possible_iterator):
    return hasattr(possible_iterator, '__iter__')


class SpiderMiddlewareManager(MiddlewareManager):
    component_name = 'spider middleware'

    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        return build_component_list(settings.getwithbase('SPIDER_MIDDLEWARES'))

    def _add_middleware(self, mw):
        super(SpiderMiddlewareManager, self)._add_middleware(mw)
        if hasattr(mw, 'process_spider_input'):
            self.methods['process_spider_input'].append(mw.process_spider_input)
        if hasattr(mw, 'process_start_requests'):
            self.methods['process_start_requests'].appendleft(mw.process_start_requests)
        self.methods['process_spider_output'].appendleft(getattr(mw, 'process_spider_output', None))
        self.methods['process_spider_exception'].appendleft(getattr(mw, 'process_spider_exception', None))

    def scrape_response(self, scrape_func, response, request, spider):
        fname = lambda f: '%s.%s' % (
            f.__self__.__class__.__name__,
            f.__func__.__name__)

        def process_spider_input(response):
            return scrape_func(response, request, spider)

        def process_spider_exception(_failure, start_index=0):
            return _failure

        def process_spider_output(result, start_index=0):
            # items in this iterable do not need to go through the process_spider_output
            # chain, they went through it already from the process_spider_exception method
            return chain(result, None)

        return

    async def process_start_requests(self, start_requests, spider):
        return await self._process_chain('process_start_requests', start_requests, spider)
