# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    pass


class AtomView(atomview.AtomView):
    """
    Atom browser view
    """
    implements(IAtomView)
    render = ViewPageTemplateFile('atomview.pt')
    LinkEntry = AtomEntry