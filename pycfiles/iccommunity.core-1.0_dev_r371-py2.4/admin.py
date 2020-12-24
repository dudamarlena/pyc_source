# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/core/browser/admin.py
# Compiled at: 2008-10-06 10:31:14
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
from iccommunity.core import interfaces
from iccommunity.core import pkg_home
from iccommunity.core.i18n import _
from base import BaseSettingsForm
from widgets import OrderedMultiSelectionWidgetFactory, MultiSelectionWidgetFactory

class Overview(BrowserView):
    """ Platecom config overview
    """
    __module__ = __name__

    def getVersion(self):
        fh = open(os.path.join(pkg_home, 'version.txt'))
        version_string = fh.read()
        fh.close()
        return version_string


class UserOverview(BrowserView):
    """ Platecom user config overview
    """
    __module__ = __name__

    def __init__(self, context, request):
        self.context = context
        self.request = request
        super(UserOverview, self).__init__(context, request)

    def __call__(self):
        self.authenticated_member = self.context.portal_membership.getAuthenticatedMember()
        return super(UserOverview, self).__call__()