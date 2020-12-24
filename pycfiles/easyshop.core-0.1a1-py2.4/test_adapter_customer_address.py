# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_customer_address.py
# Compiled at: 2008-08-07 12:42:20
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IAddressManagement

class TestAddressManagementWithoutAddresses(EasyShopTestCase):
    """Tests IAddressManagement, when no address is added yet.
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestAddressManagementWithoutAddresses, self).afterSetUp()
        self.shop.customers.invokeFactory('Customer', 'customer')
        self.customer = self.shop.customers.customer
        self.customer.at_post_create_script()

    def testGetAddresses(self):
        """
        """
        am = IAddressManagement(self.customer)
        self.assertEqual([], am.getAddresses())

    def testGetInvoiceAddress(self):
        """
        """
        am = IAddressManagement(self.customer)
        self.assertEqual(am.getInvoiceAddress(), None)
        return

    def testGetShippingAddress(self):
        """
        """
        am = IAddressManagement(self.customer)
        self.assertEqual(am.getShippingAddress(), None)
        return

    def testDeleteAddress(self):
        """
        """
        am = IAddressManagement(self.customer)
        result = am.deleteAddress('address_1')
        self.assertEqual(result, False)


class TestAddressManagement(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestAddressManagement, self).afterSetUp()
        self.setRoles(('Manager', ))
        self.shop.customers.invokeFactory('Customer', 'customer')
        self.customer = self.shop.customers.customer
        self.customer.invokeFactory('Address', 'address_1')
        self.address_1 = self.customer.address_1
        self.customer.invokeFactory('Address', 'address_2')
        self.address_2 = self.customer.address_2
        self.customer.invokeFactory('Address', 'address_3')
        self.address_3 = self.customer.address_3
        self.customer.selected_invoice_address = 'address_1'
        self.customer.selected_shipping_address = 'address_2'

    def testGetAddresses(self):
        """
        """
        am = IAddressManagement(self.customer)
        ids = [ a.getId() for a in am.getAddresses() ]
        self.assertEqual(ids, ['address_1', 'address_2', 'address_3'])

    def testGetInvoiceAddress(self):
        """
        """
        am = IAddressManagement(self.customer)
        self.assertEqual(am.getInvoiceAddress().getId(), 'address_1')

    def testGetShippingAddress(self):
        """
        """
        am = IAddressManagement(self.customer)
        self.assertEqual(am.getShippingAddress().getId(), 'address_2')

    def testDeleteAddress(self):
        """
        """
        am = IAddressManagement(self.customer)
        am.deleteAddress('address_1')
        ids = [ a.getId() for a in am.getAddresses() ]
        self.assertEqual(ids, ['address_2', 'address_3'])
        am.deleteAddress('address_2')
        ids = [ a.getId() for a in am.getAddresses() ]
        self.assertEqual(ids, ['address_3'])
        am.deleteAddress('address_3')
        ids = [ a.getId() for a in am.getAddresses() ]
        self.assertEqual(ids, [])

    def testAddAddress(self):
        """
        """
        am = IAddressManagement(self.customer)
        id = am.addAddress({'firstname': 'John', 'lastname': 'Doe', 'address_1': 'Doe Str. 1', 'zip_code': '4711', 'city': 'Doe City', 'country': 'Germany'})
        ids = [ a.getId() for a in am.getAddresses() ]
        self.assertEqual(ids, ['address_1', 'address_2', 'address_3', id])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestAddressManagement))
    suite.addTest(makeSuite(TestAddressManagementWithoutAddresses))
    return suite