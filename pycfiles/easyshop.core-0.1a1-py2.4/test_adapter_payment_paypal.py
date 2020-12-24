# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_payment_paypal.py
# Compiled at: 2008-08-07 12:42:20
from DateTime import DateTime
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IType

class TestPayPalType(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def testGetType(self):
        """
        """
        cod = self.shop.paymentmethods['paypal']
        self.assertEqual(IType(cod).getType(), 'paypal')


class TestPayPalCompleteness(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def testIsComplete(self):
        """
        """
        cod = self.shop.paymentmethods['paypal']
        self.assertEqual(ICompleteness(cod).isComplete(), True)


class TestPayPalPaymentProcessor(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def testProcess(self):
        """
        """
        pass


class TestPayPalValidity(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def testValidity(self):
        """
        """
        self.shop.setPayPalId('')
        paypal = self.shop.paymentmethods.paypal
        result = IValidity(paypal).isValid()
        self.failUnless(result == False)
        self.shop.setPayPalId('john@doe.com')
        result = IValidity(paypal).isValid()
        self.failUnless(result == True)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPayPalType))
    suite.addTest(makeSuite(TestPayPalCompleteness))
    suite.addTest(makeSuite(TestPayPalValidity))
    return suite