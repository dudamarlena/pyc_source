# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/html/test_regular_season_player_box_scores_table.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 1262 bytes
from unittest import TestCase
from unittest.mock import MagicMock
from basketball_reference_web_scraper.html import RegularSeasonPlayerBoxScoresTable, PlayerSeasonBoxScoresRow

class TestRegularSeasonPlayerBoxScoresTable(TestCase):

    def setUp(self):
        self.html = MagicMock()

    def test_rows_query(self):
        self.assertEqual('//tbody/tr[not(contains(@class, "thead"))]', RegularSeasonPlayerBoxScoresTable(html=(self.html)).rows_query)

    def test_rows_returns_empty_array_when_there_are_not_any_matching_rows(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertListEqual([], RegularSeasonPlayerBoxScoresTable(html=(self.html)).rows)

    def test_rows_returns_populated_array_when_there_are_matching_rows(self):
        first_row_html = MagicMock(name='first matching row html')
        second_row_html = MagicMock(name='second matching row html')
        self.html.xpath = MagicMock(return_value=[first_row_html, second_row_html])
        self.assertListEqual([
         PlayerSeasonBoxScoresRow(html=first_row_html),
         PlayerSeasonBoxScoresRow(html=second_row_html)], RegularSeasonPlayerBoxScoresTable(html=(self.html)).rows)