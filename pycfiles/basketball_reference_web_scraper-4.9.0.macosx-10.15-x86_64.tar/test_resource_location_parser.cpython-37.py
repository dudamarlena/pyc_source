# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/parsers/test_resource_location_parser.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 2024 bytes
from unittest import TestCase
from basketball_reference_web_scraper.http_client import SEARCH_RESULT_RESOURCE_LOCATION_REGEX
from basketball_reference_web_scraper.parsers import ResourceLocationParser

class TestResourceLocationParser(TestCase):

    def setUp(self):
        self.parser = ResourceLocationParser(resource_location_regex=SEARCH_RESULT_RESOURCE_LOCATION_REGEX)

    def test_parse_players_resource_type(self):
        self.assertEqual(self.parser.parse_resource_type(resource_location='https://www.basketball-reference.com/players/k/koperbu01.html'), 'players')

    def test_parse_coaches_resource_type(self):
        self.assertEqual(self.parser.parse_resource_type(resource_location='https://www.basketball-reference.com/coaches/vanbrbu01c.html'), 'coaches')

    def test_parse_executives_resource_type(self):
        self.assertEqual(self.parser.parse_resource_type(resource_location='https://www.basketball-reference.com/executives/vanbrbu01x.html'), 'executives')

    def test_parse_players_resource_identifier(self):
        self.assertEqual(self.parser.parse_resource_identifier(resource_location='https://www.basketball-reference.com/players/k/koperbu01.html'), 'koperbu01')

    def test_parse_coaches_resource_identifier(self):
        self.assertEqual(self.parser.parse_resource_identifier(resource_location='https://www.basketball-reference.com/coaches/vanbrbu01c.html'), 'vanbrbu01c')

    def test_parse_executives_resource_identifier(self):
        self.assertEqual(self.parser.parse_resource_identifier(resource_location='https://www.basketball-reference.com/executives/vanbrbu01x.html'), 'vanbrbu01x')