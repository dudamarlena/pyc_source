# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/cache/utility.py
# Compiled at: 2012-06-11 15:33:55
from persistent import Persistent
from ztfy.cache.interfaces import ICacheHandler, IPersistentCacheProxyHandler
from ztfy.cache.metadirectives import ICacheProxyHandler
from zope.component import queryUtility
from zope.container.contained import Contained
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

class CacheProxyHandler(object):
    """Cache proxy handler"""
    implements(ICacheProxyHandler)
    name = FieldProperty(ICacheProxyHandler['name'])
    cache_interface = FieldProperty(ICacheProxyHandler['cache_interface'])
    cache_name = FieldProperty(ICacheProxyHandler['cache_name'])

    def __init__(self, name, cache_interface, cache_name):
        self.name = name
        self.cache_interface = cache_interface
        self.cache_name = cache_name

    def getCache(self):
        return ICacheHandler(queryUtility(self.cache_interface, self.cache_name), None)


class PersistentCacheProxyHandler(Persistent, Contained):
    """Persistent cache proxy handler"""
    implements(IPersistentCacheProxyHandler)
    cache_interface = FieldProperty(IPersistentCacheProxyHandler['cache_interface'])
    cache_name = FieldProperty(IPersistentCacheProxyHandler['cache_name'])

    def getCache(self):
        return ICacheHandler(queryUtility(self.cache_interface, self.cache_name), None)