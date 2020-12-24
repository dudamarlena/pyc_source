# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/davemclain/code/mmf/django-gzipping-cache/django_gzipping_cache/cache.py
# Compiled at: 2014-02-21 16:52:26
from django.core.cache import get_cache
import zlib

class GzippingCache(object):

    def __init__(self, name, params):
        super(GzippingCache, self).__init__()
        self._cache = get_cache(params.get('LOCATION'))
        self._compress_level = params.get('COMPRESS_LEVEL', 6)
        self._pass_uncompressed = params.get('PASS_UNCOMPRESSED', False)

    def gzip(self, value):
        if not value:
            return None
        else:
            return zlib.compress(value, self._compress_level)

    def ungzip(self, value):
        if not value:
            return
        else:
            try:
                return zlib.decompress(value)
            except zlib.error:
                if self._pass_uncompressed:
                    return value
                raise

            return

    def __getattr__(self, name):
        return getattr(self._cache, name)

    def add(self, key, value, *args, **kwargs):
        value = self.gzip(value)
        return self._cache.add(key, value, *args, **kwargs)

    def get(self, *args, **kwargs):
        return self.ungzip(self._cache.get(*args, **kwargs))

    def set(self, key, value, *args, **kwargs):
        value = self.gzip(value)
        return self._cache.set(key, value, *args, **kwargs)

    def get_many(self, *args, **kwargs):
        value_dict = self._cache.get_many(*args, **kwargs)
        for k, v in value_dict.items():
            value_dict[k] = self.ungzip(v)

    def set_many(self, data, *args, **kwargs):
        for k, v in data.items():
            data[k] = self.gzip(v)

        self._cache.set_many(data, *args, **kwargs)