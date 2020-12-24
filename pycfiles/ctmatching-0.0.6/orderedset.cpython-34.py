# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Workspace\py34\py34_projects\ctmatching-project\ctmatching\orderedset.py
# Compiled at: 2016-09-08 01:30:12
# Size of source mod 2**32: 6653 bytes
"""
Module description
~~~~~~~~~~~~~~~~~~
This module provide a pure python OrderedSet data type implementation.
inspired by http://code.activestate.com/recipes/576694/

Ordered set is a set that remembers original insertion order. Also support
add item, remove item, iterate, union, intersect, difference, classic set
operations.

Note: this is not a high performance implementation, don't use this for 
big data and product environment. But there's are better one:

orderedset: a Cython implementation. https://pypi.python.org/pypi/orderedset

Usage examples
~~~~~~~~~~~~~~
Add, discard, pop::

    >>> s = OrderedSet()
    >>> s.add(1)
    >>> s.add(2)
    >>> s.add(3)
    >>> s
    OrderedSet([1, 2, 3])
    
    >>> s.discard(2)
    >>> s
    OrderedSet([1, 3])
    
    >>> s.pop()
    3
    >>> s
    OrderedSet([1])
    
Union, intersect, difference::

    >>> s = OrderedSet("abracadaba") # {"a", "b", "r", "c", "d"}
    >>> t = OrderedSet("simcsalabim") # {"s", "i", "m", "c", "a", "l", "b"}
    >>> s | t # s union t
    OrderedSet(['a', 'b', 'r', 'c', 'd', 's', 'i', 'm', 'l'])
    
    >>> s & t # s intersect t
    OrderedSet(['c', 'a', 'b'])
    
    >>> s - t # s different t
    OrderedSet(['r', 'd'])

About
~~~~~
**Compatibility**

- Python2: Yes
- Python3: Yes
    

**Prerequisites**

- None

class, method, func, exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from __future__ import print_function
import collections

class OrderedSet(collections.MutableSet):
    __doc__ = 'A light weight OrderedSet data type pure Python implementation.\n    '

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]
        self.map = {}
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        """Add an item to the OrderedSet.

        Usage::

            >>> s = OrderedSet()
            >>> s.add(1)
            >>> s.add(2)
            >>> s.add(3)
            >>> s
            OrderedSet([1, 2, 3])

        **中文文档**

        添加一个元素, 如果该元素已经存在, 则不会有任何作用。
        """
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        """Remove a item from its member if it is a member.

        Usage::

            >>> s = OrderedSet([1, 2, 3])
            >>> s.discard(2)
            >>> s
            OrderedSet([1, 3])

        **中文文档**

        从有序集合中删除一个元素, 同时保持集合依然有序。
        """
        if key in self.map:
            key, prev, next_item = self.map.pop(key)
            prev[2] = next_item
            next_item[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        """Remove and returns the last added item.

        Usage::

            >>> s = OrderedSet([1, 2, 3])
            >>> s.pop()
            3
            >>> s
            OrderedSet([1, 2])

        **中文文档**

        移除并返回最后添加的元素。
        """
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

    @staticmethod
    def union(*argv):
        """Returns union of sets as a new set. basically it's
        Items are ordered by set1, set2, ...

        **中文文档**

        求多个有序集合的并集, 按照第一个集合, 第二个, ..., 这样的顺序。
        """
        res = OrderedSet()
        for ods in argv:
            res = res | ods

        return res

    @staticmethod
    def intersection(*argv):
        """Returns the intersection of multiple sets.
        Items are ordered by set1, set2, ...

        **中文文档**

        求多个有序集合的交集, 按照第一个集合, 第二个, ..., 这样的顺序。
        """
        res = OrderedSet(argv[0])
        for ods in argv:
            res = ods & res

        return res


def test_add_pop_and_discard():
    """test, add(item), pop(last=True/False), discard(item) method
    """
    s = OrderedSet('abcde')
    assert list(s) == ['a', 'b', 'c', 'd', 'e']
    s.pop()
    assert list(s) == ['a', 'b', 'c', 'd']
    s.pop(last=False)
    assert list(s) == ['b', 'c', 'd']
    s.discard('c')
    assert list(s) == ['b', 'd']


def test_union_intersect_and_difference():
    """test union, intersect, difference operation
    """
    s = OrderedSet('abracadaba')
    t = OrderedSet('simcsalabim')
    assert list(s | t) == ['a', 'b', 'r', 'c', 'd', 's', 'i', 'm', 'l']
    assert list(s & t) == ['c', 'a', 'b']
    assert list(s - t) == ['r', 'd']


def test_staticmethod():
    """test customized batch union and intersect static method
    """
    r = OrderedSet('buag')
    s = OrderedSet('abracadaba')
    t = OrderedSet('simcsalabim')
    expected = [
     'b', 'u', 'a', 'g', 'r', 'c', 'd', 's', 'i', 'm', 'l']
    assert list(OrderedSet.union(r, s, t)) == expected
    assert list(OrderedSet.intersection(r, s, t)) == ['b', 'a']


if __name__ == '__main__':
    test_add_pop_and_discard()
    test_union_intersect_and_difference()
    test_staticmethod()