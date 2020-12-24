# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/catalog/browser/search.py
# Compiled at: 2008-10-06 10:31:12
from Acquisition import aq_inner
from zope.component import queryUtility
from zope.interface import implements
from zope.app.schema.vocabulary import IVocabularyFactory
from icsemantic.core.config import HAS_PLONE3
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import BrowserView
from icsemantic.thesaurus.Thesaurus import thesaurus_utility
from icsemantic.catalog.interfaces import IicSemanticManagementAdvancedSearchOptions
from icsemantic.catalog.browser.interfaces import IAdvancedSearch

class AdvancedSearch(BrowserView):
    """Add some custom functionality to the advanced search"""
    __module__ = __name__
    implements(IAdvancedSearch)

    def __init__(self, context, request):
        """Store the context and request in local variables"""
        self.context = context
        self.request = request

    def ontocatalog_fields_enabled(self):
        """Return True if the OntoCatalog options are enabled in the
        control panel.
        """
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        sm = portal.getSiteManager()
        pmas = sm.queryUtility(IicSemanticManagementAdvancedSearchOptions, name='icsemantic.advancedsearch')
        return pmas.include_ontocatalog_criteria

    def available_languages(self):
        """Return all the avalilable languages"""
        vocab = queryUtility(IVocabularyFactory, name='icsemantic.languages')
        return [ (i.token, i.title) for i in vocab(self.context) ]

    def contexts(self):
        """Return all the contexts in the thesaurus"""
        t = thesaurus_utility()
        return t.contexts()