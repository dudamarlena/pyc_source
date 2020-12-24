# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/expire/__init__.py
# Compiled at: 2018-03-05 20:20:12
# Size of source mod 2**32: 436 bytes
from .cache_setting import CacheSetting
from .decorator import cached
from .memcached_cache import MemcachedCache
from .memory_cache import MemoryCache
from .redis_cache import RedisCache
from .serializer import JsonSerializer, PickleSerializer, StrSerializer

class Settings:
    __doc__ = 'Global Settings'
    cache = {'cache_class':MemoryCache, 
     'cache_config':{},  'serializer':None, 
     'ttl':None}