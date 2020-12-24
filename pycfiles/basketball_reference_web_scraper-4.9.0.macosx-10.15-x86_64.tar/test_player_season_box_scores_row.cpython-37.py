# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/html/test_player_season_box_scores_row.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 2642 bytes
from unittest import TestCase
from unittest.mock import MagicMock
from basketball_reference_web_scraper.html import PlayerSeasonBoxScoresRow

class TestPlayerSeasonBoxScoresRow(TestCase):

    def setUp(self):
        self.html = MagicMock()

    def test_not_equal_when_row_is_compared_against_non_row(self):
        self.assertNotEqual(1, PlayerSeasonBoxScoresRow(html=(MagicMock())))

    def test_not_equal_when_both_rows_but_different_html(self):
        self.assertNotEqual(PlayerSeasonBoxScoresRow(html=MagicMock(name='first html')), PlayerSeasonBoxScoresRow(html=MagicMock(name='second html')))

    def test_equal_when_both_rows_and_same_html(self):
        html = MagicMock(name='shared html')
        self.assertEqual(PlayerSeasonBoxScoresRow(html=html), PlayerSeasonBoxScoresRow(html=html))

    def test_is_active_is_false_when_cells_exist(self):
        cell = MagicMock()
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertFalse(PlayerSeasonBoxScoresRow(html=(self.html)).is_active)
        self.html.xpath.assert_called_once_with('td[@data-stat="reason"]')

    def test_is_active_is_true_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertTrue(PlayerSeasonBoxScoresRow(html=(self.html)).is_active)
        self.html.xpath.assert_called_once_with('td[@data-stat="reason"]')

    def test_date_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[MagicMock(text_content=MagicMock(return_value='some date'))])
        self.assertEqual(PlayerSeasonBoxScoresRow(html=(self.html)).date, 'some date')
        self.html.xpath.assert_called_once_with('td[@data-stat="date_game"]')

    def test_date_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerSeasonBoxScoresRow(html=(self.html)).date, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="date_game"]')

    def test_points_scored_when_cells_exist(self):
        self.html.xpath = MagicMock(return_value=[MagicMock(text_content=MagicMock(return_value='some points'))])
        self.assertEqual(PlayerSeasonBoxScoresRow(html=(self.html)).points_scored, 'some points')
        self.html.xpath.assert_called_once_with('td[@data-stat="pts"]')

    def test_points_scored_is_empty_string_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerSeasonBoxScoresRow(html=(self.html)).points_scored, '')
        self.html.xpath.assert_called_once_with('td[@data-stat="pts"]')