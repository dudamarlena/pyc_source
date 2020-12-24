# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/catalog/tests/test_searchview.py
# Compiled at: 2008-10-06 10:31:12
"""Test the search helper view
"""
import unittest
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.LinguaPlone.tests.utils import makeTranslation
from icsemantic.thesaurus.Thesaurus import thesaurus_utility
from icsemantic.catalog.tests.base import ICSemanticCatalogTestCase

class TestSearchView(ICSemanticCatalogTestCase):
    """Testing search view"""
    __module__ = __name__

    def test_contexts(self):
        """Test the contexts method"""
        t = thesaurus_utility()
        request = self.portal.REQUEST
        search_view = getMultiAdapter((self.portal, request), name='ontocatalog-advanced-search')
        self.assertEquals(t.contexts(), search_view.contexts())


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSearchView))
    return suite