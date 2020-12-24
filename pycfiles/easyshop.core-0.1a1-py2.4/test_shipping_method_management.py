# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_shipping_method_management.py
# Compiled at: 2008-06-20 09:37:19
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.interfaces import IShippingMethodManagement

class TestShippingMethodManagement(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def testGetSelectedShippingMethod(self):
        """
        """
        sm = IShippingMethodManagement(self.shop)
        result = sm.getSelectedShippingMethod()
        self.assertEqual(result.getId(), 'standard')

    def testGetShippingMethod_1(self):
        """Requested shipping method exists.
        """
        sm = IShippingMethodManagement(self.shop)
        result = sm.getShippingMethod('standard')
        self.assertEqual(result.getId(), 'standard')

    def testGetShippingMethod_2(self):
        """Requested shipping method doesn't exist.
        """
        sm = IShippingMethodManagement(self.shop)
        result = sm.getShippingMethod('dummy')
        self.failUnless(result is None)
        return

    def testGetShippingMethods(self):
        """
        """
        sm = IShippingMethodManagement(self.shop)
        methods = sm.getShippingMethods()
        ids = [ method.getId() for method in methods ]
        self.assertEqual(ids, ['standard'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShippingMethodManagement))
    return suite