# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/html/test_player_identification_row.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 2218 bytes
from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock
from basketball_reference_web_scraper.html import PlayerIdentificationRow

class TestPlayerIdentificationRow(TestCase):

    def setUp(self):
        self.html = MagicMock()

    def test_player_cell_when_cells_exist(self):
        cell = MagicMock()
        self.html.xpath = MagicMock(return_value=[cell])
        self.assertEqual(PlayerIdentificationRow(html=(self.html)).player_cell, cell)
        self.html.xpath.assert_called_once_with('td[@data-stat="player"]')

    def test_player_cell_is_none_when_cells_do_not_exist(self):
        self.html.xpath = MagicMock(return_value=[])
        self.assertIsNone(PlayerIdentificationRow(html=(self.html)).player_cell)
        self.html.xpath.assert_called_once_with('td[@data-stat="player"]')

    @patch.object(PlayerIdentificationRow, 'player_cell', new_callable=PropertyMock)
    def test_slug_when_player_cell_is_not_none(self, mocked_player_cell):
        cell = MagicMock(get=MagicMock(return_value='some slug'))
        mocked_player_cell.return_value = cell
        self.assertEqual(PlayerIdentificationRow(html=(self.html)).slug, 'some slug')
        cell.get.assert_called_once_with('data-append-csv')

    @patch.object(PlayerIdentificationRow, 'player_cell', new_callable=PropertyMock)
    def test_slug_when_player_cell_is_none(self, mocked_player_cell):
        mocked_player_cell.return_value = None
        self.assertEqual(PlayerIdentificationRow(html=(self.html)).slug, '')

    @patch.object(PlayerIdentificationRow, 'player_cell', new_callable=PropertyMock)
    def test_name_when_player_cell_is_not_none(self, mocked_player_cell):
        cell = MagicMock(text_content=MagicMock(return_value='some name'))
        mocked_player_cell.return_value = cell
        self.assertEqual(PlayerIdentificationRow(html=(self.html)).name, 'some name')
        cell.text_content.assert_called_once_with()

    @patch.object(PlayerIdentificationRow, 'player_cell', new_callable=PropertyMock)
    def test_name_when_player_cell_is_none(self, mocked_player_cell):
        mocked_player_cell.return_value = None
        self.assertEqual(PlayerIdentificationRow(html=(self.html)).name, '')