# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_shop_stock_management.py
# Compiled at: 2008-06-20 09:37:19
from zope.component import getMultiAdapter
from base import EasyShopTestCase
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IStockManagement

class TestShopStockManagement(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestShopStockManagement, self).afterSetUp()

    def testRemoveCart(self):
        """
        """
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name='addToCart')
        view.addToCart()
        view.addToCart()
        view = getMultiAdapter((self.shop.products.product_2, self.shop.products.product_2.REQUEST), name='addToCart')
        view.addToCart()
        cart = ICartManagement(self.shop).getCart()
        sm = IStockManagement(self.shop)
        sm.removeCart(cart)
        self.assertEqual(self.shop.products.product_1.getStockAmount(), 8.0)
        self.assertEqual(self.shop.products.product_2.getStockAmount(), 19.0)

    def testGetStockInformations(self):
        """
        """
        container = self.shop['stock-information']
        container.invokeFactory('StockInformation', id='s1')
        container.invokeFactory('StockInformation', id='s2')
        container.invokeFactory('StockInformation', id='s3')
        sm = IStockManagement(self.shop)
        ids = [ s.getId() for s in sm.getStockInformations() ]
        self.assertEqual(ids, ['s1', 's2', 's3'])

    def testgetStockInformationFor_1(self):
        """
        """
        container = self.shop['stock-information']
        container.invokeFactory('StockInformation', id='s1')
        sm = IStockManagement(self.shop)
        valid_stock_information = sm.getStockInformationFor(self.shop.products.product_1)
        self.assertEqual(valid_stock_information.getId(), 's1')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShopStockManagement))
    return suite