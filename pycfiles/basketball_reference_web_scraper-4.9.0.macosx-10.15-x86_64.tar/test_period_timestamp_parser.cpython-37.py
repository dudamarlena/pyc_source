# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/parsers/test_period_timestamp_parser.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 605 bytes
from unittest import TestCase
from basketball_reference_web_scraper.http_client import PLAY_BY_PLAY_TIMESTAMP_FORMAT
from basketball_reference_web_scraper.parsers import PeriodTimestampParser

class TestPeriodTimestampParser(TestCase):

    def setUp(self):
        self.parser = PeriodTimestampParser(timestamp_format=PLAY_BY_PLAY_TIMESTAMP_FORMAT)

    def test_less_than_a_minute_to_seconds(self):
        self.assertEqual(32.1, self.parser.to_seconds(timestamp='0:32.1'))

    def test_more_than_a_minute_to_seconds(self):
        self.assertEqual(684.5, self.parser.to_seconds(timestamp='11:24.5'))