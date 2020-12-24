# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_shop_currency.py
# Compiled at: 2008-08-07 12:42:20
from DateTime import DateTime
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ICurrencyManagement

class TestCurrencyManagementEUR(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestCurrencyManagementEUR, self).afterSetUp()
        self.cm = ICurrencyManagement(self.shop)

    def testGetLongName(self):
        """
        """
        self.assertEqual(self.cm.getLongName(), 'Euro')

    def testGetShortName(self):
        """
        """
        self.assertEqual(self.cm.getShortName(), 'EUR')

    def testGetSymbol(self):
        """
        """
        self.assertEqual(self.cm.getSymbol(), '€')

    def testPriceToString(self):
        """
        """
        price = 42.0
        string = self.cm.priceToString(price)
        self.assertEqual(string, '€ 42,00')
        string = self.cm.priceToString(price, 'short')
        self.assertEqual(string, 'EUR 42,00')
        string = self.cm.priceToString(price, 'long')
        self.assertEqual(string, 'Euro 42,00')
        string = self.cm.priceToString(price, 'long', 'after')
        self.assertEqual(string, '42,00 Euro')


class TestCurrencyManagementUSD(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestCurrencyManagementUSD, self).afterSetUp()
        self.shop.setCurrency('usd')
        self.cm = ICurrencyManagement(self.shop)

    def testGetLongName(self):
        """
        """
        self.assertEqual(self.cm.getLongName(), 'US-Dollar')

    def testGetShortName(self):
        """
        """
        self.assertEqual(self.cm.getShortName(), 'USD')

    def testGetSymbol(self):
        """
        """
        self.assertEqual(self.cm.getSymbol(), '$')

    def testPriceToString(self):
        """
        """
        price = 42.0
        string = self.cm.priceToString(price)
        self.assertEqual(string, '$ 42,00')
        string = self.cm.priceToString(price, 'short')
        self.assertEqual(string, 'USD 42,00')
        string = self.cm.priceToString(price, 'long')
        self.assertEqual(string, 'US-Dollar 42,00')
        string = self.cm.priceToString(price, 'long', 'after')
        self.assertEqual(string, '42,00 US-Dollar')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCurrencyManagementEUR))
    suite.addTest(makeSuite(TestCurrencyManagementUSD))
    return suite