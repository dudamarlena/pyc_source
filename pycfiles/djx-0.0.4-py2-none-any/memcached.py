# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/cache/backends/memcached.py
# Compiled at: 2019-02-14 00:35:17
"""Memcached cache backend"""
import pickle, re, time, warnings
from django.core.cache.backends.base import DEFAULT_TIMEOUT, BaseCache
from django.utils import six
from django.utils.deprecation import RemovedInDjango21Warning
from django.utils.encoding import force_str
from django.utils.functional import cached_property

class BaseMemcachedCache(BaseCache):

    def __init__(self, server, params, library, value_not_found_exception):
        super(BaseMemcachedCache, self).__init__(params)
        if isinstance(server, six.string_types):
            self._servers = re.split('[;,]', server)
        else:
            self._servers = server
        self.LibraryValueNotFoundException = value_not_found_exception
        self._lib = library
        self._options = params.get('OPTIONS') or {}

    @property
    def _cache(self):
        """
        Implements transparent thread-safe access to a memcached client.
        """
        if getattr(self, '_client', None) is None:
            self._client = self._lib.Client(self._servers, **self._options)
        return self._client

    def get_backend_timeout(self, timeout=DEFAULT_TIMEOUT):
        """
        Memcached deals with long (> 30 days) timeouts in a special
        way. Call this function to obtain a safe value for your timeout.
        """
        if timeout == DEFAULT_TIMEOUT:
            timeout = self.default_timeout
        if timeout is None:
            return 0
        else:
            if int(timeout) == 0:
                timeout = -1
            if timeout > 2592000:
                timeout += int(time.time())
            return int(timeout)

    def make_key(self, key, version=None):
        return force_str(super(BaseMemcachedCache, self).make_key(key, version))

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_key(key, version=version)
        return self._cache.add(key, value, self.get_backend_timeout(timeout))

    def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        val = self._cache.get(key)
        if val is None:
            return default
        else:
            return val

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_key(key, version=version)
        if not self._cache.set(key, value, self.get_backend_timeout(timeout)):
            self._cache.delete(key)

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

    def set_many(self, data, timeout=DEFAULT_TIMEOUT, version=None):
        safe_data = {}
        for key, value in data.items():
            key = self.make_key(key, version=version)
            safe_data[key] = value

        self._cache.set_multi(safe_data, self.get_backend_timeout(timeout))

    def delete_many(self, keys, version=None):
        self._cache.delete_multi(self.make_key(key, version=version) for key in keys)

    def clear(self):
        self._cache.flush_all()


class MemcachedCache(BaseMemcachedCache):
    """An implementation of a cache binding using python-memcached"""

    def __init__(self, server, params):
        import memcache
        super(MemcachedCache, self).__init__(server, params, library=memcache, value_not_found_exception=ValueError)

    @property
    def _cache(self):
        if getattr(self, '_client', None) is None:
            client_kwargs = dict(pickleProtocol=pickle.HIGHEST_PROTOCOL)
            client_kwargs.update(self._options)
            self._client = self._lib.Client(self._servers, **client_kwargs)
        return self._client


class PyLibMCCache(BaseMemcachedCache):
    """An implementation of a cache binding using pylibmc"""

    def __init__(self, server, params):
        import pylibmc
        super(PyLibMCCache, self).__init__(server, params, library=pylibmc, value_not_found_exception=pylibmc.NotFound)
        legacy_behaviors = {}
        for option in list(self._options):
            if option not in ('behaviors', 'binary', 'username', 'password'):
                warnings.warn('Specifying pylibmc cache behaviors as a top-level property within `OPTIONS` is deprecated. Move `%s` into a dict named `behaviors` inside `OPTIONS` instead.' % option, RemovedInDjango21Warning, stacklevel=2)
                legacy_behaviors[option] = self._options.pop(option)

        if legacy_behaviors:
            self._options.setdefault('behaviors', {}).update(legacy_behaviors)

    @cached_property
    def _cache(self):
        return self._lib.Client(self._servers, **self._options)

    def close(self, **kwargs):
        pass