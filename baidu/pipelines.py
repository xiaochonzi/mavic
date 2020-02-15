# -*- coding:utf-8 -*-


class DefaultPipelines(object):
    name = 'default pipeline'

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    async def open_spider(self, spider):
        pass

    async def close_spider(self, spider):
        pass

    async def process_item(self, item, spider):
        print(self.name, 'process_item', item)
