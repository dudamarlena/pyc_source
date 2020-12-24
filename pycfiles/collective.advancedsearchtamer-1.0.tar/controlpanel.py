# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/ads/browser/controlpanel.py
# Compiled at: 2009-01-02 03:04:19
from zope.interface import implements
from zope.formlib import form
from zope.i18nmessageid import MessageFactory
from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm
from Products.Five.formlib import formbase
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.PythonScripts.standard import html_quote, newline_to_br
from collective.ads.admin.utility import IAdsAdminControlPanelForm, IAdsPortal
_ = MessageFactory('portal_adsadmin')

class AdsAdminControlPanelForm(ControlPanelForm):
    """Control Panel Form"""
    __module__ = __name__
    implements(IAdsAdminControlPanelForm)
    ads = FormFieldsets(IAdsAdminControlPanelForm)
    ads.id = 'ads'
    ads.label = _('ads', default='Macros')
    form_fields = FormFieldsets(ads)
    label = _('AdsAdmin')
    description = _('AdsAdmin')
    form_name = _('AdsAdmin')