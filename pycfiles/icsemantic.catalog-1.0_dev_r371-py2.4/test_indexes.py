# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/catalog/tests/test_indexes.py
# Compiled at: 2008-10-06 10:31:12
"""Test the catalog indexes added by OntoCatalog.
"""
import unittest
from Products.CMFCore.utils import getToolByName
from Products.LinguaPlone.tests.utils import makeTranslation
from icsemantic.catalog.tests.base import ICSemanticCatalogTestCase

class TestICSemanticCatalogIndexes(ICSemanticCatalogTestCase):
    """Testing OntoCatalog indexes"""
    __module__ = __name__

    def afterSetUp(self):
        """Set up the test environment"""
        ICSemanticCatalogTestCase.afterSetUp(self)
        self.loginAsPortalOwner()
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.portal.invokeFactory('Document', 'football-player', title='Football Player', language='en')
        self.portal.invokeFactory('Document', 'balon-pie', title='Balón pie', language='es')
        page1 = getattr(self.portal, 'football-player')
        page1_es = makeTranslation(page1, 'es')
        page1_es.setTitle('Jugador')
        page1_es.setSubject(('fútbol', ))
        page1_es.reindexObject()

    def test_synonyms_index_search(self):
        """Test a catalog search using the SynonymIndex"""
        results = self.catalog(SearchableSynonymousText='soccer')
        self.assertEquals(len(results), 1)
        self.assertEquals(results[0].Title, 'Football Player')

    def test_translation_index_search(self):
        """Test a catalog search using the TranslationIndex"""
        self.login('member2')
        results = self.catalog(SearchableTranslatedText={'query': 'soccer', 'language': ('es', )})
        self.assertEquals(len(results), 2)
        titles = [ i.Title for i in results ]
        self.failUnless('Jugador' in titles)
        self.failUnless('Balón pie' in titles)

    def test_related_index_search(self):
        """Test the contexts parameter for the related criteria"""
        self.login('member2')
        results = self.catalog(SearchableRelatedText={'query': 'pelota', 'contexts': ('otro', )})
        self.assertEquals(len(results), 0)
        results = self.catalog(SearchableRelatedText={'query': 'pelota', 'contexts': ('publicidad', )})
        self.assertEquals(len(results), 1)
        self.assertEquals(results[0].Title, 'Balón pie')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestICSemanticCatalogIndexes))
    return suite