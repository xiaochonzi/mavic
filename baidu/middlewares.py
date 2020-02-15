# -*- coding:utf-8 -*-


class DefaultDownloadMiddle(object):
    name = 'default download middle'

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    async def process_request(self, request, spider):
        return request

    async def process_response(self, request, response, spider):
        return response


class SecondDownloadMiddle(object):
    name = 'second download'

    async def process_request(self, request, spider):
        return request

    async def process_response(self, request, response, spider):
        return response
