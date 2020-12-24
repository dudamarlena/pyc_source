# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ledermac/devel/plone41/zeocluster/src/collective.geo.opensearch/collective/geo/opensearch/browser/folderview.py
# Compiled at: 2013-01-29 07:14:40
import urllib
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from collective.opensearch import opensearchMessageFactory as _

class IFolderView(Interface):
    """
    OSFolder view interface
    """


class FolderView(BrowserView):
    """
    OSFolder browser view
    """
    implements(IFolderView)
    js_template = "\n        $.get('%(url)s',\n                function(data) {\n                  $('#%(id)s').html(data);\n            });\n            "

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def searchterm(self):
        return self.request.form.get('searchTerms', '')

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_searches(self):
        type_filter = {'portal_type': ['Link']}
        for r in self.context.getFolderContents(contentFilter=type_filter):
            if r.getObject().getLayout() == 'feed_map_view.html':
                yield r

    def get_js(self, link):
        vars = {}
        url = '/opensearchresults.html?searchTerms='
        vars['url'] = link.getURL() + url + urllib.quote_plus(self.searchterm)
        vars['id'] = 'searchresults-' + link.id
        return self.js_template % vars