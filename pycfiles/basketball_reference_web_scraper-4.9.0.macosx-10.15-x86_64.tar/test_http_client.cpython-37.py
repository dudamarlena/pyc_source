# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/test_http_client.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 672 bytes
from unittest import TestCase, mock
from requests import codes
from basketball_reference_web_scraper import http_client
from basketball_reference_web_scraper.errors import InvalidDate

class TestHttpClient(TestCase):

    @mock.patch('requests.get')
    def test_player_box_scores_raises_invalid_date_for_300_response(self, mocked_get):
        response = mock.Mock(status_code=(codes.multiple_choices))
        mocked_get.return_value = response
        self.assertRaisesRegex(InvalidDate,
          'Date with year set to 2018, month set to 1, and day set to 1 is invalid',
          (http_client.player_box_scores),
          day=1,
          month=1,
          year=2018)