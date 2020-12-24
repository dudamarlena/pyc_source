# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/cloudtb/tests/test_iteration.py
# Compiled at: 2013-11-12 16:48:22
import pdb
try:
    from .. import iteration
    from .. import dectools
except ValueError:
    try:
        import iteration, dectools
        print 'Running from within cloudtb'
    except:
        import sys
        sys.path.insert(1, '..')
        import iteration, dectools
        print 'Running as __main__'

import unittest, random
DEBUG = True

def get_ranges(number):
    return (range(n, n + 100) for n in range(number))


@dectools.debug(DEBUG)
def test_basic(self):
    a1 = xrange(0, 100)
    self.assertIterEqual(a1, self.get_object(a1))


@dectools.debug(DEBUG)
def test_add(self):
    a1, a2 = get_ranges(2)
    self.assertIterEqual(a1 + a2, self.get_object(a1) + self.get_object(a2))


@dectools.debug(DEBUG)
def test_extend(self):
    a1, a2 = get_ranges(2)
    b1 = self.get_object(a1)
    a1.extend(a2)
    b1.front_extend(a2)
    self.assertIterEqual(a1, b1)


@dectools.debug(DEBUG)
def test_extend_front(self):
    a1, a2 = get_ranges(2)
    b1 = self.get_object(a1)
    b1.front_extend(a2)
    self.assertIterEqual(a2 + a1, b1)


@dectools.debug(DEBUG)
def test_slice(self, recreate=True):
    a1 = range(-100, 1000)
    b1 = self.get_object(a1)
    b1[100]
    start, stop, step = (0, None, 5)
    self.assertIterEqual(a1[start:stop:step], b1[start:stop:step])
    start = 100
    if recreate:
        b1 = self.get_object(a1)
    print type(b1)
    self.assertIterEqual(a1[start:stop:step], b1[start:stop:step])
    stop = 450
    if recreate:
        b1 = self.get_object(a1)
    self.assertIterEqual(a1[start:stop:step], b1[start:stop:step])
    step = 1
    if recreate:
        b1 = self.get_object(a1)
    self.assertIterEqual(a1[start:stop:step], b1[start:stop:step])
    return


@dectools.debug(DEBUG)
def test_slice_repeat(self, reobject=False):
    st, end = (100, 1233)
    a1 = range(st, end)
    b1 = self.get_object(a1)
    start, stop, step = 0, end, 5
    a1 = a1[start:stop:step]
    b1 = b1[start:stop:step]
    if reobject:
        b1 = self.get_object(b1)
    start, stop, step = 0, end / 10, 12
    a1 = a1[start:stop:step]
    b1 = b1[start:stop:step]
    self.assertIterEqual(a1, b1)


@dectools.debug(DEBUG)
def test_backward_slice(self):
    a1 = range(-100, 1000)
    b1 = self.get_object(a1)
    start, stop, step = (1000, -100, -30)
    self.assertIterEqual(a1[start:stop:step], b1[start:stop:step])


@dectools.debug(DEBUG)
def test_getitem(self, recreate=True):
    a1 = range(-100, 1000)
    b1 = self.get_object(a1)
    for index in xrange(100, 1000, 33):
        if recreate:
            b1 = self.get_object(a1)
        self.assertEqual(a1[index], b1[index])


class std_iterator(object):

    def test_basic(self):
        return test_basic(self)

    def test_extend(self):
        return test_extend(self)

    def test_extend_front(self):
        return test_extend_front(self)

    def test_slice(self):
        return test_slice(self)

    def test_slice_repeat(self):
        return test_slice_repeat(self)

    def test_getitem(self):
        return test_getitem(self)

    def assertIterEqual(self, iter1, iter2):
        iter1, iter2 = iter(iter1), iter(iter2)
        try:
            next(next(iter1) != n for n in iter2)
        except StopIteration:
            self.fail()


class bitterTest(unittest.TestCase, std_iterator):

    def get_object(self, *args, **kwargs):
        return iteration.biter(*args, **kwargs)

    def test_slice_repeat(self):
        return test_slice_repeat(self, reobject=True)


class soliditerTest(unittest.TestCase, std_iterator):

    def get_object(self, *args, **kwargs):
        return iteration.soliditer(*args, **kwargs)

    def test_getitem(self):
        return test_getitem(self, recreate=False)


class fiTests(unittest.TestCase):

    def setUp(self):
        self.a1 = range(-1000, 1000)
        self.aempty = (0, ) * 1000

    def testForward(self):
        for i, n in enumerate(self.a1[::33]):
            i *= 33
            self.assertEqual(i, iteration.first_index_et(self.a1, n))
            self.assertEqual(i, iteration.first_index_is(self.a1, n))
            self.assertEqual(i, iteration.first_index_in(self.a1, (n, 'other',
             len(self.a1) + 10)))

        i = 500
        empt = list(self.aempty)
        empt[453] = 453
        self.assertEqual(453, iteration.first_index_ne(empt, 0))
        self.assertEqual(453, iteration.first_index_nis(empt, 0))
        self.assertEqual(453, iteration.first_index_nin(empt, (0, 10, 200)))


if __name__ == '__main__':
    unittest.main()