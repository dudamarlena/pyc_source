# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/tests/test_dates.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.util.dates."""
from __future__ import unicode_literals
from datetime import datetime
import pytz
from djblets.testing.testcases import TestCase
from djblets.util.dates import get_latest_timestamp, get_tz_aware_utcnow, http_date

class DatesTests(TestCase):
    """Unit tests for djblets.util.dates."""

    def test_http_date_with_datetime(self):
        """Testing http_date with datetime"""
        date_time = datetime(2016, 8, 26, 3, 3, 26, 123456)
        self.assertEqual(http_date(date_time), b'Fri, 26 Aug 2016 03:03:26 GMT')

    def test_http_date_with_date_string(self):
        """Testing http_date with date string"""
        date = b'20/06/2016'
        self.assertEqual(http_date(date), date)

    def test_http_date_with_unix_timestamp(self):
        """Testing http_date with unix timestamp"""
        unix_timestamp = b'1466424000'
        self.assertEqual(http_date(unix_timestamp), unix_timestamp)

    def test_get_latest_timestamp_with_empty_list(self):
        """Testing get_latest_timestamp without any timestamps in the list"""
        self.assertIsNone(get_latest_timestamp([]))

    def test_get_latest_timestamp_with_jumbled_list(self):
        """Testing get_latest_timestamp with unsorted date time
        list.
         """
        self.assertEqual(get_latest_timestamp([
         b'1453204800',
         b'1466337600',
         b'1466424000']), b'1466424000')

    def test_date_time_is_in_utc(self):
        """Testing get_tz_aware_utcnow returns UTC time."""
        utc_time = get_tz_aware_utcnow()
        self.assertEqual(utc_time.tzinfo, pytz.utc)