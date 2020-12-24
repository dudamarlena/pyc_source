# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_generic_shipping.py
# Compiled at: 2008-08-07 12:42:20
from DateTime import DateTime
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IValidity

class TestShippingPriceValidityManager(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestShippingPriceValidityManager, self).afterSetUp()
        self.shop.shippingprices.invokeFactory('ShippingPrice', id='shipping_price')
        self.shipping_price = self.shop.shippingprices.shipping_price

    def testIsValid_1(self):
        """Without criteria
        """
        v = IValidity(self.shipping_price)
        self.assertEqual(v.isValid(), True)

    def testIsValid_2(self):
        """With one invalid criterion.
        """
        self.shipping_price.invokeFactory('PriceCriteria', id='price_criterion')
        self.shipping_price.price_criterion.setPrice(123.0)
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name='addToCart')
        view.addToCart()
        v = IValidity(self.shop.shippingprices.shipping_price)
        self.assertEqual(v.isValid(), False)

    def testIsValid_3(self):
        """With one valid criterion.
        """
        self.shipping_price.invokeFactory('PriceCriteria', id='price_criterion')
        self.shipping_price.price_criterion.setPrice(21.0)
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name='addToCart')
        view.addToCart()
        v = IValidity(self.shop.shippingprices.shipping_price)
        self.assertEqual(v.isValid(), True)

    def testIsValid_4(self):
        """With one invalid and one valid criterion.
        """
        self.shipping_price.invokeFactory('PriceCriteria', id='price_criterion')
        self.shipping_price.price_criterion.setPrice(23.0)
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name='addToCart')
        view.addToCart()
        self.shipping_price.invokeFactory('DateCriteria', id='date_criterion')
        start = end = DateTime() + 1
        self.shipping_price.date_criterion.setStart(start)
        self.shipping_price.date_criterion.setStart(end)
        v = IValidity(self.shop.shippingprices.shipping_price)
        self.assertEqual(v.isValid(), False)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShippingPriceValidityManager))
    return suite