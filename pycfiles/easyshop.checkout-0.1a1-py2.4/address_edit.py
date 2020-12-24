# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/checkout/browser/address_edit.py
# Compiled at: 2008-06-20 09:35:17
from zope.event import notify
from zope.formlib import form
from zope.lifecycleevent import ObjectModifiedEvent
from Products.Five.browser import pagetemplatefile
from plone.app.form import base
from plone.app.form.events import EditCancelledEvent
from plone.app.form.events import EditSavedEvent
from easyshop.core.config import _
from easyshop.core.interfaces import IAddress
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import IShopManagement

class AddressEditForm(base.EditForm):
    """This form let anonymous users edit their already entered invoice and 
    shipping address. This happens when they click checkout again and they have 
    already entered addresses within the same sessions. 
    """
    __module__ = __name__
    template = pagetemplatefile.ZopeTwoPageTemplateFile('address_form.pt')
    form_fields = form.Fields(IAddress)
    label = _('Edit Address')
    description = _('To change your address edit the form and press save.')
    form_name = _('Edit Address')

    @form.action(_('label_save', default='Save'), condition=form.haveInputWidgets, name='save')
    def handle_save_action(self, action, data):
        """
        """
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            notify(ObjectModifiedEvent(self.context))
            notify(EditSavedEvent(self.context))
            self.status = 'Changes saved'
        else:
            notify(EditCancelledEvent(self.context))
            self.status = 'No changes'
        shop = IShopManagement(self.context).getShop()
        ICheckoutManagement(shop).redirectToNextURL('EDITED_ADDRESS')

    def getAddressType(self):
        """
        """
        return self.request.get('address_type', 'shipping')

    def isShippingAddress(self):
        """
        """
        return self.getAddressType() == 'shipping'