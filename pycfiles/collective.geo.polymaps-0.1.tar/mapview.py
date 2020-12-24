# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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


class MapView(oslinkview.OsLinkView):
    """
    Html browser view
    """
    implements(IMapView)

    def download_url(self):
        return self.context.absolute_url() + '/@@opensearch_link.kml?searchTerms=' + urllib.quote_plus(self.searchterm)