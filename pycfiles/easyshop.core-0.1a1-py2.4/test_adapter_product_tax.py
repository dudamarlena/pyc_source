# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_product_tax.py
# Compiled at: 2008-08-07 12:42:20
from DateTime import DateTime
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ITaxes

class TestProductTaxCalculation(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestProductTaxCalculation, self).afterSetUp()
        self.shop.taxes.invokeFactory('CustomerTax', id='customer', rate=10.0)

    def testGetTaxRate(self):
        """
        """
        t = ITaxes(self.shop.products.product_1)
        self.assertEqual(t.getTaxRate(), 19.0)

    def testGetTaxRateForCustomer(self):
        """
        """
        t = ITaxes(self.shop.products.product_1)
        self.assertEqual(t.getTaxRateForCustomer(), 10.0)

    def testGetTax(self):
        """
        """
        t = ITaxes(self.shop.products.product_1)
        self.assertEqual('%.2f' % t.getTax(), '3.51')

    def testGetTaxForCustomer(self):
        """
        """
        t = ITaxes(self.shop.products.product_1)
        self.assertEqual('%.2f' % t.getTaxForCustomer(), '1.85')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductTaxCalculation))
    return suite