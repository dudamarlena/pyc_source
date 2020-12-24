# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/override/sharing/browser/controlpanel.py
# Compiled at: 2009-09-07 04:14:45
from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.schema import Choice, List
from zope.formlib import form
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from atreal.override.sharing import OverrideSharingMessageFactory as _
from plone.app.controlpanel.form import ControlPanelForm

class IOverrideSharingSchema(Interface):
    __module__ = __name__
    sharing_group_confidential = List(title=_('Groups authorized'), required=False, default=[], value_type=Choice(title=_('Groups authorized'), source='plone.app.vocabularies.Groups'))


class OverrideSharingControlPanelAdapter(SchemaAdapterBase):
    __module__ = __name__
    adapts(IPloneSiteRoot)
    implements(IOverrideSharingSchema)

    def __init__(self, context):
        super(OverrideSharingControlPanelAdapter, self).__init__(context)

    sharing_group_confidential = ProxyFieldProperty(IOverrideSharingSchema['sharing_group_confidential'])


class OverrideSharingControlPanel(ControlPanelForm):
    __module__ = __name__
    form_fields = form.FormFields(IOverrideSharingSchema)
    label = _('OverrideSharing settings')
    description = _('OverrideSharing settings for this site.')
    form_name = _('OverrideSharing settings')