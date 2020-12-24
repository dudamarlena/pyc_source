# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/client/url_cache.py
# Compiled at: 2020-03-25 13:10:41
import os, pickle, time
_KEEPTIME = 300

class CacheItem(object):

    def __init__(self, etag, content, cached_at):
        self.etag = etag
        self.content = content
        self.cached_at = cached_at


class URLCache(object):
    """
        URLCache is a simple pickle cache, intended to be used as an HTTP
        response cache.
    """

    def __init__(self, path=None):
        """
            Initialize a URLCache, loading entries from @path, if provided.
        """
        self._path = path
        self._cache = {}
        if os.path.isfile(self._path):
            with open(self._path, 'r+b') as (f):
                try:
                    self._cache = pickle.load(f)
                except EOFError:
                    self._cache = {}

        if not os.path.exists(os.path.dirname(self._path)):
            os.makedirs(os.path.dirname(self._path))

    def get(self, url):
        try:
            item = self._cache[url]
            if item.cached_at + _KEEPTIME <= time.time():
                del self._cache
                del url
                return
            return self._cache[url]
        except KeyError:
            return

        return

    def set(self, url, etag, content):
        self._cache[url] = CacheItem(etag, content, time.time())

    def save(self):
        with open(self._path, 'w+b') as (f):
            pickle.dump(self._cache, f)