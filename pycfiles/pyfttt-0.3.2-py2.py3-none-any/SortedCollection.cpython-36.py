# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/common/SortedCollection.py
# Compiled at: 2017-07-07 09:28:37
# Size of source mod 2**32: 7929 bytes
from bisect import bisect_left, bisect_right

class SortedCollection(object):
    """SortedCollection"""

    def __init__(self, iterable=(), key=None):
        self._given_key = key
        key = (lambda x: x) if key is None else key
        decorated = sorted((key(item), item) for item in iterable)
        self._keys = [k for k, item in decorated]
        self._items = [item for k, item in decorated]
        self._key = key

    def _getkey(self):
        return self._key

    def _setkey(self, key):
        if key is not self._key:
            self.__init__((self._items), key=key)

    def _delkey(self):
        self._setkey(None)

    key = property(_getkey, _setkey, _delkey, 'key function')

    def clear(self):
        self.__init__([], self._key)

    def copy(self):
        return self.__class__(self, self._key)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, i):
        return self._items[i]

    def __iter__(self):
        return iter(self._items)

    def __reversed__(self):
        return reversed(self._items)

    def __repr__(self):
        return '%s(%r, key=%s)' % (
         self.__class__.__name__,
         self._items,
         getattr(self._given_key, '__name__', repr(self._given_key)))

    def __reduce__(self):
        return (
         self.__class__, (self._items, self._given_key))

    def __contains__(self, item):
        k = self._key(item)
        i = bisect_left(self._keys, k)
        j = bisect_right(self._keys, k)
        return item in self._items[i:j]

    def index(self, item):
        """Find the position of an item.  Raise ValueError if not found."""
        k = self._key(item)
        i = bisect_left(self._keys, k)
        j = bisect_right(self._keys, k)
        return self._items[i:j].index(item) + i

    def count(self, item):
        """Return number of occurrences of item"""
        k = self._key(item)
        i = bisect_left(self._keys, k)
        j = bisect_right(self._keys, k)
        return self._items[i:j].count(item)

    def insert(self, item):
        """Insert a new item.  If equal keys are found, add to the left"""
        k = self._key(item)
        i = bisect_left(self._keys, k)
        self._keys.insert(i, k)
        self._items.insert(i, item)

    def insert_right(self, item):
        """Insert a new item.  If equal keys are found, add to the right"""
        k = self._key(item)
        i = bisect_right(self._keys, k)
        self._keys.insert(i, k)
        self._items.insert(i, item)

    def remove(self, item):
        """Remove first occurence of item.  Raise ValueError if not found"""
        i = self.index(item)
        del self._keys[i]
        del self._items[i]

    def find(self, k):
        """Return first item with a key == k.  Raise ValueError if not found."""
        i = bisect_left(self._keys, k)
        if i != len(self):
            if self._keys[i] == k:
                return self._items[i]
        raise ValueError('No item found with key equal to: %r' % (k,))

    def find_le(self, k):
        """Return last item with a key <= k.  Raise ValueError if not found."""
        i = bisect_right(self._keys, k)
        if i:
            return self._items[(i - 1)]
        raise ValueError('No item found with key at or below: %r' % (k,))

    def find_lt(self, k):
        """Return last item with a key < k.  Raise ValueError if not found."""
        i = bisect_left(self._keys, k)
        if i:
            return self._items[(i - 1)]
        raise ValueError('No item found with key below: %r' % (k,))

    def find_ge(self, k):
        """Return first item with a key >= equal to k.  Raise ValueError if not found"""
        i = bisect_left(self._keys, k)
        if i != len(self):
            return self._items[i]
        raise ValueError('No item found with key at or above: %r' % (k,))

    def find_gt(self, k):
        """Return first item with a key > k.  Raise ValueError if not found"""
        i = bisect_right(self._keys, k)
        if i != len(self):
            return self._items[i]
        raise ValueError('No item found with key above: %r' % (k,))

    def between(self, ge, le):
        g = bisect_left(self._keys, ge)
        l = bisect_right(self._keys, le)
        if g != len(self):
            if l != len(self):
                return self._items[g:l]
        raise ValueError('No item found between keys : %r,%r' % (ge, le))

    def inside(self, ge, le):
        l = bisect_right(self._keys, le)
        g = bisect_left(self._keys, ge)
        if g != len(self):
            if l != len(self):
                if g != l:
                    return self._items[g:l]
        if g != len(self):
            if l != len(self):
                if g == l:
                    return [
                     self._items[g]]
        if g != len(self):
            return self._items[g - 1:l]
        else:
            if l != len(self):
                return self._items[g:l - 1]
            return self._items[g - 1:l - 1]
        raise ValueError('No item found inside keys: %r,%r' % (ge, le))

    def around(self, k):
        g = bisect_right(self._keys, k)
        l = bisect_left(self._keys, k)
        if g != len(self):
            if l != len(self):
                return self._items[g:l]
        raise ValueError('No item found around key : %r' % (k,))