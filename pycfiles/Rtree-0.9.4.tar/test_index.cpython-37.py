# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\projects\rtree\tests\test_index.py
# Compiled at: 2019-10-21 00:19:08
# Size of source mod 2**32: 1251 bytes
import unittest
from rtree import index

class IndexTests(unittest.TestCase):

    def test_stream_input(self):
        p = index.Property()
        sindex = index.Index((boxes15_stream()), properties=p)
        bounds = (0, 0, 60, 60)
        hits = sindex.intersection(bounds)
        self.assertEqual(sorted(hits), [0, 4, 16, 27, 35, 40, 47, 50, 76, 80])


def boxes15_stream(interleaved=True):
    boxes15 = np.genfromtxt('boxes_15x15.data')
    for i, (minx, miny, maxx, maxy) in enumerate(boxes15):
        if interleaved:
            yield (
             i, (minx, miny, maxx, maxy), 42)
        else:
            yield (
             i, (minx, maxx, miny, maxy), 42)


class ExceptionTests(unittest.TestCase):

    def test_exception_in_generator(self):
        """Assert exceptions raised in callbacks are raised in main thread"""

        class TestException(Exception):
            pass

        def create_index():

            def gen():
                for i in range(10):
                    yield (
                     i, (1, 2, 3, 4), None)

                raise TestException('raising here')

            return index.Index(gen())

        self.assertRaises(TestException, create_index)