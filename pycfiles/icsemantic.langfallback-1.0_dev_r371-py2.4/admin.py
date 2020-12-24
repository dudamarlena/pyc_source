# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/langfallback/browser/admin.py
# Compiled at: 2008-10-06 10:31:04
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
from zope.app.form.browser.itemswidgets import MultiSelectWidget as BaseMultiSelectWidget
try:
    from zope.lifecycleevent import ObjectModifiedEvent
except:
    from zope.app.event.objectevent import ObjectModifiedEvent

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.browser import BrowserView
from Products.Five.formlib import formbase
from icsemantic.langfallback import interfaces
from icsemantic.core import pkg_home
from icsemantic.core.i18n import _
from icsemantic.core.browser.base import BaseSettingsForm
from icsemantic.core.browser.widgets import OrderedMultiSelectionWidgetFactory, MultiSelectionWidgetFactory

class ManageUserLanguages(BaseSettingsForm):
    """ Configlet para configurar los lenguajes por usuario
    """
    __module__ = __name__
    form_name = _('My Languages')
    form_fields = form.Fields(interfaces.IManageUserLanguages)
    form_fields['icsemantic_languages'].custom_widget = OrderedMultiSelectionWidgetFactory