# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/html/test_search_result.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 3391 bytes
from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock, patch
from basketball_reference_web_scraper.html import SearchResult

class TestSearchResult(TestCase):

    def test_resource_link_query(self):
        self.assertEqual(SearchResult(html=(MagicMock())).resource_link_query, './div[@class="search-item-name"]//a')

    @patch.object(SearchResult, 'resource_link_query', new_callable=PropertyMock)
    def test_resource_link_when_no_matching_links(self, mocked_query):
        mocked_query.return_value = 'some query'
        html = MagicMock()
        html.xpath = MagicMock(return_value=[])
        self.assertIsNone(SearchResult(html=html).resource_link)
        html.xpath.assert_called_once_with('some query')

    @patch.object(SearchResult, 'resource_link_query', new_callable=PropertyMock)
    def test_resource_link_when_matching_links(self, mocked_query):
        mocked_query.return_value = 'some query'
        first_link = MagicMock()
        html = MagicMock()
        html.xpath = MagicMock(return_value=[first_link])
        self.assertEqual(SearchResult(html=html).resource_link, first_link)
        html.xpath.assert_called_once_with('some query')

    @patch.object(SearchResult, 'resource_link', new_callable=PropertyMock)
    def test_resource_location_when_resource_link_is_none(self, mocked_resource_link):
        mocked_resource_link.return_value = None
        self.assertIsNone(SearchResult(html=(MagicMock())).resource_location)

    @patch.object(SearchResult, 'resource_link', new_callable=PropertyMock)
    def test_resource_location_when_resource_link_is_not_none(self, mocked_resource_link):
        link = MagicMock()
        link.attrib = MagicMock()
        link.attrib.__getitem__ = MagicMock(return_value='some href')
        mocked_resource_link.return_value = link
        self.assertEqual(SearchResult(html=(MagicMock())).resource_location, 'some href')
        link.attrib.__getitem__.assert_called_once_with('href')

    @patch.object(SearchResult, 'resource_link', new_callable=PropertyMock)
    def test_resource_name_when_resource_link_is_none(self, mocked_resource_link):
        mocked_resource_link.return_value = None
        self.assertIsNone(SearchResult(html=(MagicMock())).resource_name)

    @patch.object(SearchResult, 'resource_link', new_callable=PropertyMock)
    def test_resource_name_when_resource_link_is_not_none(self, mocked_resource_link):
        link = MagicMock()
        link.text_content = MagicMock(return_value='some content')
        mocked_resource_link.return_value = link
        self.assertEqual(SearchResult(html=(MagicMock())).resource_name, 'some content')
        link.text_content.assert_called_once_with()

    def test_different_class_is_not_equal(self):
        self.assertNotEqual(SearchResult(html=(MagicMock())), 'jaebaebae')

    def test_different_html_but_same_class_is_not_equal(self):
        self.assertNotEqual(SearchResult(html=(MagicMock())), SearchResult(html=(MagicMock())))

    def test_same_html_and_same_class_is_equal(self):
        html = MagicMock()
        self.assertEqual(SearchResult(html=html), SearchResult(html=html))