# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/cache/memorycache.py
# Compiled at: 2017-01-15 13:25:40
from __future__ import unicode_literals
from __future__ import print_function
from ..cache import Cache
from collections import OrderedDict, namedtuple
from time import time as get_time
import logging
log = logging.getLogger(b'moya.runtime')
CacheEntry = namedtuple(b'CacheEntry', b'value,expire_time')

class MemoryCache(Cache):
    """Caches in a memcached server"""
    cache_backend_name = b'memory'

    def __init__(self, name, namespace, compress=True, compress_min=1024, size=1048576):
        super(MemoryCache, self).__init__(name, namespace, compress=compress, thread_safe=False)
        self.max_size = size
        self.entries = OrderedDict()
        self.size = 0

    @classmethod
    def initialize(cls, name, settings):
        return cls(name, settings.get(b'namespace', b''), compress=settings.get_bool(b'compress', True), compress_min=settings.get_int(b'compress_min', 16384), size=settings.get_int(b'size', 1024) * 1024)

    def evict_entry(self, key):
        """Evict a single key."""
        if key in self.entries:
            entry = self.entries.pop(key)
            self.size -= len(entry.value)

    def reclaim(self, num_bytes):
        """Reclaim at least `num_bytes`"""
        log.debug(b'%r size=%s bytes', self, self.size)
        log.debug(b'%r reclaiming %s bytes', self, num_bytes)
        reclaimed = 0
        while self.entries and reclaimed < num_bytes:
            key, entry = self.entries.popitem(last=False)
            log.debug(b'%r evicting %r', self, key)
            deleted_bytes_count = len(entry.value)
            self.size -= deleted_bytes_count
            reclaimed += deleted_bytes_count

        return reclaimed >= num_bytes

    def _get(self, key, default):
        try:
            entry = self.entries.pop(key)
        except KeyError:
            return default

        value_bytes = entry.value
        value_size = len(value_bytes)
        self.size -= value_size
        if entry.expire_time and get_time() > entry.expire_time:
            return default
        self.entries[key] = entry
        self.size += value_size
        return self.decode_value(value_bytes)

    def _set(self, key, value, time):
        value_bytes = self.encode_value(value)
        value_size = len(value_bytes)
        if value_size > self.max_size:
            return
        else:
            self.evict_entry(key)
            if self.size + value_size > self.max_size:
                if not self.reclaim(self.size + value_size - self.max_size):
                    return
            expire_time = None if time == 0 else get_time() + time / 1000.0
            self.entries[key] = CacheEntry(value_bytes, expire_time)
            self.size += value_size
            return

    def _delete(self, key):
        if key in self.entries:
            self.size -= len(self.entries.pop(key).value)


if __name__ == b'__main__':
    cache = MemoryCache(b'test', b'')
    cache.set(b'foo', b'bar')
    print(cache.get(b'foo'))
    print(cache.encode_value(b'value'))