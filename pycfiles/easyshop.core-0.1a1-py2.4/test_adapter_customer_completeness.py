# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_customer_completeness.py
# Compiled at: 2008-08-07 12:42:20
from zope.component import getMultiAdapter
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICompleteness

class TestCustomerCompleteness(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestCustomerCompleteness, self).afterSetUp()
        self.shop.customers.invokeFactory('Customer', 'customer')
        self.customer = self.shop.customers.customer
        self.customer.at_post_create_script()

    def testIsComplete(self):
        """
        """
        c = ICompleteness(self.shop.customers.customer)
        self.assertEqual(c.isComplete(), False)
        am = IAddressManagement(self.customer)
        id = am.addAddress({'firstname': 'John', 'lastname': 'Doe', 'address_1': 'Doe Str. 1', 'zip_code': '4711', 'city': 'Doe City', 'country': 'Germany'})
        self.customer.selected_invoice_address = id
        self.customer.selected_shipping_address = id
        self.assertEqual(c.isComplete(), False)
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name='addToCart')
        view.addToCart()
        self.assertEqual(c.isComplete(), True)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCustomerCompleteness))
    return suite