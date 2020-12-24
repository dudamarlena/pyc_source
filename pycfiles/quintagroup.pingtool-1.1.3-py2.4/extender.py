# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/pingtool/extender.py
# Compiled at: 2009-03-31 04:47:33
from zope.component import getAdapter
from Products.Archetypes.public import *
from Products.CMFCore.utils import getToolByName
from archetypes.schemaextender.field import ExtensionField
from quintagroup.pingtool import PingToolMessageFactory as _
from interfaces import ICanonicalURL

def getPingDefaultUrl(context, rss_version='Weblog'):
    rss_templates = {'ping_Weblog': '', 'ping_RSS': '/RSS', 'ping_RSS2': '/RSS2'}
    url = getToolByName(context, 'portal_url').getRelativeContentURL(context)
    portal_pingtool = getToolByName(context, 'portal_pingtool', None)
    ping_url = ''
    if portal_pingtool:
        canonical_url = getAdapter(portal_pingtool, ICanonicalURL, 'canonical_url_adapter').getCanonicalURL()
        if canonical_url:
            if not canonical_url.endswith('/'):
                canonical_url += '/'
            if not canonical_url.startswith('http://'):
                canonical_url = 'http://' + canonical_url
            url = canonical_url + url
            site_rss_version = rss_templates[rss_version]
            ping_url = url + site_rss_version
    return ping_url


class MyLinesField(ExtensionField, LinesField):
    """A trivial lines field."""
    __module__ = __name__


class MyStringField(ExtensionField, StringField):
    """The string field with custom 'get' method."""
    __module__ = __name__

    def get(self, instance, **kwargs):
        value = super(MyStringField, self).get(instance)
        if not value:
            value = getPingDefaultUrl(instance, self.__name__)
        return value


class MyBooleanField(ExtensionField, BooleanField):
    """A trivial boolean field."""
    __module__ = __name__


class PingToolExtender(object):
    """ PingToolExtender custom field
    """
    __module__ = __name__
    fields = [
     MyBooleanField('enable_ping', default=0, schemata='PingSetup', widget=BooleanWidget(label=_('label_enable_ping', default='Enable Ping'), description=_('help_enable_ping', default=''))), MyLinesField('ping_sites', schemata='PingSetup', multiValued=True, vocabulary_factory='quintagroup.pingtool.getPingSites', enforceVocabulary=True, size=10, widget=MultiSelectionWidget(format='checkbox', size=10, label=_('label_ping_sites', default='Ping Sites'), description=_('help_ping_sites', default='List of ping sites.'))), MyStringField('ping_Weblog', schemata='PingSetup', widget=StringWidget(label=_('label_weblog_rssversion', default='Ping url for Weblog'), description=_('help_weblog_rssversion', default='RSS version.'))), MyStringField('ping_RSS', schemata='PingSetup', widget=StringWidget(label=_('label_rss1_rssversion', default='Ping url for RSS'), description=_('help_rss1_rssversion', default='RSS version.'))), MyStringField('ping_RSS2', schemata='PingSetup', widget=StringWidget(label=_('label_rss2_rssversion', default='Ping url for RSS2'), description=_('help_rss2_rssversion', default='RSS version.')))]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields