# -*- coding:utf-8 -*-


ITEM_PIPELINES = {
    "baidu.pipelines.DefaultPipelines": 300
}

DOWNLOADER_MIDDLEWARES = {
    'baidu.middlewares.SecondDownloadMiddle': 544,
    'baidu.middlewares.DefaultDownloadMiddle': 543,
}
