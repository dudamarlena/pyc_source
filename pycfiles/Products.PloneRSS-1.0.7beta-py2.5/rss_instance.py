# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/PloneRSS/content/rss_instance.py
# Compiled at: 2008-10-21 05:47:02
__author__ = 'Gareth Bult <gareth@encryptec.net>'
__docformat__ = 'plaintext'
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.PloneRSS.config import *
schema = Schema((
 StringField(name='active', default='Yes', widget=SelectionWidget(label='Portlet active', description='Is this portlet currently to be displayed', label_msgid='PloneRSS_label_active', description_msgid='PloneRSS_help_active', i18n_domain='PloneRSS'), vocabulary=[
  'Yes', 'No']),
 ReferenceField(name='rss_feeds', widget=ReferenceBrowserWidget(label='Feeds', description='The feeds that will appear in this instance', label_msgid='PloneRSS_label_rss_feeds', description_msgid='PloneRSS_help_rss_feeds', i18n_domain='PloneRSS'), allowed_types=('rss_feed', ), multiValued=1, relationship='feeds')))
rss_instance_schema = ATFolderSchema.copy() + schema.copy()

class rss_instance(ATFolder):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.Irss_instance)
    meta_type = 'rss_instance'
    _at_rename_after_creation = True
    schema = rss_instance_schema


registerType(rss_instance, PROJECTNAME)