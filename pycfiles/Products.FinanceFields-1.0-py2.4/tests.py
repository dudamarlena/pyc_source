# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/FinanceFields/tests.py
# Compiled at: 2010-03-10 14:21:02
from unittest import TestCase
from Products.FinanceFields.Money import parseString
from Products.FinanceFields.Money import parseString
from Products.FinanceFields.fixedpoint import FixedPoint
from Products.FinanceFields.Currency import CURRENCIES

class TestMoney(TestCase):
    __module__ = __name__

    def test_parseString(self):
        s = '1000.00'
        self.assertEqual(parseString(s), (
         None, FixedPoint('1000.00')))
        s = 'R 1000.00'
        self.assertEqual(parseString(s), (
         CURRENCIES['ZAR'], FixedPoint('1000.00')))
        s = '(R 1000.00)'
        self.assertEqual(parseString(s), (
         CURRENCIES['ZAR'], FixedPoint('-1000.00')))
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMoney))
    return suite