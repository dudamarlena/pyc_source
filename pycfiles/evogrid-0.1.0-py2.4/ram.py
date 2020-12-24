# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/caching/ram.py
# Compiled at: 2006-08-10 15:57:20
"""RAM-based cache implementation

This RAM cache is inspired on zope.app.cache.ram but a bit simpler cause we
don't want to inherit from ``Persistent`` and has a slightly different
interface as well.

The original implementation of RAMCache is copyright Zope Corporation and
contributors and is distributed under the terms of the Zope Public License.
"""
from cPickle import dumps
from evogrid.caching.interfaces import ICache
from threading import Lock
from zope.interface import implements
_marker = object()

class RAMCache(object):
    """Cache implementation that stores entries in a python dict"""
    __module__ = __name__
    implements(ICache)
    hits = 0
    misses = 0
    max_entries = None

    def __init__(self, max_entries=None):
        self.max_entries = max_entries
        self._store = {}
        self._sorted_keys = []
        self._lock = Lock()

    def __len__(self):
        return len(self._store)

    def invalidate(self, key=None):
        if key is None:
            self._lock.acquire()
            try:
                self._store.clear()
                del self._sorted_keys[:]
            finally:
                self._lock.release()
        else:
            key = self._buildKey(key)
            if key not in self._store:
                return
            self._lock.acquire()
            try:
                if key in self._store:
                    del self._store[key]
                    self._sorted_keys.remove(key)
            finally:
                self._lock.release()
        return

    def query(self, key, default=None):
        """Search the store to find a matching entry

        If nothing is found return default. If a matching entry is found,
        the _sorted_keys list order is updated. The misses and hits counters
        are updated.
        """
        key = self._buildKey(key)
        _store, _sorted_keys = self._store, self._sorted_keys
        result = _store.get(key, _marker)
        if result is _marker:
            self.misses += 1
            return default
        self._lock.acquire()
        try:
            if key in _store:
                _sorted_keys.remove(key)
                _sorted_keys.insert(0, key)
        finally:
            self._lock.release()
        self.hits += 1
        return result

    def set(self, key, data):
        """Add data to the store

        Check that the store size does not exceed ``max_entries``.
        """
        key = self._buildKey(key)
        _store, _sorted_keys = self._store, self._sorted_keys
        if key in _store and _store[key] == data:
            return
        self._lock.acquire()
        try:
            if key not in _store:
                len_self = len(self)
                max_entries = self.max_entries
                if max_entries is not None and len_self >= max_entries:
                    for i in xrange(len_self - max_entries + 1):
                        del _store[_sorted_keys.pop()]

                _store[key] = data
                _sorted_keys.insert(0, key)
        finally:
            self._lock.release()
        return

    def _buildKey(kw):
        """Build a tuple which can be used as an index for a cached value"""
        k = tuple(sorted(kw.iteritems()))
        try:
            return hash(k)
        except TypeError:
            return dumps(k)

    _buildKey = staticmethod(_buildKey)