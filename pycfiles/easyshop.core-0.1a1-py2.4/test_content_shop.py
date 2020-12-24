# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_content_shop.py
# Compiled at: 2008-06-20 09:37:19
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import ITaxes

class TestInitialize(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def testContainers(self):
        """
        """
        containers = [
         'carts', 'categories', 'products', 'customers', 'discounts', 'groups', 'information', 'orders', 'paymentmethods', 'paymentprices', 'shippingmethods', 'shippingprices', 'stock-information', 'taxes']
        object_ids = self.shop.objectIds()
        for container in containers:
            self.failUnless(container in object_ids)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInitialize))
    return suite