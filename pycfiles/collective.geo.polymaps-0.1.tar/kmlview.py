# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ledermac/devel/plone41/zeocluster/src/collective.geo.opensearch/collective/geo/opensearch/browser/kmlview.py
# Compiled at: 2013-01-29 07:14:40
from zope.interface import implements, Interface
from plone.memoize import view
from collective.geo.kml.browser.kmldocument import KMLBaseDocument, BrainPlacemark
from collective.opensearch.browser import search

class IKMLView(Interface):
    """
    Search Kml view interface
    """


class KMLView(KMLBaseDocument):
    """
    FlexiTopicKml browser view
    """
    implements(IKMLView)

    @property
    @view.memoize
    def features(self):
        search_results = search.get_results(self.context, self.request)
        for brain in search_results:
            if brain.zgeo_geometry:
                yield BrainPlacemark(brain, self.request, self)