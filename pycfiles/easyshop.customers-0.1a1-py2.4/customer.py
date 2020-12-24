# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/customers/content/customer.py
# Compiled at: 2008-09-03 11:14:43
from zope.component.factory import Factory
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from plone.app.content.container import Container
from easyshop.core.config import _
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICustomer
from OFS.OrderSupport import OrderSupport

class Customer(OrderSupport, Container):
    """A customer can buy products from a shop. A customer has addresses and 
    payment methods.

    A customer exists additionally to the members of Plone. Whenever a member 
    wants to buy something a customer content object is added for this member. 
    This is intended to be changed to "remember" in future.
    """
    __module__ = __name__
    implements(ICustomer)
    portal_type = 'Customer'
    firstname = FieldProperty(ICustomer['firstname'])
    lastname = FieldProperty(ICustomer['lastname'])
    email = FieldProperty(ICustomer['email'])
    selected_invoice_address = ''
    selected_shipping_address = ''
    selected_payment_method = 'prepayment'
    selected_payment_information = ''
    selected_shipping_method = 'standard'
    selected_country = ''

    def __init__(self, id):
        """
        """
        super(Customer, self).__init__(id)
        self.selected_country = 'Deutschland'

    def Title(self):
        """
        """
        if self.firstname and self.lastname:
            return self.firstname + ' ' + self.lastname
        else:
            return self.getId()

    def SearchableText(self):
        """
        """
        text = []
        text.append(self.firstname)
        text.append(self.lastname)
        text.append(self.email)
        am = IAddressManagement(self)
        for address in am.getAddresses():
            if address.firstname:
                text.append(address.firstname)
            if address.lastname:
                text.append(address.lastname)
            if address.address_1:
                text.append(address.address_1)
            if address.zip_code:
                text.append(address.zip_code)
            if address.city:
                text.append(address.city)
            if address.country:
                text.append(address.country)

        return (' ').join(text)


customerFactory = Factory(Customer, title=_('Create a new customer'))