# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/tests/test_portal_properties.py
# Compiled at: 2018-10-18 17:35:14
from brasil.gov.portal.config import LOCAL_LONG_TIME_FORMAT
from brasil.gov.portal.config import LOCAL_TIME_FORMAT
from brasil.gov.portal.testing import INTEGRATION_TESTING
import unittest
SELECTABLE_VIEWS = ('listing_view', 'news_listing')

class PortalPropertiesTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.properties = self.portal['portal_properties'].site_properties
        self.languages = self.portal['portal_languages']
        self.types = self.portal['portal_types']

    def test_localTimeFormat(self):
        self.assertEqual(self.properties.localTimeFormat, LOCAL_TIME_FORMAT)

    def test_localLongTimeFormat(self):
        self.assertEqual(self.properties.localLongTimeFormat, LOCAL_LONG_TIME_FORMAT)

    def test_enable_link_integrity_checks_enabled(self):
        self.assertTrue(self.properties.enable_link_integrity_checks)

    def test_livesearch_disabled(self):
        self.assertFalse(self.properties.enable_livesearch)

    def test_default_language(self):
        self.assertTrue(self.languages.use_combined_language_codes)
        self.assertEqual(self.properties.default_language, 'pt-br')

    def test_default_charset(self):
        self.assertEqual(self.properties.default_charset, 'utf-8')

    def test_types_searched(self):
        all_types = set(self.types.listContentTypes())
        types_not_searched = set(self.properties.types_not_searched)
        types_searched = list(all_types - types_not_searched)
        types_searched.sort()
        types_expected = [
         'AgendaDiaria',
         'Audio',
         'Document',
         'Event',
         'ExternalContent',
         'File',
         'Image',
         'Infographic',
         'Link',
         'collective.nitf.content',
         'collective.polls.poll',
         'sc.embedder']
        self.assertListEqual(types_searched, types_expected)

    def test_metaTypesNotToList(self):
        from zope.component import getUtility
        from zope.schema.interfaces import IVocabularyFactory
        types = getUtility(IVocabularyFactory, 'plone.app.vocabularies.PortalTypes')(None)
        types = set(t.value for t in types)
        navtree = self.portal['portal_properties'].navtree_properties
        exclude = set(navtree.metaTypesNotToList)
        expected = {
         'Document',
         'Folder',
         'FormFolder'}
        self.assertSetEqual(types - exclude, expected)
        return

    def test_selectable_views(self):
        selectable_views_property = self.portal.getProperty('selectable_views')
        self.assertTupleEqual(selectable_views_property, SELECTABLE_VIEWS)

    def test_dropdown_depth(self):
        dropdown = self.portal['portal_properties'].dropdown_properties
        self.assertEqual(dropdown.dropdown_depth, 1)