# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/checkout/browser/address_add.py
# Compiled at: 2008-06-20 09:35:17
from zope.formlib import form
from Products.Five.browser import pagetemplatefile
from plone.app.form import base
from easyshop.core.config import _
from easyshop.core.interfaces import IAddress
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import ICustomerManagement

class AddressAddForm(base.AddForm):
    """
    """
    __module__ = __name__
    template = pagetemplatefile.ZopeTwoPageTemplateFile('address_form.pt')
    form_fields = form.Fields(IAddress)
    label = _('Add Address')
    form_name = _('Add Address')

    @form.action(_('label_next', default='Next'), condition=form.haveInputWidgets, name='next')
    def handle_next_action(self, action, data):
        """
        """
        self.createAndAdd(data)
        ICheckoutManagement(self.context).redirectToNextURL('ADDED_ADDRESS')

    def createAndAdd(self, data):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        am = IAddressManagement(customer)
        if len(customer.firstname) == 0:
            customer.firstname = data.get('firstname')
            customer.lastname = data.get('lastname')
        if len(customer.email) == 0:
            customer.email = data.get('email', '')
        am.addAddress(data)

    def getAddressType(self):
        """
        """
        return self.request.get('address_type', 'shipping')

    def isShippingAddress(self):
        """
        """
        return self.getAddressType() == 'shipping'