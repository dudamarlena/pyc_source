# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/parsers/test_player_box_score_outcome_parser.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 2552 bytes
from unittest import TestCase
from basketball_reference_web_scraper.data import OUTCOME_ABBREVIATIONS_TO_OUTCOME, Outcome
from basketball_reference_web_scraper.parsers import OutcomeAbbreviationParser, PlayerBoxScoreOutcomeParser

class TestPlayerBoxScoreOutcomeParser(TestCase):

    def setUp(self):
        self.parser = PlayerBoxScoreOutcomeParser(outcome_abbreviation_parser=OutcomeAbbreviationParser(abbreviations_to_outcomes=OUTCOME_ABBREVIATIONS_TO_OUTCOME))

    def test_parse_win_abbreviation_for_single_digit_margin_of_victory(self):
        self.assertEqual('W', self.parser.parse_outcome_abbreviation(formatted_outcome='W (+8)'))

    def test_parse_win_abbreviation_for_double_digit_margin_of_victory(self):
        self.assertEqual('W', self.parser.parse_outcome_abbreviation(formatted_outcome='W (+18)'))

    def test_parse_loss_abbreviation_for_single_digit_margin_of_victory(self):
        self.assertEqual('L', self.parser.parse_outcome_abbreviation(formatted_outcome='L (-8)'))

    def test_parse_loss_abbreviation_for_double_digit_margin_of_victory(self):
        self.assertEqual('L', self.parser.parse_outcome_abbreviation(formatted_outcome='L (-18)'))

    def test_parse_win_outcome_for_single_digit_margin_of_victory(self):
        self.assertEqual(Outcome.WIN, self.parser.parse_outcome(formatted_outcome='W (+8)'))

    def test_parse_win_outcome_for_double_digit_margin_of_victory(self):
        self.assertEqual(Outcome.WIN, self.parser.parse_outcome(formatted_outcome='W (+18)'))

    def test_parse_loss_outcome_for_single_digit_margin_of_victory(self):
        self.assertEqual(Outcome.LOSS, self.parser.parse_outcome(formatted_outcome='L (-8)'))

    def test_parse_loss_outcome_for_double_digit_margin_of_victory(self):
        self.assertEqual(Outcome.LOSS, self.parser.parse_outcome(formatted_outcome='L (-18)'))

    def test_parse_positive_single_digit_margin_of_victory(self):
        self.assertEqual(8, self.parser.parse_margin_of_victory(formatted_outcome='W (+8)'))

    def test_parse_positive_double_digit_margin_of_victory(self):
        self.assertEqual(18, self.parser.parse_margin_of_victory(formatted_outcome='W (+18)'))

    def test_parse_negative_single_digit_margin_of_victory(self):
        self.assertEqual(-8, self.parser.parse_margin_of_victory(formatted_outcome='L (-8)'))

    def test_parse_negative_double_digit_margin_of_victory(self):
        self.assertEqual(-18, self.parser.parse_margin_of_victory(formatted_outcome='L (-18)'))