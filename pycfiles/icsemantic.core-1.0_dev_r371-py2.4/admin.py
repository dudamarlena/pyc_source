# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/core/browser/admin.py
# Compiled at: 2008-10-06 10:31:07
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
from zope.formlib import form
from zope.app.form.browser import MultiSelectSetWidget
from zope.app.form.browser.itemswidgets import MultiSelectWidget as BaseMultiSelectWidget, DropdownWidget, SelectWidget
from zope.app.form.browser import FileWidget
try:
    from zope.lifecycleevent import ObjectModifiedEvent
except:
    from zope.app.event.objectevent import ObjectModifiedEvent

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.browser import BrowserView
from Products.Five.formlib import formbase
from icsemantic.core import interfaces
from icsemantic.core import pkg_home
from icsemantic.core.i18n import _
from base import BaseSettingsForm
from widgets import OrderedMultiSelectionWidgetFactory, MultiSelectionWidgetFactory
from icsemantic.core.vocabularies import LanguagesVocabularyFactory

class Overview(BrowserView):
    """ icSemantic config overview
        """
    __module__ = __name__

    def getVersion(self):
        fh = open(os.path.join(pkg_home, 'version.txt'))
        version_string = fh.read()
        fh.close()
        return version_string


class UserOverview(BrowserView):
    """ icSemantic user config overview
        """
    __module__ = __name__

    def __init__(self, context, request):
        self.context = context
        self.request = request
        super(UserOverview, self).__init__(context, request)

    def __call__(self):
        self.authenticated_member = self.context.portal_membership.getAuthenticatedMember()
        return super(UserOverview, self).__call__()


class ContentTypes(BaseSettingsForm):
    """ Configlet para elegir los Content Types que tendran la
                capacidad de hacer fallback de lenguajes
        """
    __module__ = __name__
    form_name = _('Content Types')
    form_fields = form.Fields(interfaces.IicSemanticManagementContentTypes)
    form_fields['fallback_types'].custom_widget = MultiSelectionWidgetFactory

    @form.action(_('Apply'), condition=form.haveInputWidgets)
    def handle_edit_action(self, action, data):
        old_types = self.adapters['IicSemanticManagementContentTypes'].fallback_types
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            ccpatcher = getUtility(interfaces.IContentTypesMultilingualPatcher)
            for type_name in data['fallback_types']:
                ccpatcher.patch(type_name, True)

            unpatch_types = [ type_name for type_name in old_types if type_name not in data['fallback_types'] ]
            for type_name in unpatch_types:
                ccpatcher.unpatch(type_name)

            zope.event.notify(ObjectModifiedEvent(self.context))
            self.status = _('Updated on ${date_time}', mapping={'date_time': str(datetime.utcnow())})
        else:
            self.status = _('No changes')


class ManageUserLanguages(BaseSettingsForm):
    """ Configlet para configurar los lenguajes por usuario
        """
    __module__ = __name__
    form_name = _('My Languages')
    form_fields = form.Fields(interfaces.IicSemanticManageUserLanguages)
    form_fields['icsemantic_preferred_languages'].custom_widget = OrderedMultiSelectionWidgetFactory