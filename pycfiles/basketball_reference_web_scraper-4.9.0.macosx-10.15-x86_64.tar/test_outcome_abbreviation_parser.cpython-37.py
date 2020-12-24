# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/parsers/test_outcome_abbreviation_parser.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 724 bytes
from unittest import TestCase
from basketball_reference_web_scraper.data import Outcome, OUTCOME_ABBREVIATIONS_TO_OUTCOME
from basketball_reference_web_scraper.parsers import OutcomeAbbreviationParser

class TestOutcomeAbbreviationParser(TestCase):

    def setUp(self):
        self.parser = OutcomeAbbreviationParser(abbreviations_to_outcomes=OUTCOME_ABBREVIATIONS_TO_OUTCOME)

    def test_parse_unknown_outcome_symbol(self):
        self.assertRaises(ValueError, self.parser.from_abbreviation, 'jaebaebae')

    def test_parse_win(self):
        self.assertEqual(Outcome.WIN, self.parser.from_abbreviation('W'))

    def test_parse_loss(self):
        self.assertEqual(Outcome.LOSS, self.parser.from_abbreviation('L'))