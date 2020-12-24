# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/PloneRSS/content/rss_history.py
# Compiled at: 2008-10-21 05:47:03
__author__ = 'Gareth Bult <gareth@encryptec.net>'
__docformat__ = 'plaintext'
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.PloneRSS.config import *
schema = Schema((
 DateTimeField(name='last_date', widget=DateTimeField._properties['widget'](label='Last_date', label_msgid='PloneRSS_label_last_date', i18n_domain='PloneRSS')),
 IntegerField(name='last_count', widget=IntegerField._properties['widget'](label='Last_count', label_msgid='PloneRSS_label_last_count', i18n_domain='PloneRSS')),
 IntegerField(name='last_status', widget=IntegerField._properties['widget'](label='Last_status', label_msgid='PloneRSS_label_last_status', i18n_domain='PloneRSS')),
 StringField(name='body', widget=StringField._properties['widget'](label='Body', label_msgid='PloneRSS_label_body', i18n_domain='PloneRSS')),
 StringField(name='url', widget=StringField._properties['widget'](label='Url', label_msgid='PloneRSS_label_url', i18n_domain='PloneRSS')),
 StringField(name='feedID', widget=StringField._properties['widget'](label='Feedid', label_msgid='PloneRSS_label_feedID', i18n_domain='PloneRSS'))))
rss_history_schema = BaseSchema.copy() + schema.copy()

class rss_history(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.Irss_history)
    meta_type = 'rss_history'
    _at_rename_after_creation = True
    schema = rss_history_schema


registerType(rss_history, PROJECTNAME)