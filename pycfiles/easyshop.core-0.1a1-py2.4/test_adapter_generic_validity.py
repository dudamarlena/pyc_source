# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_generic_validity.py
# Compiled at: 2008-06-20 09:37:19
from base import EasyShopTestCase
from easyshop.core.interfaces import IValidity
from easyshop.payment.content import BankAccount
from easyshop.taxes.content import CustomerTax
from easyshop.taxes.content import DefaultTax
from easyshop.payment.content import PaymentPrice
from easyshop.payment.content import GenericPaymentMethod
from easyshop.shipping.content import ShippingPrice

class TestValidityAdapters(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def testAdapters(self):
        """
        """
        adapter = IValidity(BankAccount('dummy'))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.validity.Validity'>")
        adapter = IValidity(GenericPaymentMethod('dummy'))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.validity.Validity'>")
        adapter = IValidity(PaymentPrice('dummy'))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.validity.Validity'>")
        adapter = IValidity(CustomerTax('dummy'))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.validity.Validity'>")
        adapter = IValidity(DefaultTax('dummy'))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.validity.Validity'>")
        adapter = IValidity(ShippingPrice('dummy'))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.validity.Validity'>")


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestValidityAdapters))
    return suite