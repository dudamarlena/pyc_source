# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/browser/typescontrolpanel.py
# Compiled at: 2009-04-26 22:17:24
from zope.component import getUtility
from zope.formlib import form
from zope.interface import implements
from plone.app.controlpanel.form import ControlPanelForm
from Products.DigestoContentTypes import DigestoContentTypesMessageFactory as _
from Products.DigestoContentTypes.browser.widget import NormativaDynamicSequenceWidget
from Products.DigestoContentTypes.utilities.interfaces import INormativaTypes

def normativa_types_settings(context):
    """Adapter factory"""
    return getUtility(INormativaTypes)


class NormativaTypesControlPanel(ControlPanelForm):
    """Control panel form view for the normativa types management.
    """
    __module__ = __name__
    form_fields = form.FormFields(INormativaTypes)
    form_fields['types'].custom_widget = NormativaDynamicSequenceWidget
    form_name = _('Normativa Types Management')
    label = _('Normativa Types Management')
    description = _('Please enter Normativa Types')

    def _on_save(self, data):
        nt = getUtility(INormativaTypes)
        nt.types.sort()