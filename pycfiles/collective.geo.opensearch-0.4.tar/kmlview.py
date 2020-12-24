# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    pass


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