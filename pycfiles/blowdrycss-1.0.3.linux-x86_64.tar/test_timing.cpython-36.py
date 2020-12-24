# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/unit_tests/test_timing.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 3429 bytes
from __future__ import absolute_import
from unittest import TestCase, main
import sys
from datetime import datetime
from time import time, sleep
from string import digits
from io import StringIO
from blowdrycss.timing import Timer, LimitTimer
from blowdrycss.utilities import change_settings_for_testing
import blowdrycss_settings as settings
change_settings_for_testing()
__author__ = 'chad nelson'
__project__ = 'blowdrycss'

class TestTiming(TestCase):

    def test_seconds_to_string(self):
        timer = Timer()
        allowed = set(digits + '.')
        time_string = timer.seconds_to_string(seconds_elapsed=(time()))
        self.assertTrue(set(time_string) <= allowed)

    def test_elapsed_end_set(self):
        timer = Timer()
        allowed = set(digits + '.eE-+')
        timer.end = time()
        self.assertTrue((set(timer.elapsed) <= allowed), msg=(str(timer.elapsed) + '\nAllowed: ' + str(allowed)))

    def test_elapsed_end_not_set(self):
        timer = Timer()
        allowed = set(digits + '.eE-+')
        self.assertTrue((set(timer.elapsed) <= allowed), msg=(str(timer.elapsed) + '\nAllowed: ' + str(allowed)))

    def test_print_time(self):
        timer = Timer()
        substrings = [
         'Completed ', 'It took:', 'seconds', '=====', '.', str(datetime.now().year), str(datetime.now().month),
         str(datetime.now().day)]
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            timer.print_time()
            output = out.getvalue()
            for substring in substrings:
                self.assertTrue((substring in output), msg=substring)

        finally:
            sys.stdout = saved_stdout

    def test_report(self):
        timer = Timer()
        substrings = [
         'Completed ', 'It took:', 'seconds', '=====', '.', str(datetime.now().year), str(datetime.now().month),
         str(datetime.now().day)]
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            timer.report()
            output = out.getvalue()
            for substring in substrings:
                self.assertTrue((substring in output), msg=substring)

        finally:
            sys.stdout = saved_stdout

    def test_limit_exceeded(self):
        time_limit = settings.time_limit
        settings.time_limit = 0.0001
        limit_timer = LimitTimer()
        sleep(0.001)
        self.assertTrue((limit_timer.limit_exceeded), msg=(limit_timer.start_time))
        settings.time_limit = time_limit

    def test_reset(self):
        limit_timer = LimitTimer()
        start1 = limit_timer.start_time
        sleep(0.001)
        limit_timer.reset()
        start2 = limit_timer.start_time
        self.assertTrue(start1 < start2)


if __name__ == '__main__':
    main()