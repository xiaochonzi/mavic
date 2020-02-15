# -*- coding:utf-8 -*-
"""
use aiohttp wrap download handler
"""
import aiohttp
from aiohttp.client import ClientTimeout

from mavic.http import Response


class DownloadHandler(object):

    def __init__(self, crawler):
        self.settings = crawler.settings
        self.loop = crawler.loop
        self.timeout = self.settings.getint('DOWNLOAD_TIMEOUT')
        self.conn = self._create_connector(self.settings)

    def _create_connector(self, settings):
        limit = settings.getint('CONCURRENT_REQUESTS')
        use_dns_cache = settings.getbool('DNSCACHE_ENABLED')
        ttl_dns_cache = settings.getint('DNS_TIMEOUT')
        conn = aiohttp.TCPConnector(limit=limit, use_dns_cache=use_dns_cache, ttl_dns_cache=ttl_dns_cache,
                                    force_close=True, loop=self.loop)
        return conn

    async def fetch(self, request):
        proxy = request.meta.get("proxy")
        download_timeout = request.meta.get('download_timeout') or self.timeout
        timeout = ClientTimeout(total=download_timeout)
        async with aiohttp.request(method=request.method,
                                   url=request.url,
                                   params=request.params,
                                   data=request.data,
                                   headers=request.headers,
                                   json=request.json,
                                   timeout=timeout, proxy=proxy, connector=self.conn, loop=self.loop) as resp:
            body = await resp.read()
            headers = resp.headers
            response = Response(request.url, status=resp.status, headers=headers, body=body, request=request)
            return response

    async def close(self):
        await self.conn.close()
