# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/customers/browser/address_forms.py
# Compiled at: 2008-09-03 11:14:43
from zope.formlib import form
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from Products.Five.browser import pagetemplatefile
from plone.app.form import base
from plone.app.form.validators import null_validator
from plone.app.form.events import EditCancelledEvent
from plone.app.form.events import EditSavedEvent
from easyshop.core.config import _
from easyshop.core.config import DEFAULT_SHOP_FORM
from easyshop.core.interfaces import IAddress
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICustomerManagement

class AddressEditForm(base.EditForm):
    """
    """
    __module__ = __name__
    template = pagetemplatefile.ZopeTwoPageTemplateFile(DEFAULT_SHOP_FORM)
    form_fields = form.Fields(IAddress).omit('email')
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
        self.context.reindexObject()
        self.context.aq_inner.aq_parent.reindexObject()
        self.redirectToNextURL()

    @form.action(_('label_cancel', default='Cancel'), validator=null_validator, name='cancel')
    def handle_cancel_action(self, action, data):
        """
        """
        notify(EditCancelledEvent(self.context))
        self.redirectToNextURL()

    def redirectToNextURL(self):
        """
        """
        url = self.request.get('goto', '')
        if url != '':
            self.request.response.redirect(url)
        else:
            customer = self.context.aq_inner.aq_parent
            url = '%s/manage-addressbook' % customer.absolute_url()
            self.request.response.redirect(url)


class AddressAddForm(base.AddForm):
    """
    """
    __module__ = __name__
    template = pagetemplatefile.ZopeTwoPageTemplateFile(DEFAULT_SHOP_FORM)
    form_fields = form.Fields(IAddress).omit('email')
    label = _('Add Address')
    form_name = _('Add Address')

    @form.action(_('label_save', default='Save'), condition=form.haveInputWidgets, name='save')
    def handle_save_action(self, action, data):
        """
        """
        self.createAndAdd(data)

    @form.action(_('label_cancel', default='Cancel'), validator=null_validator, name='cancel')
    def handle_cancel_action(self, action, data):
        """
        """
        self.redirectToNextURL()

    def createAndAdd(self, data):
        """
        """
        am = IAddressManagement(self.context)
        am.addAddress(data)
        self.redirectToNextURL()

    def redirectToNextURL(self):
        """
        """
        url = self.request.get('goto', '')
        if url != '':
            self.request.response.redirect(url)
        else:
            url = '%s/manage-addressbook' % self.context.absolute_url()
            self.request.response.redirect(url)