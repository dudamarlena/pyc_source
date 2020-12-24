# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pagingish/tests/test_listpager.py
# Compiled at: 2009-05-05 06:01:15
from unittest import TestCase
from pagingish.listpager import Pager

def sequence_generator(num):
    return xrange(num)


def assert_page(page, prev, rows, next, stats, expecteds):
    if page > len(expecteds):
        expected = expecteds[(-1)]
    else:
        expected = expecteds[(page - 1)]
    actual = rows
    print 'page', page
    print 'prev', prev
    print 'next', next
    print 'rows', rows
    print 'expected', expected
    print 'actual', actual
    assert expected == actual
    if page >= len(expecteds):
        assert next is None
    else:
        assert next is not None
    if page <= 1 or page > len(expecteds) and len(expecteds) == 1:
        assert prev is None
    else:
        assert prev is not None
    return


e5pp_10t = [
 [
  0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
e4pp_10t = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]

def t(d):
    return (
     d['prev'], d['items'], d['next'], d['stats'])


class TestPager_10items(TestCase):

    def setUp(self):
        self.data = sequence_generator(10)

    def test_roundtrip_5pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_10t)
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(2, prev, rows, next, stats, e5pp_10t)
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, e5pp_10t)
        return

    def test_roundtrip_4pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(4, None))
        assert_page(1, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, next))
        assert_page(2, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, next))
        assert_page(3, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, prev))
        assert_page(2, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, prev))
        assert_page(1, prev, rows, next, stats, e4pp_10t)
        return

    def test_upone_downone_4pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(4, None))
        assert_page(1, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, next))
        assert_page(2, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, prev))
        assert_page(1, prev, rows, next, stats, e4pp_10t)
        return

    def test_prev_at_start_4pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(4, None))
        assert_page(1, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, next))
        assert_page(2, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, prev))
        assert_page(1, prev, rows, next, stats, e4pp_10t)
        (prev, rows, next, stats) = t(p.get(4, prev))
        assert_page(1, prev, rows, next, stats, e4pp_10t)
        return


e5pp_5t = [
 [
  0, 1, 2, 3, 4]]
e4pp_5t = [[0, 1, 2, 3], [4]]
e6pp_5t = [[0, 1, 2, 3, 4]]

class TestPager_5items(TestCase):

    def setUp(self):
        self.data = sequence_generator(5)

    def test_roundtrip_5pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_5t)
        return

    def test_roundtrip_4pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(4, None))
        assert_page(1, prev, rows, next, stats, e4pp_5t)
        (prev, rows, next, stats) = t(p.get(4, next))
        assert_page(2, prev, rows, next, stats, e4pp_5t)
        (prev, rows, next, stats) = t(p.get(4, prev))
        assert_page(1, prev, rows, next, stats, e4pp_5t)
        return

    def test_prev_at_start_4pp(self):
        p = Pager(self.data)
        print '-----------data', self.data
        (prev, rows, next, stats) = t(p.get(4, None))
        (prev, rows, next, stats) = t(p.get(4, next))
        (prev, rows, next, stats) = t(p.get(4, prev))
        (prev, rows, next, stats) = t(p.get(4, prev))
        assert_page(1, prev, rows, next, stats, e4pp_5t)
        return

    def test_next_at_end_4pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(4, None))
        (prev, rows, next, stats) = t(p.get(4, next))
        (prev, rows, next, stats) = t(p.get(4, next))
        assert_page(1, prev, rows, next, stats, e4pp_5t)
        return

    def test_roundtrip_6pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(6, None))
        assert_page(1, prev, rows, next, stats, e6pp_5t)
        (prev, rows, next, stats) = t(p.get(6, next))
        assert_page(1, prev, rows, next, stats, e6pp_5t)
        (prev, rows, next, stats) = t(p.get(6, prev))
        assert_page(1, prev, rows, next, stats, e6pp_5t)
        return

    def test_prev_at_start_6pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(6, None))
        assert_page(1, prev, rows, next, stats, e6pp_5t)
        (prev, rows, next, stats) = t(p.get(6, prev))
        assert_page(1, prev, rows, next, stats, e6pp_5t)
        return

    def test_next_at_end_6pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(6, None))
        assert_page(1, prev, rows, next, stats, e6pp_5t)
        (prev, rows, next, stats) = t(p.get(6, next))
        assert_page(1, prev, rows, next, stats, e6pp_5t)
        return


e5pp_1t = [
 [
  0]]

class TestPager_1items(TestCase):

    def setUp(self):
        self.data = sequence_generator(1)

    def test_roundtrip_5pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_1t)
        return

    def test_next_at_end_5pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(5, None))
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(1, prev, rows, next, stats, e5pp_1t)
        return

    def test_prev_at_start_5pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(5, None))
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, e5pp_1t)
        return


e5pp_0t = [[]]

class TestPager_0items(TestCase):

    def setUp(self):
        self.data = sequence_generator(0)

    def test_roundtrip_5pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(5, None))
        assert_page(1, prev, rows, next, stats, e5pp_0t)
        return

    def test_next_at_end_5pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(5, None))
        (prev, rows, next, stats) = t(p.get(5, next))
        assert_page(1, prev, rows, next, stats, e5pp_0t)
        return

    def test_prev_at_start_5pp(self):
        p = Pager(self.data)
        (prev, rows, next, stats) = t(p.get(5, None))
        (prev, rows, next, stats) = t(p.get(5, prev))
        assert_page(1, prev, rows, next, stats, e5pp_0t)
        return