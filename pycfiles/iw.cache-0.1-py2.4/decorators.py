# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/cache/decorators.py
# Compiled at: 2007-12-05 09:41:22
"""
cache decorators
"""
__docformat__ = 'restructuredtext'
import zope.component, plone.memoize.volatile
from iw.cache.interfaces import IIWRAMCache
from iw.cache.interfaces import IIWMemcachedClient
from iw.cache.utils import get_storage
from iw.cache.keys import cache_key

def cache(ns, get_key=None, maxAge=3600, storage=IIWRAMCache):
    """a cache decorator
    """
    get_cache = lambda *a, **k: get_storage(ns, maxAge, storage)
    if not get_key:
        get_key = cache_key
    return plone.memoize.volatile.cache(get_key, get_cache=get_cache)


def ramcache(ns, get_key=None, maxAge=3600):
    return cache(ns, get_key=get_key, maxAge=maxAge, storage=IIWRAMCache)


def memcache(ns, get_key=None, maxAge=3600):
    return cache(ns, get_key=get_key, maxAge=maxAge, storage=IIWMemcachedClient)