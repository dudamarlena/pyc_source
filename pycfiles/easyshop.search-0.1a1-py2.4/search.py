# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/search/browser/search.py
# Compiled at: 2008-09-04 04:30:30
from plone.memoize.instance import memoize
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.AdvancedQuery import And
from Products.AdvancedQuery import Eq

class SearchView(BrowserView):
    """Provides miscellanous methods for searching.
    """
    __module__ = __name__

    @memoize
    def getSearchResults(self, simple=True, searchable_text=None):
        """
        """
        if searchable_text is None:
            searchable_text = self.request.get('SearchableText', '')
        if searchable_text == '':
            return []
        utool = getToolByName(self.context, 'portal_url')
        portal_url = ('/').join(utool.getPortalObject().getPhysicalPath())
        properties = getToolByName(self.context, 'portal_properties').site_properties
        shop_path = portal_url + properties.easyshop_path
        catalog = getToolByName(self.context, 'portal_catalog')
        searchable_text_orig = searchable_text
        if searchable_text.find('*') == -1:
            searchable_text = (' ').join([ '*%s*' % x for x in searchable_text.split() ])
        query = And(Eq('path', shop_path), Eq('portal_type', 'Product'), Eq('Title', searchable_text))
        if simple == False:
            category = self.request.get('category')
            if category is not None:
                query = query & Eq('categories', category)
        results_glob = catalog.evalAdvancedQuery(query)
        searchable_text = searchable_text_orig
        searchable_text = searchable_text.replace('*', '')
        searchable_text = searchable_text.replace('%', '')
        searchable_text = '%' + searchable_text
        query = And(Eq('path', shop_path), Eq('portal_type', 'Product'), Eq('Title', searchable_text))
        if simple == False:
            category = self.request.get('category')
            if category is not None:
                query = query & Eq('categories', category)
        results_similar = catalog.evalAdvancedQuery(query)
        unique = {}
        for result in results_glob:
            unique[result.UID] = result

        for result in results_similar:
            unique[result.UID] = result

        result = unique.values()
        if len(result) == 0:
            searchable_text = searchable_text_orig
            searchable_text = searchable_text.replace('*', '')
            searchable_text = (' OR ').join([ '*%s*' % x for x in searchable_text.split() ])
            query = And(Eq('path', shop_path), Eq('portal_type', 'Product'), Eq('Title', searchable_text))
            if simple == False:
                category = self.request.get('category')
                if category is not None:
                    query = query & Eq('categories', category)
            result = catalog.evalAdvancedQuery(query)
        return result

    @memoize
    def getSearchUrl(self):
        """
        """
        properties = getToolByName(self.context, 'portal_properties').site_properties
        shop_path = properties.easyshop_path
        return shop_path + '/shop-search'