# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplon/plone/ldap/browser/baseform.py
# Compiled at: 2007-11-14 08:14:44
from Acquisition import Implicit
from Acquisition import aq_inner, aq_parent
from zope.component import getMultiAdapter
from zope.formlib.form import action, applyChanges
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from Products.Five import BrowserView
from Products.Five.formlib.formbase import AddFormBase
from Products.Five.formlib.formbase import EditFormBase
from plone.app.form.validators import null_validator
from Products.CMFPlone import PloneMessageFactory as _

class Adding(Implicit, BrowserView):
    __module__ = __name__
    __allow_access_to_unprotected_subobjects__ = True
    contentName = None
    request = None
    context = None

    def nextURL(self):
        return

    def hasCustomAddView(self):
        return False

    def addingInfo(self):
        return []

    def isSingleMenuItem(self):
        return False


class LDAPAddForm(AddFormBase):
    """Base class for add forms.

    This class has a nextURL method which will return the URL of the LDAP
    management screen and standard form actions.
    """
    __module__ = __name__
    fieldset = None

    def nextURL(self):
        parent = aq_parent(aq_inner(self.context))
        url = str(getMultiAdapter((parent, self.request), name='absolute_url'))
        if self.fieldset is not None:
            return url + '/@@ldap-controlpanel#fieldsetlegend-' + self.fieldset
        return url + '/@@ldap-controlpanel'

    @action(_('label_save', default='Save'), name='save')
    def handle_save_action(self, action, data):
        self.createAndAdd(data)

    @action(_('label_cancel', default='Cancel'), validator=null_validator, name='cancel')
    def handle_cancel_action(self, action, data):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''


class LDAPEditForm(EditFormBase):
    """Base class for edit forms.

    This class has a nextURL method which will return the URL of the LDAP
    management screen and standard form actions.
    """
    __module__ = __name__
    fieldset = None

    @action(_('label_save', default='Save'), name='save')
    def handle_save_action(self, action, data):
        if applyChanges(self.context, self.form_fields, data, self.adapters):
            notify(ObjectModifiedEvent(self.context))
            self.status = 'Changes saved'
        else:
            self.status = 'No changes'
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''

    @action(_('label_cancel', default='Cancel'), validator=null_validator, name='cancel')
    def handle_cancel_action(self, action, data):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''

    def nextURL(self):
        parent = aq_parent(aq_inner(self.context))
        url = str(getMultiAdapter((parent, self.request), name='absolute_url'))
        if self.fieldset is not None:
            return url + '/@@ldap-controlpanel#fieldsetlegend-' + self.fieldset
        return url + '/@@ldap-controlpanel'