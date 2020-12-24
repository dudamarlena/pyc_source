# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc_tests/test_iterator.py
# Compiled at: 2018-07-31 10:42:31
import unittest
from summerrpc.helper import Iterator

class TestIterator(unittest.TestCase):

    def testIterator(self):
        lst = range(10)
        it = Iterator(lst)
        removed = []
        while it.has_next():
            ele = it.next()
            if ele % 2 == 0:
                removed.append(it.remove())

        self.assertTrue(lst == range(1, 10, 2))
        self.assertTrue(removed == range(0, 10, 2))