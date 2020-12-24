# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-fat/egg/sc/social/viewcounter/controlpanel/viewcounter.py
# Compiled at: 2010-08-18 13:21:09
from zope.schema import Int
from zope.schema import TextLine
from zope.schema import Tuple
from zope.schema import Choice
from zope.component import adapts
from zope.interface import Interface
from zope.interface import implements
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from zope.formlib.form import FormFields
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.controlpanel.widgets import MultiSelectTupleWidget
from sc.social.viewcounter import MessageFactory as _

class IViewCounterSchema(Interface):
    __module__ = __name__
    blacklisted_types = Tuple(title=_('Content types blacklist'), description=_('help_blacklisted_types', default='Please check any blacklisted content type -- type not to be listed on portlets and viewlets.'), missing_value=set(), value_type=Choice(vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes'))
    valid_wf_states = Tuple(title=_('Valid workflow states'), description=_('help_valid_wf_statess', default='Please inform workflow states that will be shown on rankings.'), missing_value=set(), value_type=Choice(vocabulary='plone.app.vocabularies.WorkflowStates'))


class ViewCounterControlPanelAdapter(SchemaAdapterBase):
    __module__ = __name__
    adapts(IPloneSiteRoot)
    implements(IViewCounterSchema)

    def __init__(self, context):
        super(ViewCounterControlPanelAdapter, self).__init__(context)
        portal_properties = getToolByName(context, 'portal_properties')
        self.context = portal_properties.sc_social_viewcounter

    blacklisted_types = ProxyFieldProperty(IViewCounterSchema['blacklisted_types'])
    valid_wf_states = ProxyFieldProperty(IViewCounterSchema['valid_wf_states'])


class ViewCounterControlPanel(ControlPanelForm):
    __module__ = __name__
    form_fields = FormFields(IViewCounterSchema)
    label = _('ViewCounter Settings')
    description = _('Settings for sc.social.viewcounter.')
    form_name = _('ViewCounter Settings')