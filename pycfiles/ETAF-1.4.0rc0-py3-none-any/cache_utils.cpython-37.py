# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/arch/standalone/utils/cache_utils.py
# Compiled at: 2020-05-06 02:27:06
# Size of source mod 2**32: 1467 bytes
from cachetools import LRUCache, TTLCache
import time

class EvictLRUCache(LRUCache):

    def __init__(self, maxsize, getsizeof=None, evict=None):
        LRUCache.__init__(self, maxsize, getsizeof)
        self._EvictLRUCache__evict = evict

    def popitem(self):
        key, val = LRUCache.popitem(self)
        evict = self._EvictLRUCache__evict
        if evict:
            evict(key, val)
        return (
         key, val)


class EvictTTLCache(TTLCache):

    def __init__(self, maxsize, ttl, timer=time.time, getsizeof=None, evict=None):
        TTLCache.__init__(self, maxsize, ttl, timer, getsizeof)
        self._EvictTTLCache__evict = evict

    def popitem(self):
        key, val = TTLCache.popitem(self)
        evict = self._EvictTTLCache__evict
        if evict:
            evict(key, val)
        return (
         key, val)