# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/test_time_format.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 4078 bytes
"""Test time_format.py
"""
import os, time, unittest
from pyutil import time_format, increasing_timer

class TimeUtilTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_iso8601_utc_time(self, timer=increasing_timer.timer):
        ts1 = time_format.iso_utc(timer.time() - 20)
        ts2 = time_format.iso_utc()
        assert ts1 < ts2, 'failed: %s < %s' % (ts1, ts2)
        ts3 = time_format.iso_utc(timer.time() + 20)
        assert ts2 < ts3, 'failed: %s < %s' % (ts2, ts3)

    def test_iso_utc_time_to_localseconds(self, timer=increasing_timer.timer):
        t1 = int(timer.time() - 438000.0)
        iso_utc_t1 = time_format.iso_utc(t1)
        t1_2 = time_format.iso_utc_time_to_seconds(iso_utc_t1)
        assert t1 == t1_2, (t1, t1_2)
        t1 = int(timer.time() - 876000.0)
        iso_utc_t1 = time_format.iso_utc(t1)
        t1_2 = time_format.iso_utc_time_to_seconds(iso_utc_t1)
        self.assertEqual(t1, t1_2)
        t1 = int(timer.time())
        iso_utc_t1 = time_format.iso_utc(t1)
        t1_2 = time_format.iso_utc_time_to_seconds(iso_utc_t1)
        self.assertEqual(t1, t1_2)

    def test_epoch(self):
        return self._help_test_epoch()

    def test_epoch_in_London(self):
        origtz = os.environ.get('TZ')
        os.environ['TZ'] = 'Europe/London'
        if hasattr(time, 'tzset'):
            time.tzset()
        try:
            return self._help_test_epoch()
        finally:
            if origtz is None:
                del os.environ['TZ']
            else:
                os.environ['TZ'] = origtz
            if hasattr(time, 'tzset'):
                time.tzset()

    def _help_test_epoch(self):
        origtzname = time.tzname
        s = time_format.iso_utc_time_to_seconds('1970-01-01T00:00:01Z')
        self.assertEqual(s, 1.0)
        s = time_format.iso_utc_time_to_seconds('1970-01-01_00:00:01Z')
        self.assertEqual(s, 1.0)
        s = time_format.iso_utc_time_to_seconds('1970-01-01 00:00:01Z')
        self.assertEqual(s, 1.0)
        self.assertEqual(time_format.iso_utc(1.0), '1970-01-01 00:00:01Z')
        self.assertEqual(time_format.iso_utc(1.0, sep='_'), '1970-01-01_00:00:01Z')
        now = time.time()
        isostr = time_format.iso_utc(now)
        timestamp = time_format.iso_utc_time_to_seconds(isostr)
        self.assertEqual(int(timestamp), int(now))

        def my_time():
            return 1.0

        self.assertEqual(time_format.iso_utc(t=my_time), '1970-01-01 00:00:01Z')
        self.assertRaises(ValueError, time_format.iso_utc_time_to_seconds, 'invalid timestring')
        s = time_format.iso_utc_time_to_seconds('1970-01-01 00:00:01.500Z')
        self.assertEqual(s, 1.5)
        thatmomentinmarch = time_format.iso_utc_time_to_seconds('2009-03-20 21:49:02.226536Z')
        self.assertEqual(thatmomentinmarch, 1237585742.226536)
        self.assertEqual(origtzname, time.tzname)