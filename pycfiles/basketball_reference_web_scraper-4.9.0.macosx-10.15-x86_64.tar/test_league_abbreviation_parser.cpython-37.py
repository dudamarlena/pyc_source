# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/parsers/test_league_abbreviation_parser.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 2358 bytes
from unittest import TestCase
from basketball_reference_web_scraper.data import League, LEAGUE_ABBREVIATIONS_TO_LEAGUE
from basketball_reference_web_scraper.parsers import LeagueAbbreviationParser

class TestLeagueAbbreviationParser(TestCase):

    def setUp(self):
        self.parser = LeagueAbbreviationParser(abbreviations_to_league=LEAGUE_ABBREVIATIONS_TO_LEAGUE)

    def test_parsing_unknown_abbreviation(self):
        self.assertRaisesRegex(ValueError,
          'Unknown league abbreviation: jaebaebae',
          (self.parser.from_abbreviation),
          abbreviation='jaebaebae')

    def test_parsing_nba(self):
        self.assertEqual(self.parser.from_abbreviation(abbreviation='NBA'), League.NATIONAL_BASKETBALL_ASSOCIATION)

    def test_parsing_aba(self):
        self.assertEqual(self.parser.from_abbreviation(abbreviation='ABA'), League.AMERICAN_BASKETBALL_ASSOCIATION)

    def test_parsing_baa(self):
        self.assertEqual(self.parser.from_abbreviation(abbreviation='BAA'), League.BASKETBALL_ASSOCIATION_OF_AMERICA)

    def test_from_abbreviations_when_abbreviations_is_none(self):
        self.assertEqual(self.parser.from_abbreviations(abbreviations=None), [])

    def test_from_abbreviations_parsing_single_league(self):
        self.assertEqual(self.parser.from_abbreviations(abbreviations='NBA'), [
         League.NATIONAL_BASKETBALL_ASSOCIATION])

    def test_from_abbreviations_parsing_aba(self):
        self.assertEqual(self.parser.from_abbreviations(abbreviations='ABA'), [
         League.AMERICAN_BASKETBALL_ASSOCIATION])

    def test_from_abbreviations_parsing_baa(self):
        self.assertEqual(self.parser.from_abbreviations(abbreviations='BAA'), [
         League.BASKETBALL_ASSOCIATION_OF_AMERICA])

    def test_from_abbreviations_parsing_nba_aba_baa(self):
        self.assertEqual(self.parser.from_abbreviations(abbreviations='NBA/ABA/BAA'), [
         League.NATIONAL_BASKETBALL_ASSOCIATION,
         League.AMERICAN_BASKETBALL_ASSOCIATION,
         League.BASKETBALL_ASSOCIATION_OF_AMERICA])