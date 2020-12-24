# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/parente/projects/nbviewer/nbviewer/providers/url/client.py
# Compiled at: 2016-10-24 14:40:21
# Size of source mod 2**32: 5538 bytes
"""Async HTTP client with bonus features!

- Support caching via upstream 304 with ETag, Last-Modified
- Log request timings for profiling
"""
import hashlib, pickle, time
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from tornado.log import app_log
from tornado import gen
from nbviewer.utils import time_block
cache_headers = {'ETag': 'If-None-Match', 
 'Last-Modified': 'If-Modified-Since'}

class NBViewerAsyncHTTPClient(object):
    __doc__ = 'Subclass of AsyncHTTPClient with bonus logging and caching!\n    \n    If upstream servers support 304 cache replies with the following headers:\n    \n    - ETag : If-None-Match\n    - Last-Modified : If-Modified-Since\n    \n    Upstream requests are still made every time,\n    but resources and rate limits may be saved by 304 responses.\n    \n    Currently, responses are cached for a non-configurable two hours.\n    '
    cache = None
    expiry = 7200

    def fetch_impl(self, request, callback):
        self.io_loop.add_callback(lambda : self._fetch_impl(request, callback))

    @gen.coroutine
    def _fetch_impl(self, request, callback):
        tic = time.time()
        if request.user_agent is None:
            request.user_agent = 'Tornado-Async-Client'
        name = request.url.split('?')[0]
        cached_response = None
        app_log.debug('Fetching %s', name)
        cache_key = hashlib.sha256(request.url.encode('utf8')).hexdigest()
        with time_block('Upstream cache get %s' % name):
            cached_response = yield self._get_cached_response(cache_key, name)
        if cached_response:
            app_log.debug('Upstream cache hit %s', name)
            for resp_key, req_key in cache_headers.items():
                value = cached_response.headers.get(resp_key)
                if value:
                    request.headers[req_key] = value

        else:
            app_log.debug('Upstream cache miss %s', name)
        response = yield gen.Task(super(NBViewerAsyncHTTPClient, self).fetch_impl, request)
        dt = time.time() - tic
        log = app_log.info if dt > 1 else app_log.debug
        if response.code == 304 and cached_response:
            log('Upstream 304 on %s in %.2f ms', name, 1000.0 * dt)
            response = self._update_cached_response(response, cached_response)
            callback(response)
        else:
            if not response.error:
                log('Fetched  %s in %.2f ms', name, 1000.0 * dt)
            callback(response)
        if not response.error:
            yield self._cache_response(cache_key, name, response)

    def _update_cached_response(self, three_o_four, cached_response):
        """Apply any changes to the cached response from the 304

        Return the HTTPResponse to be used.

        Currently this hardcodes more recent GitHub rate limit headers,
        and that's it.
        Is there a better way for this to be in the right place?

        """
        for key, value in three_o_four.headers.items():
            if key.lower().startswith('x-ratelimit-'):
                cached_response.headers[key] = value

        return cached_response

    @gen.coroutine
    def _get_cached_response(self, cache_key, name):
        """Get the cached response, if any"""
        if not self.cache:
            return
            try:
                cached_pickle = yield self.cache.get(cache_key)
                if cached_pickle:
                    raise gen.Return(pickle.loads(cached_pickle))
            except gen.Return:
                raise
            except Exception:
                app_log.error('Upstream cache get failed %s', name, exc_info=True)

    @gen.coroutine
    def _cache_response(self, cache_key, name, response):
        """Cache the response, if any cache headers we understand are present."""
        if not self.cache:
            return
        if not any(response.headers.get(key) for key in cache_headers):
            return
        with time_block('Upstream cache set %s' % name):
            try:
                pickle_response = pickle.dumps(response, pickle.HIGHEST_PROTOCOL)
                yield self.cache.set(cache_key, pickle_response, int(time.time() + self.expiry))
            except Exception:
                app_log.error('Upstream cache failed %s' % name, exc_info=True)


class NBViewerSimpleAsyncHTTPClient(NBViewerAsyncHTTPClient, SimpleAsyncHTTPClient):
    pass


try:
    from tornado.curl_httpclient import CurlAsyncHTTPClient
except ImportError:
    pass
else:

    class NBViewerCurlAsyncHTTPClient(NBViewerAsyncHTTPClient, CurlAsyncHTTPClient):
        pass