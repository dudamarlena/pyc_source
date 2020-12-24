# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/pingtool/PingInfo.py
# Compiled at: 2009-03-31 04:47:33
from Globals import DTMLFile
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFDefault.utils import _dtmldir
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema, finalizeATCTSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from config import RSS_LIST, PROJECTNAME
from quintagroup.pingtool import PingToolMessageFactory as _
PingInfoSchema = ATContentTypeSchema.copy() + Schema((TextField('description', default='', searchable=False, widget=TextAreaWidget(label=_('label_description', default='Description'), description=_('help_description', default='Description of ping info'))), StringField('url', default='', required=1, searchable=False, widget=StringWidget(label=_('label_url', default='Url ping servies'), description=_('help_url', default=''))), StringField('method_name', default='weblogUpdates.ping', required=1, searchable=False, widget=StringWidget(label=_('label_method_name', default='Method name'), description=_('help_method_name', default=''))), StringField('rss_version', default='Weblog', searchable=False, vocabulary=RSS_LIST, widget=SelectionWidget(label=_('label_rss_version', default='RSS version'), description=_('help_rss_version', default='')))), marshall=RFC822Marshaller())

class PingInfo(ATCTContent, HistoryAwareMixin):
    """Ping Info container
       id - name of the server to ping
       url - server ping url
       method_name - ping method
       rss_version - rss version supported by the server
    """
    __module__ = __name__
    __implements__ = (
     ATCTContent.__implements__, HistoryAwareMixin.__implements__)
    schema = PingInfoSchema
    security = ClassSecurityInfo()

    def Contributors(self):
        return self.contributors

    security.declareProtected(ModifyPortalContent, 'manage_metadata')
    manage_metadata = DTMLFile('zmi_metadata', _dtmldir)


registerType(PingInfo, PROJECTNAME)