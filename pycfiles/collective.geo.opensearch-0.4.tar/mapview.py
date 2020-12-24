# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ledermac/devel/plone41/zeocluster/src/collective.geo.opensearch/collective/geo/opensearch/browser/mapview.py
# Compiled at: 2013-01-29 07:14:40
import logging, urllib
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from collective.opensearch import opensearchMessageFactory as _
from collective.opensearch.browser import oslinkview

class IMapView(Interface):
    """
    Html view interface
    """
    pass


class MapView(oslinkview.OsLinkView):
    """
    Html browser view
    """
    implements(IMapView)

    def download_url(self):
        return self.context.absolute_url() + '/@@opensearch_link.kml?searchTerms=' + urllib.quote_plus(self.searchterm)