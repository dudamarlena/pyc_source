# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/client/test_season_schedule.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 1063 bytes
from unittest import TestCase
from unittest.mock import patch, MagicMock
from requests import HTTPError, codes
from basketball_reference_web_scraper.client import season_schedule
from basketball_reference_web_scraper.errors import InvalidSeason

class TestSeasonSchedule(TestCase):

    @patch('basketball_reference_web_scraper.http_client.season_schedule')
    def test_not_found_raises_invalid_season(self, mocked_season_schedule):
        mocked_season_schedule.side_effect = HTTPError(response=MagicMock(status_code=(codes.not_found)))
        self.assertRaisesRegex(InvalidSeason,
          'Season end year of jaebaebae is invalid',
          season_schedule,
          season_end_year='jaebaebae')

    @patch('basketball_reference_web_scraper.http_client.season_schedule')
    def test_other_http_error_is_raised(self, mocked_season_schedule):
        mocked_season_schedule.side_effect = HTTPError(response=MagicMock(status_code=(codes.internal_server_error)))
        self.assertRaises(HTTPError, season_schedule, season_end_year=2018)