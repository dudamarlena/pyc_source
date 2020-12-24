# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/hydro/cache/in_memory.py
# Compiled at: 2016-03-22 15:09:41
from django.core.cache.backends.locmem import LocMemCache
from base_classes import CacheBase
from hydro.common.configurator import Configurator
__author__ = 'moshebasanchig'

class InMemoryCache(CacheBase):

    def __init__(self, params=None):
        self.cache = LocMemCache(name='Hydro', params={})

    def get(self, key):
        try:
            value = self.cache.get(key)
        except Exception as err:
            value = None

        return value

    def put(self, key, value, ttl=Configurator.CACHE_IN_MEMORY_KEY_EXPIRE):
        if ttl > Configurator.CACHE_IN_MEMORY_KEY_EXPIRE:
            ttl = Configurator.CACHE_IN_MEMORY_KEY_EXPIRE
        self.cache.set(key, value, ttl)


if __name__ == '__main__':
    from time import sleep
    key = 'a'
    val = {1: 1}
    cache = InMemoryCache()
    cache.put(key, val, None)
    sleep(5)
    print cache.get(key)