# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/parsers/test_team_totals_parser.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 911 bytes
from unittest import TestCase
from unittest.mock import MagicMock
from basketball_reference_web_scraper.parsers import TeamTotalsParser, TeamAbbreviationParser
from basketball_reference_web_scraper.data import Outcome, TeamTotal, TEAM_ABBREVIATIONS_TO_TEAM

class TestTeamTotalsParser(TestCase):

    def setUp(self):
        self.parser = TeamTotalsParser(team_abbreviation_parser=TeamAbbreviationParser(abbreviations_to_teams=TEAM_ABBREVIATIONS_TO_TEAM))

    def test_parse_none_outcome_when_points_are_same(self):
        team_totals = TeamTotal(team_abbreviation='BOS', totals=MagicMock(points='100'))
        opposing_team_totals = TeamTotal(team_abbreviation='GSW', totals=MagicMock(points='100'))
        self.assertIsNone(self.parser.parse_totals(team_totals=team_totals, opposing_team_totals=opposing_team_totals)['outcome'])