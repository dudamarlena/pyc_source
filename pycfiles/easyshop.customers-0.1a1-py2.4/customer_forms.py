# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/customers/browser/customer_forms.py
# Compiled at: 2008-09-03 11:14:43
from zope.formlib import form
import zope.event, zope.lifecycleevent
from Products.Five.browser import pagetemplatefile
from Products.CMFCore.utils import getToolByName
from plone.app.form import base
from plone.app.form.validators import null_validator
from plone.app.form.events import EditCancelledEvent, EditSavedEvent
from easyshop.core.config import _
from easyshop.core.config import DEFAULT_SHOP_FORM
from easyshop.core.interfaces import ICustomer
from easyshop.core.interfaces import IShopManagement

class CustomerEditForm(base.EditForm):
    """
    """
    __module__ = __name__
    template = pagetemplatefile.ZopeTwoPageTemplateFile(DEFAULT_SHOP_FORM)
    form_fields = form.Fields(ICustomer)
    label = _('Edit Customer')
    description = _('Please edit the form below and press save.')
    form_name = _('Edit Customer')

    @form.action(_('label_save', default='Save'), condition=form.haveInputWidgets, name='save')
    def handle_save_action(self, action, data):
        """
        """
        utils = getToolByName(self.context, 'plone_utils')
        utils.addPortalMessage(_('Changes saved'), 'info')
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            zope.event.notify(zope.lifecycleevent.ObjectModifiedEvent(self.context))
            zope.event.notify(EditSavedEvent(self.context))
        else:
            zope.event.notify(EditCancelledEvent(self.context))
        self.context.reindexObject()
        self._nextUrl()

    @form.action(_('label_cancel', default='Cancel'), validator=null_validator, name='cancel')
    def handle_cancel_action(self, action, data):
        """
        """
        utils = getToolByName(self.context, 'plone_utils')
        utils.addPortalMessage(_('Edit canceled'), 'info')
        zope.event.notify(EditCancelledEvent(self.context))
        self._nextUrl()

    def _nextUrl(self):
        """
        """
        url = self.request.get('goto', '')
        if url != '':
            self.request.response.redirect(url)
        else:
            url = self.context.absolute_url()
            url += '/my-account'
            self.request.response.redirect(url)