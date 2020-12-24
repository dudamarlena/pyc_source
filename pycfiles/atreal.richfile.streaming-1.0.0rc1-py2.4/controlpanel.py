# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/streaming/browser/controlpanel.py
# Compiled at: 2009-10-31 10:38:14
from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.schema import TextLine, Choice, List, Bool, Password
from zope.formlib import form
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_hasattr
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from atreal.richfile.streaming import RichFileStreamingMessageFactory as _
from atreal.richfile.streaming.interfaces import IStreamable
from atreal.richfile.qualifier.common import RFControlPanel
from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm

class IRFStreamingMainSchema(Interface):
    __module__ = __name__
    rf_streaming_collapsed = Bool(title=_('label_rf_streaming_collapsed', default='Display collapsed ?'), description=_('help_rf_streaming_collapsed', default="Do you want the plugin's display to be collapsed ?"), default=False)
    rfs_autoplay = Bool(title=_('label_rfs_autoplay', default='Auto Play ?'), description=_('help_rfs_autoplay', default='Do you want the player start automatically when the page is loaded or do you want a user action to start it ?'), default=False)


class IRFStreamingConvertDaemonSchema(Interface):
    __module__ = __name__
    rfs_host = TextLine(title=_('label_rfs_host', default='ConvertDaemon host'), description=_('help_rfs_host', default="The address of your ConvertDaemon server. Usually 'localhost', unless you use an external server."), default='localhost', required=True)
    rfs_port = TextLine(title=_('label_rfs_port', default='ConvertDaemon port'), description=_('help_rfs_port', default="The port of your ConvertDaemon server. Usually '8888', unless you use another port."), default='8888', required=True)
    rfs_callback_netloc = TextLine(title=_('label_rfs_callback_netloc', default='ConvertDaemon callback netloc'), description=_('help_rfs_callback_netloc', default='The address of your zope server.'), default='localhost:8080', required=True)
    rfs_user = TextLine(title=_('label_rfs_user', default='ConvertDaemon username'), description=_('help_rfs_user', default='Username for authentication of ConvertDaemon on Plone Site. '), default='admin', required=True)
    rfs_pass = Password(title=_('label_rfs_pass', default='ConvertDaemon password'), description=_('help_rfs_pass', default='The password for the ConvertDaemon user account.'), default='admin', required=True)


class IRichFileStreamingSchema(IRFStreamingMainSchema, IRFStreamingConvertDaemonSchema):
    """Combined schema for the adapter lookup.
    """
    __module__ = __name__


class RichFileStreamingControlPanelAdapter(SchemaAdapterBase):
    __module__ = __name__
    adapts(IPloneSiteRoot)
    implements(IRichFileStreamingSchema)
    rf_streaming_collapsed = ProxyFieldProperty(IRichFileStreamingSchema['rf_streaming_collapsed'])
    rfs_autoplay = ProxyFieldProperty(IRichFileStreamingSchema['rfs_autoplay'])
    rfs_host = ProxyFieldProperty(IRichFileStreamingSchema['rfs_host'])
    rfs_port = ProxyFieldProperty(IRichFileStreamingSchema['rfs_port'])
    rfs_callback_netloc = ProxyFieldProperty(IRichFileStreamingSchema['rfs_callback_netloc'])
    rfs_user = ProxyFieldProperty(IRichFileStreamingSchema['rfs_user'])
    rfs_pass = ProxyFieldProperty(IRichFileStreamingSchema['rfs_pass'])


rfs_mainset = FormFieldsets(IRFStreamingMainSchema)
rfs_mainset.id = 'main'
rfs_mainset.label = _('label_rfs_main', default='Main')
rfs_convertdaemonset = FormFieldsets(IRFStreamingConvertDaemonSchema)
rfs_convertdaemonset.id = 'convertdaemon'
rfs_convertdaemonset.label = _('label_rfs_convertdaemon', default='ConvertDaemon')

class RichFileStreamingControlPanel(RFControlPanel):
    """
    """
    __module__ = __name__
    template = ZopeTwoPageTemplateFile('controlpanel.pt')
    form_fields = FormFieldsets(rfs_mainset, rfs_convertdaemonset)
    label = _('RichFileStreaming settings')
    description = _('RichFileStreaming settings for this site.')
    form_name = _('RichFileStreaming settings')
    plugin_iface = IStreamable
    supported_ifaces = ('atreal.richfile.streaming.interfaces.IStreaming', )