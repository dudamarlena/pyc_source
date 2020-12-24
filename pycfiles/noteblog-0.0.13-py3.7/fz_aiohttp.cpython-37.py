# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/spider/fz_aiohttp.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 6970 bytes
"""
@author = super_fazai
@File    : fz_aiohttp.py
@Time    : 2017/7/14 14:45
@connect : superonesfazai@gmail.com
"""
import re
from gc import collect
from asyncio import get_event_loop
from asyncio import wait as async_wait
from asyncio import Queue as AsyncioQueue
from aiohttp import TCPConnector, ClientSession
from ..ip_pools import IpPools, ip_proxy_pool, fz_ip_pool
from ..internet_utils import get_random_pc_ua
__all__ = [
 'MyAiohttp',
 'AioHttp']

class MyAiohttp(object):

    def __init__(self, ip_pool_type=ip_proxy_pool, max_tasks=10):
        super(MyAiohttp, self).__init__()
        self.loop = get_event_loop()
        self.max_tasks = max_tasks
        self.queue = AsyncioQueue(loop=(self.loop))
        self.ip_pool_type = ip_pool_type

    @property
    def headers(self):
        return {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 
         'Accept-Encoding:':'gzip, deflate, br', 
         'Accept-Language':'zh-CN,zh;q=0.9', 
         'Cache-Control':'max-age=0', 
         'Connection':'keep-alive', 
         'User-Agent':get_random_pc_ua()}

    @classmethod
    async def aio_get_url_body(cls, url, headers, method='get', params=None, timeout=10, num_retries=10, high_conceal=True, data=None, ip_pool_type=ip_proxy_pool, verify_ssl=True, use_dns_cache=True, proxy_auth=None, allow_redirects=True, proxy_headers=None):
        """
        异步获取url的body(简略版)
        :param url:
        :param headers:
        :param method:
        :param params:
        :param timeout:
        :param num_retries: 常规使用都设置为1次
        :param high_conceal:
        :param data: post的data
        :param ip_pool_type:
        :param verify_ssl:
        :param use_dns_cache:
        :param proxy_auth:
        :param allow_redirects:
        :param proxy_headers:
        :return:
        """
        proxy = await cls.get_proxy(ip_pool_type=ip_pool_type, high_conceal=high_conceal)
        if isinstance(proxy, bool):
            if proxy is False:
                print('异步获取代理失败! return ""!')
                return ''
        conn = TCPConnector(verify_ssl=verify_ssl,
          limit=150,
          use_dns_cache=use_dns_cache)
        async with ClientSession(connector=conn) as session:
            try:
                async with session.request(method=method,
                  url=url,
                  headers=headers,
                  params=params,
                  data=data,
                  proxy=proxy,
                  timeout=timeout,
                  proxy_auth=proxy_auth,
                  allow_redirects=allow_redirects,
                  proxy_headers=proxy_headers) as r:
                    result = await r.text(encoding=None)
                    result = await cls.wash_html(result)
                    return result
            except Exception as e:
                try:
                    if num_retries > 0:
                        return await cls.aio_get_url_body(url=url,
                          headers=headers,
                          method=method,
                          params=params,
                          timeout=timeout,
                          num_retries=(num_retries - 1),
                          high_conceal=high_conceal,
                          data=data,
                          ip_pool_type=ip_pool_type,
                          verify_ssl=verify_ssl,
                          use_dns_cache=use_dns_cache,
                          proxy_auth=proxy_auth,
                          allow_redirects=allow_redirects,
                          proxy_headers=proxy_headers)
                    print('异步获取body失败!')
                    return ''
                finally:
                    e = None
                    del e

    @classmethod
    async def wash_html(cls, body):
        """
        异步清洗html
        :param body:
        :return:
        """
        body = re.compile('\t|  ').sub('', body)
        body = re.compile('\r\n').sub('', body)
        body = re.compile('\n').sub('', body)
        body = re.compile('<ahref').sub('<a href', body)
        body = re.compile('<strongtitle').sub('<strong title', body)
        return body

    @classmethod
    async def get_proxy(cls, ip_pool_type=ip_proxy_pool, high_conceal=True):
        """
        异步获取proxy
        :return: 格式: 'http://ip:port'
        """
        loop = get_event_loop()
        ip_object = IpPools(type=ip_pool_type, high_conceal=high_conceal)
        args = []
        proxy = False
        try:
            try:
                proxy = await (loop.run_in_executor)(None, ip_object._get_random_proxy_ip, *args)
            except Exception:
                pass

        finally:
            return

        try:
            del loop
        except:
            pass

        collect()
        return proxy

    async def run(self):
        url = 'https://superonesfazai.github.io/'
        tasks = [self.loop.create_task(self.aio_get_url_body(url=url, headers=(self.headers))) for _ in range(self.max_tasks)]
        finished_job, unfinished_job = await async_wait(tasks)
        all_result = [r.result() for r in finished_job]
        return all_result

    def __del__(self):
        self.loop.close()
        collect()


class AioHttp(MyAiohttp):
    __doc__ = '改名'