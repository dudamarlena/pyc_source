# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/cache/adapter.py
# Compiled at: 2012-06-11 15:33:55
from lovely.memcached.interfaces import IMemcachedClient
from zope.ramcache.interfaces.ram import IRAMCache
from ztfy.cache.interfaces import ICacheHandler
from zope.component import adapts
from zope.interface import implements

class RAMCacheAdapter(object):
    """RAM cache adapter"""
    adapts(IRAMCache)
    implements(ICacheHandler)

    def __init__(self, context):
        self.context = context

    def set(self, namespace, key, value):
        if not isinstance(key, dict):
            key = {'_key': key}
        self.context.set(value, namespace, key)

    def query(self, namespace, key, default=None):
        if not isinstance(key, dict):
            key = {'_key': key}
        return self.context.query(namespace, key, default)

    def invalidate(self, namespace, key=None):
        if key is not None and not isinstance(key, dict):
            key = {'_key': key}
        self.context.invalidate(namespace, key)
        return

    def invalidateAll(self):
        self.context.invalidateAll()


class MemcachedCacheAdapter(object):
    """Memcached cache adapter"""
    adapts(IMemcachedClient)
    implements(ICacheHandler)

    def __init__(self, context):
        self.context = context

    def set(self, namespace, key, value):
        self.context.set(value, key, ns=namespace)

    def query(self, namespace, key, default=None):
        return self.context.query(key, default, ns=namespace)

    def invalidate(self, namespace, key=None):
        self.context.invalidate(key, ns=namespace)

    def invalidateAll(self):
        self.context.invalidateAll()