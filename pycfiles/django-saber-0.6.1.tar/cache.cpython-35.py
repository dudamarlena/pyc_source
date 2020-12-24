# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jvai/code/django-saber/djangosaber/cache.py
# Compiled at: 2015-10-09 09:23:44
# Size of source mod 2**32: 550 bytes
from cachetools import LRUCache
import threading
_thread_locals = threading.local()

def threaded_cache(name='_cache'):
    if not hasattr(_thread_locals, name):
        set_cache(name)
    return getattr(_thread_locals, name)


def get_cache():
    return LRUCache(maxsize=20000)


def set_cache(name):
    setattr(_thread_locals, name, get_cache())


class ObjectCachedMixin(object):

    @property
    def _cache(self):
        return threaded_cache()


class DictCachedMixin(dict):

    @property
    def _cache(self):
        return threaded_cache()