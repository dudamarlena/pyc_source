# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fud/advanced_search/browser/fudresultview.py
# Compiled at: 2009-12-15 15:39:42
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.AdvancedQuery import And, Eq, In, Or
from fud.advanced_search import advanced_searchMessageFactory as _

class IFudresultView(Interface):
    """
    Fudresult view interface
    """
    __module__ = __name__

    def getSearchItems():
        """ test method"""
        pass

    def __createTextQuery():
        """
        returns the query for the text search
        """
        pass

    def __listEqTuple():
        """
        Compare a list's content with a tuple's content
        """
        pass

    def __listHasElemFromTuple():
        """Compare a list's content with a tuple's content"""
        pass


class FudresultView(BrowserView):
    """
    Fudresult browser view
    """
    __module__ = __name__
    implements(IFudresultView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def getSearchItems(self):
        """ test method"""
        context = self.context
        request = self.request
        context_path = ('/').join(context.getPhysicalPath())
        compositeQuery = And()
        zcatQuery = {}
        subQuery = None
        if request.DocType:
            zcatQuery['portal_type'] = request.DocType
        textQuery = self.__createTextQuery()
        if textQuery:
            zcatQuery['SearchableText'] = textQuery
        if zcatQuery:
            subQuery = self.portal_catalog.makeAdvancedQuery(zcatQuery)
        if subQuery:
            compositeQuery.addSubquery(subQuery)
        if request.creators:
            if request.coop:
                creatorsQuery = And()
            else:
                creatorsQuery = Or()
            if isinstance(request.creators, str):
                creators = [
                 request.creators]
            else:
                creators = request.creators
            for rc in creators:
                creatorsQuery.addSubquery(Eq('listCreators', rc))

            compositeQuery.addSubquery(creatorsQuery)
        if request.notcreators:
            if isinstance(request.notcreators, str):
                creators = [
                 request.notcreators]
            else:
                creators = request.notcreators
            for rc in creators:
                compositeQuery.addSubquery(~Eq('listCreators', rc))

        if request.SortBy:
            sortCriteria = request.SortBy.split()
            if sortCriteria[0] in ('Creator', 'created'):
                if len(sortCriteria) > 1:
                    if sortCriteria[1] == 'desc':
                        brains = self.portal_catalog.evalAdvancedQuery(compositeQuery, ((sortCriteria[0], sortCriteria[1]),))
                else:
                    brains = self.portal_catalog.evalAdvancedQuery(compositeQuery, (sortCriteria[0],))
        else:
            brains = self.portal_catalog.evalAdvancedQuery(compositeQuery)
        items = []
        for brain in brains:
            if brain.getPath() != context_path:
                items.append({'title': brain.Title, 'url': brain.getURL(), 'created': brain.created, 'Creators': brain.listCreators})

        return items

    def __listEqTuple(self, l, t):
        """Compare a list's content with a tuple's content"""
        if len(l) == len(t):
            for elem in l:
                if elem not in t:
                    return False

            return True
        else:
            return False

    def __listHasElemFromTuple(self, l, t):
        """Compare a list's content with a tuple's content"""
        for elem in l:
            if elem in t:
                return True
        else:
            return False

    def __createTextQuery(self):
        """
        returns the query for the search
        """
        request = self.request
        searchabletext = ''
        if request.AndWords:
            andwords = (' and ').join(request.AndWords.split())
        else:
            andwords = ''
        searchabletext += andwords
        if request.OrWords:
            if searchabletext:
                orwords = ' or ' + (' or ').join(request.OrWords.split())
            else:
                orwords = (' or ').join(request.OrWords.split())
        else:
            orwords = ''
        searchabletext += orwords
        if request.Phrase:
            if searchabletext:
                phrase = ' and "' + (' ').join(request.Phrase.split()) + '"'
            else:
                phrase = '"' + (' ').join(request.Phrase.split()) + '"'
        else:
            phrase = ''
        searchabletext += phrase
        if request.NotWords:
            if searchabletext:
                notwords = ' and not ' + (' and not ').join(request.NotWords.split())
            else:
                notwords = ''
        else:
            notwords = ''
        searchabletext += notwords
        return searchabletext