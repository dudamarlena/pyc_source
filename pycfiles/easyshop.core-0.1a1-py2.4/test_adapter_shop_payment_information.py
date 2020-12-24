# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_shop_payment_information.py
# Compiled at: 2008-06-20 09:37:19
from base import EasyShopTestCase
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IPaymentInformationManagement

class TestPaymentInformationManagement(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestPaymentInformationManagement, self).afterSetUp()
        self.shop.customers.invokeFactory('Customer', 'customer')
        self.customer = self.shop.customers.customer
        self.customer.at_post_create_script()

    def testGetSelectedPaymentMethod_1(self):
        """Customer has selected prepayment by default.
        """
        pm = IPaymentInformationManagement(self.customer)
        result = pm.getSelectedPaymentMethod().getId()
        self.assertEqual(result, 'prepayment')

    def testGetSelectedPaymentMethod_2(self):
        """Customer has selected paypal.
        """
        self.customer.selected_payment_method = 'paypal'
        pm = IPaymentInformationManagement(self.customer)
        result = pm.getSelectedPaymentMethod().getId()
        self.assertEqual(result, 'paypal')

    def testGetSelectedPaymentMethod_3(self):
        """Customer has selected a non existing. Returns default, which is 
        prepayment atm.
        """
        self.customer.selected_payment_method = 'dummy'
        pm = IPaymentInformationManagement(self.customer)
        result = pm.getSelectedPaymentMethod().getId()
        self.assertEqual(result, 'prepayment')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPaymentInformationManagement))
    return suite