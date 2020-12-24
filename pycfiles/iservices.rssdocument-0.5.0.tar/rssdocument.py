# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erik/Develop/amlo/src/iservices.rssdocument/iservices/rssdocument/content/rssdocument.py
# Compiled at: 2012-05-03 22:31:07
import urlparse
from urllib import quote
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ModifyPortalContent
from AccessControl import ClassSecurityInfo
from iservices.rssdocument import RSSDocumentMessageFactory as _
from iservices.rssdocument.interfaces import IRSSDocument
from iservices.rssdocument import config
RSSDocumentSchema = ATContentTypeSchema.copy() + atapi.Schema((
 atapi.StringField('RSSLink', required=True, widget=atapi.StringWidget(label=_('RSS URL'), description=_('The URL of the RSS Feed'))),
 atapi.IntegerField('max_entries', required=True, widget=atapi.IntegerWidget(label=_('Max Entries'), description=_('Maximum Number of entries to show')))))
finalizeATCTSchema(RSSDocumentSchema)

class RSSDocument(base.ATCTContent):
    """A Plone document that embedds a RSS feed with JQuery"""
    implements(IRSSDocument)
    schema = RSSDocumentSchema
    security = ClassSecurityInfo()
    security.declareProtected(ModifyPortalContent, 'setRSSLink')

    def setRSSLink(self, value, **kwargs):
        """RSS Link mutator - taken from ATLink

        Use urlparse to sanify the url
        Also see http://dev.plone.org/plone/ticket/3296
        """
        if value:
            value = urlparse.urlunparse(urlparse.urlparse(value))
        self.getField('RSSLink').set(self, value, **kwargs)

    security.declareProtected(View, 'getRSSLink')

    def getRSSLink(self):
        """Sanitize output - taken from ATLink
        """
        value = self.Schema()['RSSLink'].get(self)
        if not value:
            value = ''
        return quote(value, safe='?$#@/:=+;$,&%')


atapi.registerType(RSSDocument, config.PROJECTNAME)