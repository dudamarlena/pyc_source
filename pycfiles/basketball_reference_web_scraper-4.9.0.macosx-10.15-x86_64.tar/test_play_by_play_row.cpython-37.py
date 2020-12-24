# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/html/test_play_by_play_row.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 862 bytes
from unittest import TestCase
from unittest.mock import patch, PropertyMock, MagicMock
from basketball_reference_web_scraper.html import PlayByPlayRow

class TestPlayByPlayRow(TestCase):

    @patch.object(PlayByPlayRow, 'home_team_play_description', new_callable=PropertyMock)
    def test_is_home_team_play_when_home_team_play_description_is_not_empty_string(self, mocked_play_description):
        mocked_play_description.return_value = 'jaebaebae'
        self.assertTrue(PlayByPlayRow(html=(MagicMock())).is_home_team_play)

    @patch.object(PlayByPlayRow, 'home_team_play_description', new_callable=PropertyMock)
    def test_is_not_home_team_play_when_home_team_play_description_is_empty_string(self, mocked_play_description):
        mocked_play_description.return_value = ''
        self.assertFalse(PlayByPlayRow(html=(MagicMock())).is_home_team_play)