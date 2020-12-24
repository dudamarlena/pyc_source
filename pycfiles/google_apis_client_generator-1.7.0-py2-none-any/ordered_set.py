# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/utilities/ordered_set.py
# Compiled at: 2019-01-24 16:56:47
"""Ordered set implementations."""
import collections

class _OrderedSetBase(object):

    def __init__(self, iterable=None):
        self._set = collections.OrderedDict()
        if iterable:
            for i in iterable:
                self._set[i] = 1

    def __len__(self):
        return len(self._set)

    def __contains__(self, thing):
        return thing in self._set

    def __iter__(self):
        return iter(self._set)


class _MutableSetBase(_OrderedSetBase):

    def add(self, thing):
        self._set[thing] = 1

    def discard(self, thing):
        if thing in self._set:
            del self._set[thing]

    def clear(self):
        self._set.clear()


class FrozenOrderedSet(_OrderedSetBase, collections.Set, collections.Hashable):
    __hash__ = collections.Set._hash


class MutableOrderedSet(_MutableSetBase, collections.MutableSet):
    pass