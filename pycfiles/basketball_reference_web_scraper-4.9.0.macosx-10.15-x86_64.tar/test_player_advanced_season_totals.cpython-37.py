# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/client/test_player_advanced_season_totals.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 1286 bytes
from unittest import TestCase
from unittest.mock import patch, MagicMock
from requests import HTTPError, codes
from basketball_reference_web_scraper.client import players_advanced_season_totals
from basketball_reference_web_scraper.errors import InvalidSeason

class TestPlayerAdvancedSeasonTotals(TestCase):

    @patch('basketball_reference_web_scraper.http_client.players_advanced_season_totals')
    def test_not_found_raises_invalid_season(self, mocked_players_advanced_season_totals):
        end_year = 'jaebaebae'
        expected_message = 'Season end year of {end_year} is invalid'.format(end_year=end_year)
        mocked_players_advanced_season_totals.side_effect = HTTPError(response=MagicMock(status_code=(codes.not_found)))
        self.assertRaisesRegex(InvalidSeason, expected_message, players_advanced_season_totals, season_end_year=end_year)

    @patch('basketball_reference_web_scraper.http_client.players_advanced_season_totals')
    def test_other_http_error_is_raised(self, mocked_players_advanced_season_totals):
        mocked_players_advanced_season_totals.side_effect = HTTPError(response=MagicMock(status_code=(codes.internal_server_error)))
        self.assertRaises(HTTPError, players_advanced_season_totals, season_end_year=2018)