# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/magot/tests/test_refdata.py
# Compiled at: 2006-09-10 17:07:19
"""Unit tests for reference data."""
from unittest import TestCase, makeSuite, TestSuite
import unittest
from magot.refdata import *

class TestMoney(TestCase):
    __module__ = __name__

    def test_money(self):
        a = Money()
        assert a.amount == 0
        self.failUnless(a != 0)
        a = Money.mdl_fromString('100.256')
        b = Money(100.256)
        assert a == b
        self.failUnless(a != 0)
        assert a.amount == Decimal('100.256')


if __name__ == '__main__':
    unittest.main()