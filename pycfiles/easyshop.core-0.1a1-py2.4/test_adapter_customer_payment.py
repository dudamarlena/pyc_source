# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_customer_payment.py
# Compiled at: 2008-06-20 09:37:19
from base import EasyShopTestCase
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
        self.customer.invokeFactory('BankAccount', id='bank-account')

    def testDeletePaymentInformations(self):
        """
        """
        pm = IPaymentInformationManagement(self.customer)
        ids = [ p.getId() for p in pm.getPaymentInformations() ]
        self.assertEqual(['bank-account'], ids)
        result = pm.deletePaymentInformation('paypal')
        self.assertEqual(result, False)
        result = pm.deletePaymentInformation('prepayment')
        self.assertEqual(result, False)
        ids = [ p.getId() for p in pm.getPaymentInformations() ]
        self.assertEqual(['bank-account'], ids)
        result = pm.deletePaymentInformation('bank-account')
        self.assertEqual(result, True)
        ids = [ p.getId() for p in pm.getPaymentInformations() ]
        self.assertEqual([], ids)

    def testGetPaymentInformations(self):
        """Get all payment methods (without parameter)
        """
        pm = IPaymentInformationManagement(self.customer)
        ids = [ p.getId() for p in pm.getPaymentInformations() ]
        self.assertEqual(['bank-account'], ids)

    def testGetSelectedPaymentMethod(self):
        """
        """
        pm = IPaymentInformationManagement(self.customer)
        result = pm.getSelectedPaymentMethod().getId()
        self.assertEqual(result, 'prepayment')

    def testGetSelectedPaymentInformation(self):
        """
        """
        pm = IPaymentInformationManagement(self.customer)
        result = pm.getSelectedPaymentInformation()
        self.failUnless(result is None)
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPaymentInformationManagement))
    return suite