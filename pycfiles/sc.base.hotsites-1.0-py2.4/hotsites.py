# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/sc/base/hotsites/controlpanel/hotsites.py
# Compiled at: 2009-12-29 13:58:42
from zope.schema import Int
from zope.schema import Bool
from zope.schema import ASCII
from zope.schema import Tuple
from zope.schema import TextLine
from zope.formlib import form
from zope.component import adapts
from zope.interface import Interface
from zope.interface import implements
from zope.app.form.browser.textwidgets import ASCIIWidget
from zope.app.form.browser.boolwidgets import CheckBoxWidget
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from sc.base.hotsites import MessageFactory as _
from plone.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm

class IHotSitesConfSchema(Interface):
    __module__ = __name__
    allowedContentTypes = Tuple(title=_('Allowed Content Types'), description=_('allowed_content_types', default='Allowed Content Types on Hot Sites folder'), value_type=TextLine(), default=(), required=False)
    skin_name = ASCII(title=_('label_skin_name', default='Skin Name'), description=_('help_skin_name', default='Skin name to use on Hot Sites folder '), default=None, required=True)
    default_view_id = ASCII(title=_('label_default_view_id', default='Default view to the hot site'), description=_('help_default_view_id', default='Id of object to be used as default view on the hot site'), default=None, required=False)
    default_view_path = ASCII(title=_('label_default_view_path', default='Path of object'), description=_('help_default_view_path', default='Path of object to be copied as default view of hot site'), default=None, required=False)
    workflow_id = ASCII(title=_('label_workflow_id', default='Workflow Id to use on hot site'), description=_('help_workflow_id', default='Id of the workflow to be used in the hot site folder'), default=None, required=False)
    use_accessibility = Bool(title=_('label_use_accessibility', default='Use a alterantive document as accessibility content?'), description=_('help_use_accessibility', default='If checked, will be created a document to be used as accessibility content.'), default=False, required=False)


class HotSitesControlPanelAdapter(SchemaAdapterBase):
    __module__ = __name__
    adapts(IPloneSiteRoot)
    implements(IHotSitesConfSchema)

    def __init__(self, context):
        super(HotSitesControlPanelAdapter, self).__init__(context)
        portal_properties = getToolByName(context, 'portal_properties')
        self.context = portal_properties.hotsites_conf

    allowedContentTypes = ProxyFieldProperty(IHotSitesConfSchema['allowedContentTypes'])
    skin_name = ProxyFieldProperty(IHotSitesConfSchema['skin_name'])
    default_view_id = ProxyFieldProperty(IHotSitesConfSchema['default_view_id'])
    default_view_path = ProxyFieldProperty(IHotSitesConfSchema['default_view_path'])
    workflow_id = ProxyFieldProperty(IHotSitesConfSchema['workflow_id'])
    use_accessibility = ProxyFieldProperty(IHotSitesConfSchema['use_accessibility'])


hotsites_set = FormFieldsets(IHotSitesConfSchema)
hotsites_set.id = 'hotsites'
hotsites_set.label = _('Hot Sites')

class HotSitesControlPanel(ControlPanelForm):
    __module__ = __name__
    form_fields = FormFieldsets(hotsites_set)
    form_fields['skin_name'].custom_widget = ASCIIWidget
    form_fields['default_view_id'].custom_widget = ASCIIWidget
    form_fields['default_view_path'].custom_widget = ASCIIWidget
    form_fields['workflow_id'].custom_widget = ASCIIWidget
    form_fields['use_accessibility'].custom_widget = CheckBoxWidget
    label = _('Hot Site Settings')
    description = _('Settings to Hot Site.')
    form_name = _('Hot Site settings')