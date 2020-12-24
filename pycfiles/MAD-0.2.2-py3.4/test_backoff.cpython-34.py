# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\simulation\test_backoff.py
# Compiled at: 2016-04-22 02:31:06
# Size of source mod 2**32: 2131 bytes
from unittest import TestCase
from mock import patch
from mad.simulation.backoff import ConstantBackoff, ExponentialBackoff
BASE_DELAY = 25

class ConstantDelayTests(TestCase):

    def test_constant_delay(self):
        backoff = ConstantBackoff(BASE_DELAY)
        for attempts in range(10):
            self.assertEqual(backoff.delay(attempts), BASE_DELAY)


def fake_pick_up_to(limit):
    return limit


class ExponentialBackoffTests(TestCase):
    TEST_CASES = [{'attempts': 0,  'expected_delay': 0}, {'attempts': 1,  'expected_delay': BASE_DELAY}, {'attempts': 4,  'expected_delay': BASE_DELAY * fake_pick_up_to(15)}]

    def setUp(self):
        self.backoff = ExponentialBackoff(BASE_DELAY)

    @patch.object(ExponentialBackoff, '_pick_up_to', side_effect=fake_pick_up_to)
    def test_delay(self, mock):
        for each_case in self.TEST_CASES:
            self._do_test_delay(**each_case)

    def _do_test_delay(self, attempts, expected_delay):
        delay = self.backoff.delay(attempts)
        self.assertEqual(expected_delay, delay, 'Error! delay({0:d}) = {1:d} (found {2:d})'.format(attempts, expected_delay, delay))

    def test_pick_up_to(self):
        limit = BASE_DELAY * 31
        for i in range(100):
            delay = self.backoff.delay(5)
            self.assertGreaterEqual(limit, delay)