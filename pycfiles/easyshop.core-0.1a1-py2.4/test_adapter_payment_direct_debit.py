# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_payment_direct_debit.py
# Compiled at: 2008-06-20 09:37:19
from base import EasyShopTestCase
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IType

class TestDirectDebit(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestDirectDebit, self).afterSetUp()
        self.login('newmember')
        cm = ICustomerManagement(self.shop)
        self.customer = cm.getAuthenticatedCustomer()
        self.customer.invokeFactory('BankAccount', id='bank-account')

    def testGetType(self):
        """
        """
        dd = self.shop.paymentmethods['direct-debit']
        self.assertEqual(IType(dd).getType(), 'direct-debit')

    def testIsComplete(self):
        """
        """
        dd = self.customer['bank-account']
        self.assertEqual(ICompleteness(dd).isComplete(), False)
        dd.account_number = '47114711'
        self.assertEqual(ICompleteness(dd).isComplete(), False)
        dd.bank_identification_code = '50010000'
        self.assertEqual(ICompleteness(dd).isComplete(), False)
        dd.depositor = 'John Doe'
        self.assertEqual(ICompleteness(dd).isComplete(), False)
        dd.bank_name = 'Deutsche Bank'
        self.assertEqual(ICompleteness(dd).isComplete(), True)

    def testProcess(self):
        """
        """
        dd = self.shop.paymentmethods['direct-debit']
        result = IPaymentProcessing(dd).process()
        self.assertEqual(result.code, 'NOT_PAYED')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestDirectDebit))
    return suite