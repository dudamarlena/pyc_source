# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/metadata/browser/controlpanel.py
# Compiled at: 2009-09-04 10:38:20
from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.schema import TextLine, Choice, List, Bool
from zope.formlib import form
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from atreal.richfile.metadata import RichFileMetadataMessageFactory as _
from atreal.richfile.qualifier.common import RFControlPanel
from atreal.richfile.metadata.interfaces import IMetadataExtractor
from plone.app.controlpanel.form import ControlPanelForm

class IRichFileMetadataSchema(Interface):
    """ """
    __module__ = __name__
    rf_metadata_collapsed = Bool(title=_('label_rf_metadata_collapsed', default='Display collapsed ?'), description=_('help_rf_streaming_collapsed', default="Do you want the plugin's display to be collapsed ?"), default=False)


class RichFileMetadataControlPanelAdapter(SchemaAdapterBase):
    """ """
    __module__ = __name__
    adapts(IPloneSiteRoot)
    implements(IRichFileMetadataSchema)
    rf_metadata_collapsed = ProxyFieldProperty(IRichFileMetadataSchema['rf_metadata_collapsed'])


class RichFileMetadataControlPanel(RFControlPanel):
    __module__ = __name__
    template = ZopeTwoPageTemplateFile('controlpanel.pt')
    form_fields = form.FormFields(IRichFileMetadataSchema)
    label = _('RichFileMetadata settings')
    description = _('RichFileMetadata settings for this site.')
    form_name = _('RichFileMetadata settings')
    plugin_iface = IMetadataExtractor
    supported_ifaces = ('atreal.richfile.metadata.interfaces.IMetadata', )