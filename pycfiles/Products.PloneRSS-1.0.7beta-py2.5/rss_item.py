# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/PloneRSS/content/rss_item.py
# Compiled at: 2008-10-21 05:47:02
__author__ = 'Gareth Bult <gareth@encryptec.net>'
__docformat__ = 'plaintext'
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.ATContentTypes.content.newsitem import ATNewsItem
from Products.ATContentTypes.content.newsitem import ATNewsItemSchema
from Products.PloneRSS.config import *
schema = Schema((
 StringField(name='rssKey', widget=StringField._properties['widget'](label='Rsskey', label_msgid='PloneRSS_label_rssKey', i18n_domain='PloneRSS')),
 StringField(name='rssID', widget=StringField._properties['widget'](label='Rssid', label_msgid='PloneRSS_label_rssID', i18n_domain='PloneRSS')),
 DateTimeField(name='rssDate', widget=DateTimeField._properties['widget'](label='Rssdate', label_msgid='PloneRSS_label_rssDate', i18n_domain='PloneRSS')),
 StringField(name='remoteUrl', widget=StringField._properties['widget'](label='URL', description='Actual location of source news item', label_msgid='PloneRSS_label_remoteUrl', description_msgid='PloneRSS_help_remoteUrl', i18n_domain='PloneRSS'))))
rss_item_schema = ATNewsItemSchema.copy() + schema.copy()

class rss_item(ATNewsItem):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.Irss_item)
    meta_type = 'rss_item'
    _at_rename_after_creation = True
    schema = rss_item_schema


registerType(rss_item, PROJECTNAME)