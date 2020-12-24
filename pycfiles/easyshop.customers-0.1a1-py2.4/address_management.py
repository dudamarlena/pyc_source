# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/customers/adapters/address_management.py
# Compiled at: 2008-09-03 11:14:43
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.exceptions import BadRequest
from Products.Archetypes.utils import shasattr
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICustomer
from easyshop.customers.content.address import Address

class CustomerAddressManager:
    """An adapter which provides address management for customers.
    """
    __module__ = __name__
    implements(IAddressManagement)
    adapts(ICustomer)

    def __init__(self, context):
        self.context = context

    def addAddress(self, data):
        """
        """
        id = self.context.generateUniqueId('Address')
        address = Address(id)
        address.firstname = data.get('firstname', '')
        address.lastname = data.get('lastname', '')
        address.company_name = data.get('company_name', '')
        address.address_1 = data.get('address_1', '')
        address.zip_code = data.get('zip_code', '')
        address.city = data.get('city', '')
        address.country = data.get('country', '')
        address.phone = data.get('phone', '')
        address.email = data.get('email', '')
        self.context._setObject(id, address)
        if data.get('address_type', '') == 'shipping':
            self.context.selected_shipping_address = id
        else:
            self.context.selected_invoice_address = id
        return id

    def deleteAddress(self, id):
        """
        """
        try:
            self.context.manage_delObjects(id)
        except BadRequest:
            return False

        return True

    def getAddress(self, id):
        """
        """
        return getattr(self.context, id, None)

    def getAddresses(self):
        """
        """
        return self.context.objectValues('Address')

    def getInvoiceAddress(self):
        """
        """
        if shasattr(self.context, self.context.selected_invoice_address):
            return getattr(self.context, self.context.selected_invoice_address)
        try:
            return self.getAddresses()[0]
        except IndexError:
            return

        return

    def getShippingAddress(self):
        """
        """
        if shasattr(self.context, self.context.selected_shipping_address):
            return getattr(self.context, self.context.selected_shipping_address)
        try:
            return self.getAddresses()[0]
        except IndexError:
            return

        return

    def hasAddresses(self):
        """
        """
        return len(self.getAddresses()) > 0

    def hasInvoiceAddress(self):
        """
        """
        if shasattr(self.context, self.context.selected_invoice_address):
            return True
        else:
            return False

    def hasShippingAddress(self):
        """
        """
        if shasattr(self.context, self.context.selected_shipping_address):
            return True
        else:
            return False