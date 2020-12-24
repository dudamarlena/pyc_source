# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/html/test_player_season_box_scores_page.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 1537 bytes
from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock, patch
from basketball_reference_web_scraper.html import PlayerSeasonBoxScoresPage

class TestPlayerSeasonBoxScoresPage(TestCase):

    def setUp(self):
        self.html = MagicMock()

    def test_regular_season_box_scores_table_query(self):
        self.assertEqual('//table[@id="pgl_basic"]', PlayerSeasonBoxScoresPage(html=(self.html)).regular_season_box_scores_table_query)

    @patch.object(PlayerSeasonBoxScoresPage, 'regular_season_box_scores_table_query', new_callable=PropertyMock)
    def test_regular_season_box_scores_table_is_none_when_no_matching_tables(self, mocked_query):
        mocked_query.return_value = 'foobar'
        self.html.xpath = MagicMock(return_value=[])
        self.assertIsNone(PlayerSeasonBoxScoresPage(html=(self.html)).regular_season_box_scores_table)
        self.html.xpath.assert_called_once_with('foobar')

    @patch.object(PlayerSeasonBoxScoresPage, 'regular_season_box_scores_table_query', new_callable=PropertyMock)
    def test_regular_season_box_scores_table_is_first_value_when_there_are_matching_tables(self, mocked_query):
        mocked_query.return_value = 'foobar'
        first_value = MagicMock(name='First Matching Table')
        self.html.xpath = MagicMock(return_value=[first_value])
        table = PlayerSeasonBoxScoresPage(html=(self.html)).regular_season_box_scores_table
        self.assertIsNotNone(table)
        self.assertEqual(first_value, table.html)