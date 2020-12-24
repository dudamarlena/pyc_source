# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ledermac/devel/plone41/zeocluster/src/collective.geo.opensearch/collective/geo/opensearch/browser/atomview.py
# Compiled at: 2013-01-29 07:14:40
from zope.interface import implements, Interface
from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.opensearch.browser import atomview
from utils import get_geo_rss

class AtomEntry(atomview.AtomEntry):

    def geo_rss(self):
        return get_geo_rss(self, self.brain)


class IAtomView(Interface):
    """
    Atom view interface
    """


class AtomView(atomview.AtomView):
    """
    Atom browser view
    """
    implements(IAtomView)
    render = ViewPageTemplateFile('atomview.pt')
    LinkEntry = AtomEntry