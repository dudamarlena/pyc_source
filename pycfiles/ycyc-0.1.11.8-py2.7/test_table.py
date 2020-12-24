# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/tests/ycollections/test_table.py
# Compiled at: 2016-07-19 10:55:32
from unittest import TestCase
from ycyc.ycollections import table

class TestSimpleTable(TestCase):

    def test_usage(self):
        tb = table.simple_table(3, 4, lambda x, y: x * 10 + y)
        self.assertListEqual(tb[0], [0, 1, 2, 3])
        self.assertListEqual(tb[1], [10, 11, 12, 13])
        self.assertListEqual(tb[2], [20, 21, 22, 23])


class TestTable(TestCase):

    def test_usage(self):
        tb = table.Table(3, 4, 0)
        self.assertEqual(len(tb.table), 3)
        self.assertEqual(len(tb.table[0]), 4)
        self.assertEqual(tb[(1, 2)], 0)
        tb[(1, 2)] = 1
        self.assertEqual(tb[(1, 2)], 1)


class TestSparseTable(TestCase):

    def test_usage(self):
        tb = table.SparseTable(3, 4, 0)
        self.assertEqual(tb[(1, 2)], 0)
        tb[(1, 2)] = 1
        self.assertEqual(tb[(1, 2)], 1)