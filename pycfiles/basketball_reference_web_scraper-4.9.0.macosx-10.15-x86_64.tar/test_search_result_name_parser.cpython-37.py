# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/parsers/test_search_result_name_parser.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 817 bytes
from unittest import TestCase
from basketball_reference_web_scraper.parsers import SearchResultNameParser

class TestSearchResultNameParser(TestCase):

    def setUp(self):
        self.parser = SearchResultNameParser()

    def test_parse_name_with_parentheses_with_start_and_end_year(self):
        self.assertEqual(self.parser.parse(search_result_name='Kobe Bryant (1997-2016)'), 'Kobe Bryant')

    def test_parse_name_with_parentheses_with_start_year(self):
        self.assertEqual(self.parser.parse(search_result_name='Bud Koper (1965)'), 'Bud Koper')

    def test_parse_name_without_parentheses(self):
        self.assertEqual(self.parser.parse(search_result_name='Bronson Koenig'), 'Bronson Koenig')