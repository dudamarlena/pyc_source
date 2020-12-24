# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/iqpp/plone/rotating/browser/options.py
# Compiled at: 2008-08-04 04:35:06
from zope.formlib import form
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('iqpp.plone.commenting')
from Products.CMFCore.utils import getToolByName
from Products.Five.formlib import formbase
from Products.Five.browser import pagetemplatefile
from iqpp.plone.rotating.config import MESSAGES
from iqpp.plone.rotating.interfaces import IRotatingOptions

class OptionsForm(formbase.EditForm):
    """
    """
    __module__ = __name__
    form_fields = form.FormFields(IRotatingOptions)
    template = pagetemplatefile.ZopeTwoPageTemplateFile('options.pt')

    @form.action('add')
    def action_add(self, action, data):
        """
        """
        options = IRotatingOptions(self.context)
        options.setOptions(data)
        ptool = getToolByName(self.context, 'plone_utils')
        ptool.addPortalMessage(MESSAGES['options-saved'])
        url = self.context.absolute_url() + '/rotating-options'
        self.request.response.redirect(url)