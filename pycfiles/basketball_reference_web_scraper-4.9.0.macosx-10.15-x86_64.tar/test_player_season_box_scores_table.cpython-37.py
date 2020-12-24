# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/html/test_player_season_box_scores_table.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 726 bytes
from unittest import TestCase
from unittest.mock import MagicMock
from basketball_reference_web_scraper.html import PlayerSeasonBoxScoresTable

class TestPlayerSeasonBoxScoresTable(TestCase):

    def setUp(self):
        self.html = MagicMock()

    def test_rows_query_raises_not_implemented_error(self):
        table = PlayerSeasonBoxScoresTable(html=(self.html))
        self.assertRaises(NotImplementedError, lambda : table.rows_query)

    def test_rows_raises_not_implemented_error_when_rows_query_is_not_overridden(self):
        table = PlayerSeasonBoxScoresTable(html=(self.html))
        self.assertRaises(NotImplementedError, lambda : table.rows)