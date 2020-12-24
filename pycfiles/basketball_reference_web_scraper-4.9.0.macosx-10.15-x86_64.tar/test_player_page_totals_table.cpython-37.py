# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/html/test_player_page_totals_table.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 1607 bytes
from unittest import TestCase
from unittest.mock import MagicMock
from basketball_reference_web_scraper.html import PlayerPageTotalsTable, PlayerPageTotalsRow

class TestPlayerPageTotalsTable(TestCase):

    def test_rows_are_empty_array_when_no_results(self):
        html = MagicMock()
        html.xpath = MagicMock(return_value=[])
        self.assertEqual(PlayerPageTotalsTable(html=html).rows, [])
        html.xpath.assert_called_once_with('.//tbody/tr')

    def test_rows_when_results(self):
        first_row = MagicMock(name='first row html')
        second_row = MagicMock(name='second row html')
        html = MagicMock()
        html.xpath = MagicMock(return_value=[first_row, second_row])
        self.assertEqual(PlayerPageTotalsTable(html=html).rows, [
         PlayerPageTotalsRow(html=first_row),
         PlayerPageTotalsRow(html=second_row)])
        html.xpath.assert_called_once_with('.//tbody/tr')

    def test_different_class_is_not_equal(self):
        self.assertNotEqual(PlayerPageTotalsTable(html=(MagicMock())), 'jaebaebae')

    def test_different_html_but_same_class_is_not_equal(self):
        self.assertNotEqual(PlayerPageTotalsTable(html=(MagicMock())), PlayerPageTotalsTable(html=(MagicMock())))

    def test_same_html_and_same_class_is_equal(self):
        html = MagicMock()
        self.assertEqual(PlayerPageTotalsTable(html=html), PlayerPageTotalsTable(html=html))