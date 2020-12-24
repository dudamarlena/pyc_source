# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ledermac/devel/plone41/zeocluster/src/collective.geo.opensearch/collective/geo/opensearch/browser/rssview.py
# Compiled at: 2013-01-29 07:14:40
from DateTime import DateTime
from zope.interface import implements, Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.opensearch.browser import rssview
from utils import get_geo_rss

class RSSEntry(rssview.RSSEntry):

    def geo_rss(self):
        return get_geo_rss(self, self.brain)


class IRSSView(Interface):
    """
    RSS view interface
    """


class RSSView(rssview.RSSView):
    """
    RSS browser view
    """
    implements(IRSSView)
    render = ViewPageTemplateFile('rssview.pt')
    LinkEntry = RSSEntry