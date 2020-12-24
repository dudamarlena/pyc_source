# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/cache/ramcache.py
# Compiled at: 2007-12-05 09:41:22
"""
ram cache
"""
__docformat__ = 'restructuredtext'
import time, zope.component, zope.interface
from zope.app.cache.ram import RAMCache, Storage, writelock, cache_id_counter, cache_id_writelock
from zope.app.cache.interfaces import ICache
from iw.cache.interfaces import IIWRAMCache
caches = {}
NS = 'iw.cache.ramcache'
_marker = object()

class IWRAMCache(RAMCache):
    """used to have a plone.memoize compatible
    storage.

        >>> from iw.cache.ramcache import IWRAMCache
        >>> cache = IWRAMCache(maxAge=36000)
        >>> cache.maxAge = 3600
        >>> cache.set(1, 1)
        >>> cache.get(1)
        1
        >>> cache.get(2, 'not cached')
        'not cached'
    """
    __module__ = __name__
    zope.interface.implements(IIWRAMCache)

    def __init__(self, ns=None, maxAge=3600):
        self.ns = ns or NS
        super(IWRAMCache, self).__init__()
        self.maxAge = maxAge

    def get(self, key, default=_marker, ns=None, raw=False):
        """returns query results"""
        return super(IWRAMCache, self).query(ob=key, default=default)

    def set(self, value, key):
        s = self._getStorage()
        s._misses[key] = 0
        super(IWRAMCache, self).set(value, ob=key)

    def __setitem__(self, key, value):
        self.set(value, key)

    def _getStorage(self):
        """Finds or creates a storage object."""
        cacheId = self._cacheId
        writelock.acquire()
        try:
            if cacheId not in caches:
                caches[cacheId] = IWStorage(self.maxEntries, self.maxAge, self.cleanupInterval)
            self._v_storage = caches[cacheId]
        finally:
            writelock.release()
        return self._v_storage

    def _buildKey(kw):
        """Build a tuple which can be used as an index for a cached value"""
        return kw

    _buildKey = staticmethod(_buildKey)


class IWStorage(Storage):
    __module__ = __name__

    def getEntry(self, ob, key='main'):
        try:
            data = self._data[ob][key]
        except KeyError:
            if ob not in self._misses:
                self._misses[ob] = 0
            self._misses[ob] += 1
            raise
        else:
            if time.time() > data[1] + self.maxAge:
                raise KeyError(ob)
            data[2] += 1
            return data[0]