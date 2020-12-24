# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/cache/memcached.py
# Compiled at: 2007-12-05 09:41:22
"""
memcached
"""
__docformat__ = 'restructuredtext'
import zope.component, zope.interface
from lovely.memcached.utility import MemcachedClient
from interfaces import IIWMemcachedClient
from interfaces import MemcachedError
NS = 'iw.cache.memcached'
_marker = object()

class IWMemcachedClient(MemcachedClient):
    """used to have a plone.memoize compatible
    storage.
    """
    __module__ = __name__
    zope.interface.implements(IIWMemcachedClient)

    def get(self, key, default=_marker):
        """returns query results"""
        value = super(IWMemcachedClient, self).query(key, ns=self.defaultNS, default=default)
        if value is _marker:
            raise MemcachedError('Seems the server for %s is not up' % self.defaultNS)
        return value

    def __setitem__(self, key, value):
        self.set(value, key, ns=self.defaultNS)