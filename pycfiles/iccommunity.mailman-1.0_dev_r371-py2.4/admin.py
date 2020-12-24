# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/mailman/browser/admin.py
# Compiled at: 2008-10-06 10:31:16
"""
admin setting and preferences
Solo vistas y forms

@author: Juan Pablo Gimenez
@contact: jpg@rcom.com.ar
"""
__author__ = 'Juan Pablo Gimenez <jpg@rcom.com.ar>'
__docformat__ = 'plaintext'
import os
from datetime import datetime
import zope
from zope import component
from zope.component import getUtility
from zope.component import queryUtility
from zope.formlib import form
from zope.app.form.browser import MultiSelectSetWidget
from zope.app.form.browser.itemswidgets import MultiSelectWidget as BaseMultiSelectWidget, DropdownWidget, SelectWidget
from zope.app.form.browser import FileWidget
from Products.CMFCore.utils import getToolByName
try:
    from zope.lifecycleevent import ObjectModifiedEvent
except:
    from zope.app.event.objectevent import ObjectModifiedEvent

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.browser import BrowserView
from Products.Five.formlib import formbase
from iccommunity.mailman import interfaces
from iccommunity.mailman.i18n import _
from iccommunity.core.browser.base import BaseSettingsForm
from zope.app.component.hooks import getSite
from iccommunity.core.browser.widgets import OrderedMultiSelectionWidgetFactory, MultiSelectionWidgetFactory
from iccommunity.mailman.interfaces import IicCommunityMailman

class MailmanPlone(BaseSettingsForm):
    """ Configlet para configurar mailman
        """
    __module__ = __name__
    form_name = _('Mailman')
    form_fields = form.Fields(interfaces.IicCommunityManagementMailman)
    form_fields['available_lists'].custom_widget = MultiSelectionWidgetFactory


class MailmanUserLists(BaseSettingsForm):
    """ Configlet para configurar listas por usuario
        """
    __module__ = __name__
    form_name = _('Listas Mailman del usuario')
    form_fields = form.Fields(interfaces.IicCommunityMailmanUserLists)
    form_fields['subscribed_lists'].custom_widget = MultiSelectionWidgetFactory

    @form.action('Apply', condition=form.haveInputWidgets)
    def handle_edit_action(self, action, data):
        try:
            if form.applyChanges(self.context, self.form_fields, data, self.adapters):
                zope.event.notify(ObjectModifiedEvent(self.context))
                subscribed_lists = data['subscribed_lists']
                mailman = queryUtility(IicCommunityMailman)
                portal_membership = getToolByName(self.context, 'portal_membership')
                context = self.context
                member = portal_membership.getAuthenticatedMember()
                email = member.getProperty('email')
                all_lists = mailman.get_lists()
                real_subscribed_lists = mailman.subscribed_lists(member)
                to_unsubscribe_lists = [ l for l in all_lists if l in real_subscribed_lists if l not in subscribed_lists ]
                to_subscribe_lists = [ l for l in all_lists if l not in real_subscribed_lists if l in subscribed_lists ]
                for l in to_unsubscribe_lists:
                    mailman.unsubscribe_to_list(member, l)
                    for l in to_subscribe_lists:
                        mailman.subscribe_to_list(member, l)

                self.status = _('Updated on ${date_time}', mapping={'date_time': str(datetime.utcnow())})
            else:
                self.status = _('No changes')
        except Exception, e:
            self.status = _(e)