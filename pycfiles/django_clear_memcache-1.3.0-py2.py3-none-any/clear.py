# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/enrico/pyenv/titschendorf.de/django_clear_memcache/clear.py
# Compiled at: 2017-04-17 06:23:28
from django_clear_memcache.utility import MemcachedUtility
from django.conf import settings
from django.core.cache import cache, DEFAULT_CACHE_ALIAS
from django.core.exceptions import ImproperlyConfigured
from django.utils import six

class ClearMemcacheNoCacheFoundError(ImproperlyConfigured):
    pass


class ClearMemcacheController(object):

    def __init__(self):
        self._servers = None
        self._host = None
        self._port = None
        self._cache_key_prefix = None
        self._keys = None
        self._init()
        return

    def _init(self):
        cache_ = getattr(cache, 'cache', cache)
        if not hasattr(cache_, '_lib'):
            raise ClearMemcacheNoCacheFoundError('Unknown memcached backend or no memcached backend found')
        self._cache_key_prefix = cache.key_prefix
        server = settings.CACHES[DEFAULT_CACHE_ALIAS]['LOCATION']
        if isinstance(server, six.string_types):
            servers = server.split(';')
        else:
            servers = server
        self._servers = list()
        for server in servers:
            host, port = server.split(':')
            port = self._parse_port(port)
            if self._host == 'unix':
                continue
            self._servers.append((host, port))

    def _parse_port(self, port):
        try:
            return int(port)
        except (ValueError, TypeError) as e:
            raise ClearMemcacheNoCacheFoundError('Unable to parse port "%s": %e' % (port, e))

    def keys(self, use_prefix=True, refresh=False):
        if self._keys is None or refresh:
            self._keys = list()
            for self._host, self._port in self._servers:
                try:
                    utility = MemcachedUtility(self._host, self._port)
                    utility.open()
                    server_keys = list(utility.keys())
                    self._keys.extend(server_keys)
                finally:
                    utility.close()

        if use_prefix:
            keys = self._keys[:]
            for key in self._keys:
                if not key.startswith(self._cache_key_prefix):
                    keys.remove(key)

        else:
            keys = self._keys
        return keys

    def clear_cache(self, use_prefix=True):
        if use_prefix:
            for self._host, self._port in self._servers:
                self._clear()

        else:
            for self._host, self._port in self._servers:
                self._flush()

    def _clear(self):
        utility = MemcachedUtility(self._host, self._port)
        utility.open()
        try:
            for key in list(utility.keys()):
                key = key.strip()
                if key.startswith(self._cache_key_prefix):
                    utility.delete(key)

        finally:
            utility.close()

    def _flush(self):
        utility = MemcachedUtility(self._host, self._port)
        utility.open()
        try:
            utility.flush()
            for key in list(utility.keys()):
                utility.get(key)

        finally:
            utility.close()