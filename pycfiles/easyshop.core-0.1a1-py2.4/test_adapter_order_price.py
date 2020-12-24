# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_order_price.py
# Compiled at: 2008-08-07 12:42:20
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IPrices

class TestOrderPriceCalculation(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestOrderPriceCalculation, self).afterSetUp()
        self.login('newmember')
        utils.createTestOrder(self)

    def testGetPriceNet(self):
        """
        """
        p = IPrices(self.order)
        self.assertEqual('%.2f' % p.getPriceNet(), '126.89')

    def testGetPriceGross(self):
        """
        """
        p = IPrices(self.order)
        self.assertEqual('%.2f' % p.getPriceGross(), '151.00')

    def testGetPriceForCustomer(self):
        """
        """
        p = IPrices(self.order)
        self.assertEqual('%.2f' % p.getPriceForCustomer(), '151.00')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestOrderPriceCalculation))
    return suite