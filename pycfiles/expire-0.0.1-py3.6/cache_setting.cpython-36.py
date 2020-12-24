# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/expire/cache_setting.py
# Compiled at: 2018-03-05 19:56:07
# Size of source mod 2**32: 1390 bytes
from expire.memory_cache import MemoryCache

class CacheSetting:
    __doc__ = "\n    Cache setting configuration\n    cache_dict provides the basic configuration of the cache\n        - cache_class: such as MemoryCache RedisCache etc.\n        - cache_config: basic configuration, just like redis's host port db password etc.\n        - serializer: such as JsonSerializer PickleSerializer.\n    "
    cache_dict = {'cache_class':MemoryCache, 
     'cache_config':{},  'serializer':None}

    def __init__(self, settings=None):
        self.cache = getattr(settings, 'cache', self.cache_dict)
        if not isinstance(self.cache.get('cache_config'), dict):
            raise ValueError('Key cache_config must be a dict')
        serializer = self.cache.get('serializer')
        self.ttl = self.cache.get('ttl')
        self.instance = (self.cache['cache_class'])(serializer=serializer, **self.cache['cache_config'])

    def set(self, key, value, ttl=None, **kwargs):
        ttl = ttl or self.ttl
        return (self.instance.set)(key, value, ttl=ttl, **kwargs)

    def get(self, key, default=None, **kwargs):
        return (self.instance.get)(key, default=default, **kwargs)

    def exists(self, key, **kwargs):
        return (self.instance.exists)(key, **kwargs)

    def incr(self, key, **kwargs):
        return (self.instance.incr)(key, **kwargs)