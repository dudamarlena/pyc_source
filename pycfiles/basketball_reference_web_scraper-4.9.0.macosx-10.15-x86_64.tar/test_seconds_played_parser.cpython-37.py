# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/parsers/test_seconds_played_parser.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 1144 bytes
from unittest import TestCase
from basketball_reference_web_scraper.parsers import SecondsPlayedParser

class TestSecondsPlayedParser(TestCase):

    def setUp(self):
        self.parser = SecondsPlayedParser()

    def test_parse_seconds_played_for_empty_string(self):
        self.assertEqual(0, self.parser.parse(''))

    def test_parse_seconds_played_for_0_seconds(self):
        self.assertEqual(1, self.parser.parse('0:01'))

    def test_parse_seconds_played_for_59_seconds(self):
        self.assertEqual(59, self.parser.parse('0:59'))

    def test_parse_seconds_played_for_60_seconds(self):
        self.assertEqual(60, self.parser.parse('1:00'))

    def test_parse_seconds_played_for_61_seconds(self):
        self.assertEqual(61, self.parser.parse('1:01'))

    def test_parse_seconds_played_for_59_minutes_59_seconds(self):
        self.assertEqual(3599, self.parser.parse('59:59'))

    def test_parse_seconds_played_for_60_minutes(self):
        self.assertEqual(3600, self.parser.parse('60:00'))

    def test_parse_seconds_played_for_60_minutes_and_1_second(self):
        self.assertEqual(3601, self.parser.parse('60:01'))