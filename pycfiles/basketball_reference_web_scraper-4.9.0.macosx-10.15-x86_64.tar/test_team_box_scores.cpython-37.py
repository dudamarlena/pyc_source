# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/client/test_team_box_scores.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 862 bytes
from unittest import TestCase
from unittest.mock import patch, MagicMock
import requests
from requests.exceptions import HTTPError
import basketball_reference_web_scraper.client as client
from basketball_reference_web_scraper.errors import InvalidDate

class TestTeamBoxScores(TestCase):

    @patch('basketball_reference_web_scraper.http_client.team_box_scores')
    def test_invalid_date_error_raised_for_unknown_date(self, mocked_http_team_box_scores):
        mocked_http_team_box_scores.side_effect = HTTPError(response=MagicMock(status_code=(requests.codes.not_found)))
        self.assertRaisesRegex(InvalidDate,
          'Date with year set to jae, month set to bae, and day set to bae is invalid',
          (client.team_box_scores),
          day='bae',
          month='bae',
          year='jae')