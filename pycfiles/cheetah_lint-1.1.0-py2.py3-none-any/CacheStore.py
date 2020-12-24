# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/CacheStore.py
# Compiled at: 2019-09-22 10:12:27
__doc__ = "\nProvides several CacheStore backends for Cheetah's caching framework.  The\nmethods provided by these classes have the same semantics as those in the\npython-memcached API, except for their return values:\n\nset(key, val, time=0)\n  set the value unconditionally\nadd(key, val, time=0)\n  set only if the server doesn't already have this key\nreplace(key, val, time=0)\n  set only if the server already have this key\nget(key, val)\n  returns val or raises a KeyError\ndelete(key)\n  deletes or raises a KeyError\n"
import time

class Error(Exception):
    pass


class AbstractCacheStore(object):

    def set(self, key, val, time=None):
        raise NotImplementedError

    def add(self, key, val, time=None):
        raise NotImplementedError

    def replace(self, key, val, time=None):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError


class MemoryCacheStore(AbstractCacheStore):

    def __init__(self):
        self._data = {}

    def set(self, key, val, time=0):
        self._data[key] = (val, time)

    def add(self, key, val, time=0):
        if key in self._data:
            raise Error('a value for key %r is already in the cache' % key)
        self._data[key] = (
         val, time)

    def replace(self, key, val, time=0):
        if key in self._data:
            raise Error('a value for key %r is already in the cache' % key)
        self._data[key] = (
         val, time)

    def delete(self, key):
        del self._data[key]

    def get(self, key):
        val, exptime = self._data[key]
        if exptime and time.time() > exptime:
            del self._data[key]
            raise KeyError(key)
        else:
            return val

    def clear(self):
        self._data.clear()


class MemcachedCacheStore(AbstractCacheStore):
    servers = '127.0.0.1:11211'

    def __init__(self, servers=None, debug=False):
        if servers is None:
            servers = self.servers
        from memcache import Client as MemcachedClient
        self._client = MemcachedClient(servers, debug)
        return

    def set(self, key, val, time=0):
        self._client.set(key, val, time)

    def add(self, key, val, time=0):
        res = self._client.add(key, val, time)
        if not res:
            raise Error('a value for key %r is already in the cache' % key)
        self._data[key] = (
         val, time)

    def replace(self, key, val, time=0):
        res = self._client.replace(key, val, time)
        if not res:
            raise Error('a value for key %r is already in the cache' % key)
        self._data[key] = (
         val, time)

    def delete(self, key):
        res = self._client.delete(key, time=0)
        if not res:
            raise KeyError(key)

    def get(self, key):
        val = self._client.get(key)
        if val is None:
            raise KeyError(key)
        else:
            return val
        return

    def clear(self):
        self._client.flush_all()