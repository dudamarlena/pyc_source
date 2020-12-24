# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/cached_request.py
# Compiled at: 2019-12-26 16:17:44
# Size of source mod 2**32: 5737 bytes
__doc__ = '\nA auto compressed disk cache backed requests maker.\n'
import typing, requests
from diskcache import Cache
from .decode import decoder

class CachedRequest(object):
    """CachedRequest"""

    def __init__(self, cache: Cache, log_cache_miss: bool=False, expire: int=86400):
        """
        :type cache: Cache
        :param cache:

        :type log_cache_miss: bool
        :param log_cache_miss: default False

        :type expire: int
        :param expire: default expire time for cache
        """
        if not isinstance(cache, Cache):
            raise TypeError
        self.cache = cache
        self.log_cache_miss = log_cache_miss
        self.expire = expire
        self.use_which = 'requests'
        self.get_html_method = self.get_html_method_for_requests
        self.use_requests()

    def use_requests(self):
        self.use_which = 'requests'
        self.get_html_method = self.get_html_method_for_requests

    def get_html_method_for_requests(self, response: requests.Response, encoding: str=None, errors: str='strict', **kwargs) -> str:
        """
        Get html from ``requests.Response`` object.

        :param response: the return of ``requests.request(method, url, **kwargs)``
        :param encoding: manually specify the encoding.
        :param errors: errors handle method.
        :return: html
        """
        return decoder.decode(binary=(response.content),
          url=(response.url),
          encoding=encoding,
          errors=errors)

    def get_binary_method_for_requests(self, response: requests.Response, **kwargs) -> bytes:
        """
        Get binary data from ``requests.Response`` object.

        :param response:
        :param kwargs:
        :return: binary data
        """
        return response.content

    def request_for_html(self, url: str, get_html_method: typing.Callable=None, get_html_method_kwargs: dict=None, request_method: typing.Callable=None, request_kwargs: dict=None, cache_expire: int=None, cacheable_callback: typing.Callable=lambda html: True) -> str:
        """

        :param url:
        :param get_html_method: a callable method takes requests.Response as
            first argument, returns html.
        :param get_html_method_kwargs:
        :param request_method: requests.get or requests.post
        :param request_kwargs:
        :param cacheable_callback: a method takes html as single argument,
            if returns True, then update cache. otherwise do nothing.

        **中文文档**

        使用 ``requests.request()`` 执行 HTTP request, 返回 HTML.
        永远优先尝试使用缓存. 如果缓存未命中, 则执行 HTTP request. 并用
        cacheable_callback 检查 html, 如果返回 True, 则更新缓存. 如果返回 False
        则不更新缓存.
        """
        if get_html_method is None:
            get_html_method = self.get_html_method
        elif get_html_method_kwargs is None:
            get_html_method_kwargs = dict()
        else:
            if request_method is None:
                request_method = requests.get
            else:
                if request_kwargs is None:
                    request_kwargs = dict()
                if cache_expire is None:
                    cache_expire = self.expire
            if self.use_which == 'requests':
                if 'url' not in request_kwargs:
                    request_kwargs['url'] = url
        if url in self.cache:
            return self.cache[url]
        else:
            if self.log_cache_miss:
                msg = "{} doesn't hit cache!".format(url)
                print(msg)
            response = request_method(**request_kwargs)
            html = get_html_method(response, **get_html_method_kwargs)
            if cacheable_callback(html):
                self.cache.set(url, html, cache_expire)
            return html