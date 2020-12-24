# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_repeat_timer.py
# Compiled at: 2016-04-06 13:00:20
from __future__ import absolute_import
import time, unittest
from mock import Mock
from ecmc.repeat_timer import RepeatTimer

class TestRepeatTimer(unittest.TestCase):

    def setUp(self):
        self.mock_func = Mock()

    def test_run_timer(self):
        self.timer = RepeatTimer('test_timer', 1, self.mock_func)
        self.timer.start()
        time.sleep(3)
        self.assertTrue(self.mock_func.call_count >= 2)

    def test_args(self):
        self.timer = RepeatTimer('test_timer', 1, self.mock_func, args=[1, 2])
        self.timer.start()
        time.sleep(2)
        self.mock_func.assert_called_with(1, 2)

    def test_kwargs(self):
        self.timer = RepeatTimer('test_timer', 1, self.mock_func, kwargs={'arg1': 3, 'arg2': 'foo'})
        self.timer.start()
        time.sleep(2)
        self.mock_func.assert_called_with(arg1=3, arg2='foo')

    def tearDown(self):
        self.timer.stop_timer()
        self.timer.join()