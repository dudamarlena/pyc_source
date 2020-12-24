# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_product_price.py
# Compiled at: 2008-08-07 12:42:20
from DateTime import DateTime
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IPrices

class TestProductPriceCalculation_1(EasyShopTestCase):
    """Customer has same tax rate as default
    """
    __module__ = __name__

    def testGetPriceForCustomer(self):
        """Customer has same tax rate as default
        """
        p = IPrices(self.shop.products.product_1)
        self.assertEqual('%.2f' % p.getPriceForCustomer(), '22.00')

    def testGetPriceNet(self):
        """
        """
        p = IPrices(self.shop.products.product_1)
        self.assertEqual('%.2f' % p.getPriceNet(), '18.49')

    def testGetPriceGross(self):
        """
        """
        p = IPrices(self.shop.products.product_1)
        self.assertEqual(p.getPriceGross(), 22.0)


class TestProductPriceCalculation_2(EasyShopTestCase):
    """Customer has other tax rate than default
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestProductPriceCalculation_2, self).afterSetUp()
        self.shop.taxes.invokeFactory('CustomerTax', id='customer', rate=10.0)

    def testGetPriceForCustomer(self):
        """
        """
        p = IPrices(self.shop.products.product_1)
        self.assertEqual('%.2f' % p.getPriceForCustomer(), '20.34')

    def testGetPriceNet(self):
        """
        """
        p = IPrices(self.shop.products.product_1)
        self.assertEqual('%.2f' % p.getPriceNet(), '18.49')

    def testGetPriceGross(self):
        """
        """
        p = IPrices(self.shop.products.product_1)
        self.assertEqual(p.getPriceGross(), 22.0)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductPriceCalculation_1))
    suite.addTest(makeSuite(TestProductPriceCalculation_2))
    return suite