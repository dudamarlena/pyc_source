# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/geo/tests/util_test.py
# Compiled at: 2009-08-31 03:57:25
"""Unit tests for util.py."""
__author__ = 'api.roman.public@gmail.com (Roman Nurik)'
import unittest
from geo import util

class MergeInPlaceTests(unittest.TestCase):

    def test_merge_in_place(self):
        self.assertEquals([], util.merge_in_place())
        list1 = [
         0, 1, 5, 6, 8, 9, 15]
        list2 = [0, 2, 3, 5, 8, 10, 11, 17]
        list3 = [1, 4, 6, 8, 10, 15, 16]
        list4 = [-1, 19]
        list5 = [20]
        list6 = []
        util.merge_in_place(list1, list2, list3, list4, list5, list6, dup_fn=lambda x, y: x == y)
        self.assertEquals([
         -1, 0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 15, 16, 17, 19, 20], list1)


if __name__ == '__main__':
    unittest.main()