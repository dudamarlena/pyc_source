# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/common/SortedCollection.py
# Compiled at: 2017-07-07 09:28:37
# Size of source mod 2**32: 7929 bytes
from bisect import bisect_left, bisect_right

class SortedCollection(object):
    __doc__ = "Sequence sorted by a key function.\n\n    SortedCollection() is much easier to work with than using bisect() directly.\n    It supports key functions like those use in sorted(), min(), and max().\n    The result of the key function call is saved so that keys can be searched\n    efficiently.\n\n    Instead of returning an insertion-point which can be hard to interpret, the\n    five find-methods return a specific item in the sequence. They can scan for\n    exact matches, the last item less-than-or-equal to a key, or the first item\n    greater-than-or-equal to a key.\n\n    Once found, an item's ordinal position can be located with the index() method.\n    New items can be added with the insert() and insert_right() methods.\n    Old items can be deleted with the remove() method.\n\n    The usual sequence methods are provided to support indexing, slicing,\n    length lookup, clearing, copying, forward and reverse iteration, contains\n    checking, item counts, item removal, and a nice looking repr.\n\n    Finding and indexing are O(log n) operations while iteration and insertion\n    are O(n).  The initial sort is O(n log n).\n\n    The key function is stored in the 'key' attibute for easy introspection or\n    so that you can assign a new key function (triggering an automatic re-sort).\n\n    In short, the class was designed to handle all of the common use cases for\n    bisect but with a simpler API and support for key functions.\n\n    >>> from pprint import pprint\n    >>> from operator import itemgetter\n\n    >>> s = SortedCollection(key=itemgetter(2))\n    >>> for record in [\n    ...         ('roger', 'young', 30),\n    ...         ('angela', 'jones', 28),\n    ...         ('bill', 'smith', 22),\n    ...         ('david', 'thomas', 32)]:\n    ...     s.insert(record)\n\n    >>> pprint(list(s))         # show records sorted by age\n    [('bill', 'smith', 22),\n     ('angela', 'jones', 28),\n     ('roger', 'young', 30),\n     ('david', 'thomas', 32)]\n\n    >>> s.find_le(29)           # find oldest person aged 29 or younger\n    ('angela', 'jones', 28)\n    >>> s.find_lt(28)           # find oldest person under 28\n    ('bill', 'smith', 22)\n    >>> s.find_gt(28)           # find youngest person over 28\n    ('roger', 'young', 30)\n\n    >>> r = s.find_ge(32)       # find youngest person aged 32 or older\n    >>> s.index(r)              # get the index of their record\n    3\n    >>> s[3]                    # fetch the record at that index\n    ('david', 'thomas', 32)\n\n    >>> s.key = itemgetter(0)   # now sort by first name\n    >>> pprint(list(s))\n    [('angela', 'jones', 28),\n     ('bill', 'smith', 22),\n     ('david', 'thomas', 32),\n     ('roger', 'young', 30)]\n\n    "

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