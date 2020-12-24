# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /slapdsock/cache.py
# Compiled at: 2019-11-11 16:56:42
# Size of source mod 2**32: 1924 bytes
"""
slapdsock.cache - dict-like cache class

slapdsock - OpenLDAP back-sock listeners with Python
see https://www.stroeder.com/slapdsock.html

(c) 2015-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import time
__all__ = [
 'CacheDict']

class CacheDict(dict):
    __doc__ = '\n    Class implements a cache dictionary with\n    timestamps attached to all dict keys\n    '

    def __init__(self, cache_ttl=-1.0):
        """
        :cache_ttl: Time-to-live for cached entries in seconds
        """
        dict.__init__({})
        self._cache_ttl = cache_ttl
        self.cache_hit_count = 0
        self.max_cache_hit_time = 0.0

    def __getitem__(self, k):
        val, not_after = dict.__getitem__(self, k)
        if time.time() > not_after:
            dict.__delitem__(self, k)
            raise KeyError('cache entry expired')
        else:
            self.cache_hit_count += 1
            self.max_cache_hit_time = max(self.max_cache_hit_time, time.time() - not_after + self._cache_ttl)
            return val

    def __setitem__(self, k, v):
        return dict.__setitem__(self, k, (
         v, time.time() + self._cache_ttl))