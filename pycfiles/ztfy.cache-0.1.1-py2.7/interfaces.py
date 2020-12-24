# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/cache/interfaces.py
# Compiled at: 2012-06-11 15:33:55
from ztfy.cache.metadirectives import ICacheProxyHandlerBase
from zope.interface import Interface
from zope.schema import TextLine, Choice
from ztfy.cache import _

class ICacheHandler(Interface):
    """ICacheHandler is a common basic interface to several cache managers"""

    def set(self, namespace, key, value):
        """Set the given value for the given key"""
        pass

    def query(self, namespace, key, default=None):
        """Query cache for given key"""
        pass

    def invalidate(self, namespace, key):
        """Invalidate key in given namespace"""
        pass

    def invalidateAll(self):
        """Invalidate all cache entries"""
        pass


class IPersistentCacheProxyHandlerInfo(Interface):
    """Cache proxy handler interface"""
    cache_interface = Choice(title=_('Cache utility interface'), required=True, vocabulary='Interfaces')
    cache_name = TextLine(title=_('Cache utility name'), required=False)


class IPersistentCacheProxyHandler(ICacheProxyHandlerBase, IPersistentCacheProxyHandlerInfo):
    """Persistent cache proxy handler interface"""
    pass