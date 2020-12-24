# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/html/test_player_advanced_season_totals_table.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 1704 bytes
from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock
from unittest.mock import patch
from basketball_reference_web_scraper.html import PlayerAdvancedSeasonTotalsRow, PlayerAdvancedSeasonTotalsTable

class TestPlayerAdvancedSeasonTotalsTable(TestCase):

    def setUp(self):
        self.html = MagicMock()

    def test_rows_query_after_stripping_whitespace(self):
        self.assertEqual('\n            //table[@id="advanced_stats"]\n            /tbody\n            /tr[\n                contains(@class, "full_table") or \n                contains(@class, "italic_text partial_table") \n                and not(contains(@class, "rowSum"))\n            ]\n            '.strip(), PlayerAdvancedSeasonTotalsTable(html=(self.html)).rows_query.strip())

    @patch.object(PlayerAdvancedSeasonTotalsRow, 'is_combined_totals', new_callable=PropertyMock, return_value=False)
    def test_returns_all_rows_when_rows_are_not_combined_totals_rows(self, _):
        first_html_row = MagicMock()
        html_rows = [first_html_row]
        self.html.xpath = MagicMock(return_value=html_rows)
        rows = PlayerAdvancedSeasonTotalsTable(self.html).get_rows()
        self.assertTrue(len(html_rows) == len(rows))

    @patch.object(PlayerAdvancedSeasonTotalsRow, 'is_combined_totals', new_callable=PropertyMock, return_value=True)
    def test_returns_no_rows_when_all_rows_are_combined_totals_rows(self, _):
        first_html_row = MagicMock()
        html_rows = [first_html_row]
        self.html.xpath = MagicMock(return_value=html_rows)
        rows = PlayerAdvancedSeasonTotalsTable(self.html).get_rows()
        self.assertTrue(0 == len(rows))