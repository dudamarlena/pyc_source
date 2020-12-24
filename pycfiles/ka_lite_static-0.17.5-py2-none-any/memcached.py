# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/cache/backends/memcached.py
# Compiled at: 2018-07-11 18:15:30
"""Memcached cache backend"""
import time
from threading import local
from django.core.cache.backends.base import BaseCache, InvalidCacheBackendError
from django.utils import six
from django.utils.encoding import force_str

class BaseMemcachedCache(BaseCache):

    def __init__(self, server, params, library, value_not_found_exception):
        super(BaseMemcachedCache, self).__init__(params)
        if isinstance(server, six.string_types):
            self._servers = server.split(';')
        else:
            self._servers = server
        self.LibraryValueNotFoundException = value_not_found_exception
        self._lib = library
        self._options = params.get('OPTIONS', None)
        return

    @property
    def _cache(self):
        """
        Implements transparent thread-safe access to a memcached client.
        """
        if getattr(self, '_client', None) is None:
            self._client = self._lib.Client(self._servers)
        return self._client

    def _get_memcache_timeout(self, timeout):
        """
        Memcached deals with long (> 30 days) timeouts in a special
        way. Call this function to obtain a safe value for your timeout.
        """
        timeout = timeout or self.default_timeout
        if timeout > 2592000:
            timeout += int(time.time())
        return int(timeout)

    def make_key(self, key, version=None):
        return force_str(super(BaseMemcachedCache, self).make_key(key, version))

    def add(self, key, value, timeout=0, version=None):
        key = self.make_key(key, version=version)
        return self._cache.add(key, value, self._get_memcache_timeout(timeout))

    def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        val = self._cache.get(key)
        if val is None:
            return default
        else:
            return val

    def set(self, key, value, timeout=0, version=None):
        key = self.make_key(key, version=version)
        self._cache.set(key, value, self._get_memcache_timeout(timeout))

    def delete(self, key, version=None):
        key = self.make_key(key, version=version)
        self._cache.delete(key)

    def get_many(self, keys, version=None):
        new_keys = [ self.make_key(x, version=version) for x in keys ]
        ret = self._cache.get_multi(new_keys)
        if ret:
            _ = {}
            m = dict(zip(new_keys, keys))
            for k, v in ret.items():
                _[m[k]] = v

            ret = _
        return ret

    def close(self, **kwargs):
        self._cache.disconnect_all()

    def incr(self, key, delta=1, version=None):
        key = self.make_key(key, version=version)
        if delta < 0:
            return self._cache.decr(key, -delta)
        else:
            try:
                val = self._cache.incr(key, delta)
            except self.LibraryValueNotFoundException:
                val = None

            if val is None:
                raise ValueError("Key '%s' not found" % key)
            return val

    def decr(self, key, delta=1, version=None):
        key = self.make_key(key, version=version)
        if delta < 0:
            return self._cache.incr(key, -delta)
        else:
            try:
                val = self._cache.decr(key, delta)
            except self.LibraryValueNotFoundException:
                val = None

            if val is None:
                raise ValueError("Key '%s' not found" % key)
            return val

    def set_many(self, data, timeout=0, version=None):
        safe_data = {}
        for key, value in data.items():
            key = self.make_key(key, version=version)
            safe_data[key] = value

        self._cache.set_multi(safe_data, self._get_memcache_timeout(timeout))

    def delete_many(self, keys, version=None):
        l = lambda x: self.make_key(x, version=version)
        self._cache.delete_multi(map(l, keys))

    def clear(self):
        self._cache.flush_all()


class CacheClass(BaseMemcachedCache):

    def __init__(self, server, params):
        import warnings
        warnings.warn('memcached.CacheClass has been split into memcached.MemcachedCache and memcached.PyLibMCCache. Please update your cache backend setting.', DeprecationWarning)
        try:
            import memcache
        except ImportError:
            raise InvalidCacheBackendError("Memcached cache backend requires either the 'memcache' or 'cmemcache' library")

        super(CacheClass, self).__init__(server, params, library=memcache, value_not_found_exception=ValueError)


class MemcachedCache(BaseMemcachedCache):
    """An implementation of a cache binding using python-memcached"""

    def __init__(self, server, params):
        import memcache
        super(MemcachedCache, self).__init__(server, params, library=memcache, value_not_found_exception=ValueError)


class PyLibMCCache(BaseMemcachedCache):
    """An implementation of a cache binding using pylibmc"""

    def __init__(self, server, params):
        import pylibmc
        self._local = local()
        super(PyLibMCCache, self).__init__(server, params, library=pylibmc, value_not_found_exception=pylibmc.NotFound)

    @property
    def _cache(self):
        client = getattr(self._local, 'client', None)
        if client:
            return client
        else:
            client = self._lib.Client(self._servers)
            if self._options:
                client.behaviors = self._options
            self._local.client = client
            return client