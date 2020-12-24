# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_shop_product.py
# Compiled at: 2008-08-07 12:42:20
from DateTime import DateTime
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IProductManagement

class TestShopProductManagement(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def testGetAllProducts(self):
        """
        """
        pm = IProductManagement(self.shop)
        self.assertRaises(Exception, pm.getAllProducts)

    def testGetAmountOfProducts(self):
        """
        """
        pm = IProductManagement(self.shop)
        self.assertRaises(Exception, pm.getAmountOfProducts)

    def testGetProducts(self):
        """
        """
        pm = IProductManagement(self.shop)
        self.failIf(pm.getProducts() == 0)

    def testGetTotalAmountOfProducts(self):
        """
        """
        pm = IProductManagement(self.shop)
        self.assertRaises(Exception, pm.getTotalAmountOfProducts)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShopProductManagement))
    return suite