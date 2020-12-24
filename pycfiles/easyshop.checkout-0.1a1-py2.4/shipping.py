# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/checkout/browser/shipping.py
# Compiled at: 2008-06-20 09:35:17
from zope import schema
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements
from zope.interface import Interface
from Products.Five.browser import pagetemplatefile
from Products.Five.formlib import formbase
from Products.CMFPlone.utils import safe_unicode
from easyshop.core.config import _
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShippingMethodManagement
from easyshop.core.interfaces import IShop

class IShippingSelectForm(Interface):
    """
    """
    __module__ = __name__
    shipping_method = schema.TextLine()


class ShopShippingSelectForm:
    """
    """
    __module__ = __name__
    implements(IShippingSelectForm)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context

    shipping_method = ''


class ShippingSelectForm(formbase.EditForm):
    """
    """
    __module__ = __name__
    template = pagetemplatefile.ZopeTwoPageTemplateFile('shipping.pt')
    form_fields = form.Fields(IShippingSelectForm)

    @form.action(_('label_next', default='Next'), condition=form.haveInputWidgets, name='next')
    def handle_next_action(self, action, data):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        customer.selected_shipping_method = data.get('shipping_method', '')
        ICheckoutManagement(self.context).redirectToNextURL('SELECTED_SHIPPING_METHOD')

    def getShippingMethods(self):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        selected_shipping_id = customer.selected_shipping_method
        sm = IShippingMethodManagement(self.context)
        shipping_methods = []
        for shipping in sm.getShippingMethods():
            if selected_shipping_id == safe_unicode(shipping.getId()):
                checked = True
            elif selected_shipping_id == '' and shipping.getId() == 'standard':
                checked = True
            else:
                checked = False
            shipping_methods.append({'id': shipping.getId(), 'title': shipping.Title, 'description': shipping.Description, 'checked': checked})

        return shipping_methods