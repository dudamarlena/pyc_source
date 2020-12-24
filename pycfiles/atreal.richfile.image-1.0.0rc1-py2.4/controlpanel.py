# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/image/browser/controlpanel.py
# Compiled at: 2009-09-04 10:39:07
from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.schema import TextLine, Choice, List, Bool
from zope.formlib import form
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from atreal.richfile.image import RichFileImageMessageFactory as _
from atreal.richfile.image.interfaces import IImageable
from plone.app.controlpanel.form import ControlPanelForm
from atreal.richfile.qualifier.common import RFControlPanel

class IRichFileImageSchema(Interface):
    """ """
    __module__ = __name__
    rf_image_collapsed = Bool(title=_('label_rf_image_collapsed', default='Display collapsed ?'), description=_('help_rf_image_collapsed', default="Do you want the plugin's display to be collapsed ?"), default=False)


class RichFileImageControlPanelAdapter(SchemaAdapterBase):
    __module__ = __name__
    adapts(IPloneSiteRoot)
    implements(IRichFileImageSchema)
    rf_image_collapsed = ProxyFieldProperty(IRichFileImageSchema['rf_image_collapsed'])


class RichFileImageControlPanel(RFControlPanel):
    __module__ = __name__
    template = ZopeTwoPageTemplateFile('controlpanel.pt')
    form_fields = form.FormFields(IRichFileImageSchema)
    label = _('RichFileImage settings')
    description = _('RichFileImage settings for this site.')
    form_name = _('RichFileImage settings')
    plugin_iface = IImageable
    supported_ifaces = ('atreal.richfile.image.interfaces.IImage', )