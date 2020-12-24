# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/parsers/test_location_abbreviation_parser.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 750 bytes
from unittest import TestCase
from basketball_reference_web_scraper.data import Location, LOCATION_ABBREVIATIONS_TO_POSITION
from basketball_reference_web_scraper.parsers import LocationAbbreviationParser

class TestLocationAbbreviationParser(TestCase):

    def setUp(self):
        self.parser = LocationAbbreviationParser(abbreviations_to_locations=LOCATION_ABBREVIATIONS_TO_POSITION)

    def test_parse_away_symbol(self):
        self.assertEqual(Location.AWAY, self.parser.from_abbreviation('@'))

    def test_parse_home_symbol(self):
        self.assertEqual(Location.HOME, self.parser.from_abbreviation(''))

    def test_parse_unknown_location_symbol(self):
        self.assertRaises(ValueError, self.parser.from_abbreviation, 'jaebaebae')