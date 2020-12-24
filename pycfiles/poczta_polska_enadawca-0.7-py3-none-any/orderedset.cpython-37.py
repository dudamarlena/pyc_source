# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/thirdparty/oset/orderedset.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 2300 bytes
import collections.abc as collections

class OrderedSet(collections.MutableSet):
    """OrderedSet"""
    KEY, PREV, NEXT = range(3)

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]
        self.map = {}
        if iterable is not None:
            self |= iterable

    def __contains__(self, key):
        return key in self.map

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

    def __iter__(self):
        end = self.end
        curr = end[self.NEXT]
        while curr is not end:
            yield curr[self.KEY]
            curr = curr[self.NEXT]

    def __len__(self):
        return len(self.map)

    def __reversed__(self):
        end = self.end
        curr = end[self.PREV]
        while curr is not end:
            yield curr[self.KEY]
            curr = curr[self.PREV]

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[self.PREV]
            curr[self.NEXT] = end[self.PREV] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[self.NEXT] = next
            next[self.PREV] = prev

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = next(reversed(self)) if last else next(iter(self))
        self.discard(key)
        return key

    def __del__(self):
        self.clear()

    def __repr__(self):
        class_name = self.__class__.__name__
        if not self:
            return '{0!s}()'.format(class_name)
        return '{0!s}({1!r})'.format(class_name, list(self))


if __name__ == '__main__':
    print(OrderedSet('abracadaba'))
    print(OrderedSet('simsalabim'))
    x = OrderedSet('abracadaba')