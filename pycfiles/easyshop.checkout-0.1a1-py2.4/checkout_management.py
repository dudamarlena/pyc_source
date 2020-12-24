# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/checkout/adapters/checkout_management.py
# Compiled at: 2008-06-20 09:35:16
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShop
METHODS = {'AFTER_START': '_gotoAddresses', 'AFTER_ADDED_USER': '_gotoAddresses', 'ADDED_ADDRESS': '_addedAddress', 'EDITED_ADDRESS': '_editedAddress', 'SELECTED_ADDRESSES': '_selectedAddresses', 'SELECTED_SHIPPING_METHOD': '_selectedShipping', 'SELECTED_PAYMENT_METHOD': '_selectedPayment', 'BUYED_ORDER': '_gotoAfterBuyedOrder', 'ERROR_PAYMENT': '_gotoAfterErrorPayment'}

class CheckoutManagement:
    """
    """
    __module__ = __name__
    implements(ICheckoutManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context

    def getNextURL(self, id):
        """Returns next URL by given id.
        """
        goto = self.context.REQUEST.get('goto', '')
        if goto != '':
            return goto
        else:
            method = METHODS[id]
            method = getattr(self, method)
            return method()

    def redirectToNextURL(self, id):
        """Redirects to next URL by given id.
        """
        next_url = self.getNextURL(id)
        self.context.REQUEST.RESPONSE.redirect(next_url)

    def _addedAddress(self):
        """
        """
        if self.context.REQUEST.get('also_invoice_address', 'yes') == 'yes':
            url = '/checkout-shipping'
        else:
            url = '/checkout-add-address?address_type=invoice'
        return self.context.absolute_url() + url

    def _gotoUser(self):
        """
        """
        return self.context.absolute_url() + '/checkout-add-user'

    def _editedAddress(self):
        """
        """
        if self.context.REQUEST.get('also_invoice_address', 'yes') == 'yes':
            url = self.context.absolute_url() + '/checkout-shipping'
        else:
            customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
            invoice_address = IAddressManagement(customer).getInvoiceAddress()
            if invoice_address is None:
                url = self.context.absolute_url() + '/checkout-add-address?address_type=invoice'
            else:
                url = invoice_address.absolute_url() + '/checkout-edit-address'
        return url

    def _selectedAddresses(self):
        """
        """
        return self.context.absolute_url() + '/checkout-shipping'

    def _selectedShipping(self):
        """
        """
        return self.context.absolute_url() + '/checkout-payment'

    def _selectedPayment(self):
        """
        """
        return self.context.absolute_url() + '/checkout-order-preview'

    def _gotoAddresses(self):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        shipping_address = IAddressManagement(customer).getShippingAddress()
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.isAnonymousUser():
            if shipping_address is None:
                return self.context.absolute_url() + '/checkout-add-address'
            else:
                return shipping_address.absolute_url() + '/checkout-edit-address'
        elif shipping_address is None:
            return self.context.absolute_url() + '/checkout-add-address'
        else:
            return self.context.absolute_url() + '/checkout-select-addresses'
        return

    def _gotoAfterBuyedOrder(self):
        """
        """
        return '%s/thank-you' % self.context.absolute_url()

    def _gotoAfterErrorPayment(self):
        """
        """
        return '%s/checkout-order-preview' % self.context.absolute_url()