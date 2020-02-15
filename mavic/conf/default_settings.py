# -*- coding:utf-8 -*-
from importlib import import_module

BOT_NAME = 'mavicbot'

CONCURRENT_ITEMS = 100

CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 9

COOKIES_ENABLED = True
COOKIES_DEBUG = False

DEFAULT_ITEM_CLASS = 'mavic.item.Item'

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

DNSCACHE_ENABLED = True
DNS_TIMEOUT = 60

DOWNLOADER_MIDDLEWARES = {}

DOWNLOADER_MIDDLEWARES_BASE = {

}

DOWNLOAD_TIMEOUT = 180

DOWNLOADER = 'mavic.core.downloader.Downloader'

DUPEFILTER_CLASS = 'mavic.dupefilters.RFPDupeFilter'

ITEM_PROCESSOR = 'mavic.pipelines.ItemPipelineManager'

ITEM_PIPELINES = {}
ITEM_PIPELINES_BASE = {}

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FORMATTER = 'mavic.logformatter.LogFormatter'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
LOG_STDOUT = False
LOG_LEVEL = 'DEBUG'
LOG_FILE = None
LOG_SHORT_NAMES = False

RANDOMIZE_DOWNLOAD_DELAY = 20

REDIRECT_ENABLED = True
REDIRECT_MAX_TIMES = 20  # uses Firefox default setting
REDIRECT_PRIORITY_ADJUST = +2

RETRY_ENABLED = True
RETRY_TIMES = 2  # initial response + 2 retries = 3 requests
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]
RETRY_PRIORITY_ADJUST = -1

SCHEDULER = 'mavic.core.scheduler.Scheduler'
SCHEDULER_PRIORITY_QUEUE = 'asyncio.queues.PriorityQueue'

USER_AGENT = 'Scrapy/%s (+https://scrapy.org)' % import_module('scrapy').__version__
