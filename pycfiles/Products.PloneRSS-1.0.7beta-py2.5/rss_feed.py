# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/PloneRSS/content/rss_feed.py
# Compiled at: 2008-10-21 05:47:02
__author__ = 'Gareth Bult <gareth@encryptec.net>'
__docformat__ = 'plaintext'
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.PloneRSS.config import *
schema = Schema((
 StringField(name='frequency', widget=SelectionWidget(label='Update frequency', description='How often should we update the feed from the RSS source', label_msgid='PloneRSS_label_frequency', description_msgid='PloneRSS_help_frequency', i18n_domain='PloneRSS'), vocabulary=[
  '1 day', '12 hours', '8 hours', '4 hours', '2 hours', '1 hour', '30 minutes', '15 minutes', '5 minutes']),
 StringField(name='rssID', widget=StringField._properties['widget'](visible=False, label='Rssid', label_msgid='PloneRSS_label_rssID', i18n_domain='PloneRSS')),
 StringField(name='maxage', widget=SelectionWidget(label='Maximum item age', description='How long we should keep news items in the database', label_msgid='PloneRSS_label_maxage', description_msgid='PloneRSS_help_maxage', i18n_domain='PloneRSS'), vocabulary=[
  'Unlimited', '1 week', '2 weeks', '1 month', '2 months', '4 months', '8 months', '16 months']),
 StringField(name='remoteURL', widget=StringField._properties['widget'](label='Feed URL', size=80, maxlength=1024, label_msgid='PloneRSS_label_remoteURL', i18n_domain='PloneRSS'))))
rss_feed_schema = ATFolderSchema.copy() + schema.copy()

class rss_feed(ATFolder):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.Irss_feed)
    meta_type = 'rss_feed'
    _at_rename_after_creation = True
    schema = rss_feed_schema


registerType(rss_feed, PROJECTNAME)