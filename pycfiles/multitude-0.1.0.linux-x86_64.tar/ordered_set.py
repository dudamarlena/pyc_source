# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/multitude/ordered_set.py
# Compiled at: 2016-07-17 20:04:06
"""
Contains an implementation of a set with elements in order of insertion
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import collections
KEY = 0
NEXT = 1
PREV = 2
_NO_KEY_SENTINEL_VALUE = ()

class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self._end = end = []
        end += [None, end, end]
        self._map = {}
        if iterable is not None:
            self |= iterable
        return

    def __repr__(self):
        return (b'<OrderedSet({!r})>').format(list(self))

    def __eq__(self, other):
        is_equal = False
        if isinstance(other, OrderedSet):
            is_equal = len(self) == len(other) and list(self) == list(other)
        return is_equal

    def __len__(self):
        return len(self._map)

    def __contains__(self, key):
        return key in self._map

    def __iter__(self):
        end = self._end
        curr = end[NEXT]
        while curr is not end:
            yield curr[KEY]
            curr = curr[NEXT]

    def __reversed__(self):
        end = self._end
        curr = end[PREV]
        while curr is not end:
            yield curr[KEY]
            curr = curr[PREV]

    def add(self, key):
        if key not in self._map:
            end = self._end
            curr = end[PREV]
            curr[NEXT] = end[PREV] = self._map[key] = [key, end, curr]

    def discard(self, key):
        if key in self._map:
            key, next_node, prev_node = self._map.pop(key)
            prev_node[NEXT] = next_node
            next_node[PREV] = prev_node
        else:
            raise KeyError((b'No key {!r}').format(key))

    def pop(self, key=_NO_KEY_SENTINEL_VALUE):
        if not self:
            raise KeyError(b'set is empty')
        if key is _NO_KEY_SENTINEL_VALUE:
            key = self._end[PREV][KEY]
        elif key not in self:
            raise KeyError((b'No key {!r}').format(key))
        self.discard(key)
        return key