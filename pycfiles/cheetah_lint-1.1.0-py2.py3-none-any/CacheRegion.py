# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/CacheRegion.py
# Compiled at: 2019-09-22 10:12:27
__doc__ = "\nCache holder classes for Cheetah:\n\nCache regions are defined using the #cache Cheetah directive. Each\ncache region can be viewed as a dictionary (keyed by cacheRegionID)\nhandling at least one cache item (the default one). It's possible to add\ncacheItems in a region by using the `varyBy` #cache directive parameter as\nin the following example::\n\n   #def getArticle\n      this is the article content.\n   #end def\n\n   #cache varyBy=$getArticleID()\n      $getArticle($getArticleID())\n   #end cache\n\nThe code above will generate a CacheRegion and add new cacheItem for each value\nof $getArticleID().\n"
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

import time, Cheetah.CacheStore

class CacheItem(object):
    """
    A CacheItem is a container storing:

        - cacheID (string)
        - refreshTime (timestamp or None) : last time the cache was refreshed
        - data (string) : the content of the cache
    """

    def __init__(self, cacheItemID, cacheStore):
        self._cacheItemID = cacheItemID
        self._cacheStore = cacheStore
        self._refreshTime = None
        self._expiryTime = 0
        return

    def hasExpired(self):
        return self._expiryTime and time.time() > self._expiryTime

    def setExpiryTime(self, time):
        self._expiryTime = time

    def getExpiryTime(self):
        return self._expiryTime

    def setData(self, data):
        self._refreshTime = time.time()
        self._cacheStore.set(self._cacheItemID, data, self._expiryTime)

    def getRefreshTime(self):
        return self._refreshTime

    def getData(self):
        assert self._refreshTime
        return self._cacheStore.get(self._cacheItemID)

    def renderOutput(self):
        """Can be overridden to implement edge-caching"""
        return self.getData() or ''

    def clear(self):
        self._cacheStore.delete(self._cacheItemID)
        self._refreshTime = None
        return


class _CacheDataStoreWrapper(object):

    def __init__(self, dataStore, keyPrefix):
        self._dataStore = dataStore
        self._keyPrefix = keyPrefix

    def get(self, key):
        return self._dataStore.get(self._keyPrefix + key)

    def delete(self, key):
        self._dataStore.delete(self._keyPrefix + key)

    def set(self, key, val, time=0):
        self._dataStore.set(self._keyPrefix + key, val, time=time)


class CacheRegion(object):
    """
    A `CacheRegion` stores some `CacheItem` instances.

    This implementation stores the data in the memory of the current process.
    If you need a more advanced data store, create a cacheStore class that
    works with Cheetah's CacheStore protocol and provide it as the cacheStore
    argument to __init__.  For example you could use
    Cheetah.CacheStore.MemcachedCacheStore, a wrapper around the Python
    memcached API (http://www.danga.com/memcached).
    """
    _cacheItemClass = CacheItem

    def __init__(self, regionID, templateCacheIdPrefix='', cacheStore=None):
        self._isNew = True
        self._regionID = regionID
        self._templateCacheIdPrefix = templateCacheIdPrefix
        if not cacheStore:
            cacheStore = Cheetah.CacheStore.MemoryCacheStore()
        self._cacheStore = cacheStore
        self._wrappedCacheDataStore = _CacheDataStoreWrapper(cacheStore, keyPrefix=templateCacheIdPrefix + ':' + regionID + ':')
        self._cacheItems = {}

    def isNew(self):
        return self._isNew

    def clear(self):
        """ drop all the caches stored in this cache region """
        for cacheItemId in list(self._cacheItems.keys()):
            cacheItem = self._cacheItems[cacheItemId]
            cacheItem.clear()
            del self._cacheItems[cacheItemId]

    def getCacheItem(self, cacheItemID):
        """ Lazy access to a cacheItem

            Try to find a cache in the stored caches. If it doesn't
            exist, it's created.

            Returns a `CacheItem` instance.
        """
        cacheItemID = md5(str(cacheItemID).encode('ascii')).hexdigest()
        if cacheItemID not in self._cacheItems:
            cacheItem = self._cacheItemClass(cacheItemID=cacheItemID, cacheStore=self._wrappedCacheDataStore)
            self._cacheItems[cacheItemID] = cacheItem
            self._isNew = False
        return self._cacheItems[cacheItemID]