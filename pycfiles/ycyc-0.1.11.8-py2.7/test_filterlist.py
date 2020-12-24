# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/tests/ycollections/test_filterlist.py
# Compiled at: 2016-07-19 10:55:32
from unittest import TestCase
from ycyc.ycollections import filterlist

class TestFilterList(TestCase):

    def test_usage(self):
        list1 = filterlist.FilterList(range(5))
        list2 = list1.filter(lambda x: x % 2)
        list3 = list1.exclude(lambda x: x % 2)
        self.assertIsInstance(list2, filterlist.FilterList)
        self.assertIsInstance(list3, filterlist.FilterList)
        self.assertEqual(list(list2), [1, 3])
        self.assertEqual(list(list3), [0, 2, 4])
        self.assertEqual(list1.first(), 0)
        self.assertEqual(list1.last(), 4)
        list1.clear()
        self.assertEqual(list1.first(), None)
        self.assertEqual(list1.last(), None)
        self.assertEqual(list1.first(0), 0)
        self.assertEqual(list1.last(0), 0)
        return