# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pagingish/tests/test_generic.py
# Compiled at: 2009-05-01 12:08:42
import unittest
from pagingish.genericpager import SkipLimitPager

def t(d):
    return (
     d['prev'], d['items'], d['next'], d['stats'])


def pager_func(l):

    def func(skip=None, limit=None):
        if skip is None:
            skip = 0
        if limit is None:
            limit = len(l)
        return l[skip:skip + limit]

    return func


class TestSkipLimitPager(unittest.TestCase):

    def test_walk(self):
        pager = SkipLimitPager(pager_func(range(20)))
        (prev, items, next, stats) = t(pager.get(5))
        assert items == range(0, 5)
        assert prev is None
        assert next
        (prev, items, next, stats) = t(pager.get(5, next))
        assert items == range(5, 10)
        assert prev
        assert next
        (prev, items, next, stats) = t(pager.get(5, next))
        (prev, items, next, stats) = t(pager.get(5, next))
        assert items == range(15, 20)
        assert prev
        assert not next
        (prev, items, next, stats) = t(pager.get(5, prev))
        (prev, items, next, stats) = t(pager.get(5, prev))
        (prev, items, next, stats) = t(pager.get(5, prev))
        assert items == range(0, 5)
        assert prev is None
        assert next
        return