# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/aaron/projects/chai/tests/comparator_py2.py
# Compiled at: 2014-12-03 11:42:10
import unittest, sys
from chai.comparators import *

class ComparatorsPy2Test(unittest.TestCase):

    def test_is_a_unicode_test(self):
        if sys.version_info.major > 2:
            return
        comp = IsA(str)
        self.assertTrue(comp.test('foo'))
        self.assertFalse(comp.test('foo'))
        self.assertFalse(comp.test(bytearray('foo')))