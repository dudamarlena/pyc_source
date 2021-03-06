# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_shop_customer.py
# Compiled at: 2008-08-07 12:42:20
from DateTime import DateTime
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import ICustomer

class TestCustomerManagement(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestCustomerManagement, self).afterSetUp()
        self.cm = ICustomerManagement(self.shop)

    def testAddCustomers(self):
        """
        """
        result = self.cm.addCustomer('c1')
        self.failIf(result == False)
        result = self.cm.addCustomer('c2')
        self.failIf(result == False)
        result = self.cm.addCustomer('c3')
        self.failIf(result == False)
        result = self.cm.addCustomer('c4')
        self.failIf(result == False)
        ids = [ c.getId for c in self.cm.getCustomers() ]
        self.assertEqual(ids, ['c1', 'c2', 'c3', 'c4'])

    def testGetAuthenticatedCustomer_1(self):
        """As anonymous, returns standard customer
        """
        self.logout()
        customer = self.cm.getAuthenticatedCustomer()
        self.assertEqual(customer.getId(), 'DUMMY_SESSION')

    def testGetAuthenticatedCustomer_2(self):
        """As member
        """
        self.login('newmember')
        customer = self.cm.getAuthenticatedCustomer()
        self.failUnless(ICustomer.providedBy(customer))
        self.assertEqual(customer.getId(), 'newmember')

    def testGetCustomerById_1(self):
        """Existing customer
        """
        result = self.cm.addCustomer('c1')
        self.failIf(result == False)
        customer = self.cm.getCustomerById('c1')
        self.assertEqual(customer.getId(), 'c1')
        self.failUnless(ICustomer.providedBy(customer))

    def testGetCustomerById_2(self):
        """Non-existing customer
        """
        customer = self.cm.getCustomerById('doe')
        self.assertEqual(customer, None)
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCustomerManagement))
    return suite