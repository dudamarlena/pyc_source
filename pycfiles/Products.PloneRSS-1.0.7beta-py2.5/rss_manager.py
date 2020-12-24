# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/PloneRSS/content/rss_manager.py
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
import rssparser, feedparser, md5, pickle
schema = Schema((
 StringField(name='publish', default='No', widget=SelectionWidget(label='Require publication', description='Select whether users need to have their feeds published or not', label_msgid='PloneRSS_label_publish', description_msgid='PloneRSS_help_publish', i18n_domain='PloneRSS'), vocabulary=[
  'Yes', 'No']),
 StringField(name='retention', widget=SelectionWidget(label='Retention', description='How long should we keep new items for', label_msgid='PloneRSS_label_retention', description_msgid='PloneRSS_help_retention', i18n_domain='PloneRSS'), vocabulary=[
  'Forever', '1 year', '6 months', '2 months', '1 month', '2 weeks', '1 week', '4 days', '2 days'])))
rss_manager_schema = ATFolderSchema.copy() + schema.copy()

class rss_manager(ATFolder):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.Irss_manager)
    meta_type = 'rss_manager'
    _at_rename_after_creation = True
    schema = rss_manager_schema
    security.declarePublic('newOperation')

    def newOperation(self):
        """
        """
        pass

    security.declarePublic('calculate_md5')

    def calculate_md5(self, link, title):
        """ """
        digest = md5.md5()
        digest.update(link)
        digest.update(title)
        return digest.hexdigest()

    security.declarePublic('pickle_save')

    def pickle_save(self, data):
        """ """
        return pickle.dumps(data)

    security.declarePublic('pickle_load')

    def pickle_load(self, data):
        """ """
        try:
            return pickle.loads(data)
        except:
            return {}

    security.declarePublic('feedparser')

    def feedparser(self, url):
        """ """
        rss = feedparser.parse(url)
        result = {}
        entries = []
        result['status'] = getattr(rss, 'status', 666)
        result['count'] = len(getattr(rss, 'entries', []))
        for entry in rss.entries:
            newent = {}
            newent['title'] = getattr(entry, 'title', '[No Title]')
            newent['link'] = getattr(entry, 'link', '[No Link]')
            newent['description'] = getattr(entry, 'description', '[No Description]')
            newent['modified_parsed'] = getattr(entry, 'modified_parsed', (0, 0, 0,
                                                                           0, 0,
                                                                           0, 0,
                                                                           0))
            entries.append(newent)

        result['entries'] = entries
        return result

    security.declarePublic('fetch_feed')

    def fetch_feed(self, url):
        """ """
        return rssparser.parse(url)


registerType(rss_manager, PROJECTNAME)