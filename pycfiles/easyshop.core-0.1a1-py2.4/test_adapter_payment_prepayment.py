# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_payment_prepayment.py
# Compiled at: 2008-08-07 12:42:20
from DateTime import DateTime
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IType

class TestPrepaymentType(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def testGetType(self):
        """
        """
        cod = self.shop.paymentmethods['prepayment']
        self.assertEqual(IType(cod).getType(), 'generic-payment')


class TestPrepaymentCompleteness(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def testIsComplete(self):
        """
        """
        cod = self.shop.paymentmethods['prepayment']
        self.assertEqual(ICompleteness(cod).isComplete(), True)


class TestPrepaymentPaymentProcessor(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def testProcess(self):
        """
        """
        pm = self.shop.paymentmethods['prepayment']
        result = IPaymentProcessing(pm).process()
        self.assertEqual(result.code, 'NOT_PAYED')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPrepaymentType))
    suite.addTest(makeSuite(TestPrepaymentCompleteness))
    suite.addTest(makeSuite(TestPrepaymentPaymentProcessor))
    return suite