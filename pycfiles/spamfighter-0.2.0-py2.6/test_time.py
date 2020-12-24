# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/utils/test/test_time.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.utils.time}.
"""
import time as sys_time
from twisted.trial import unittest
from spamfighter.utils.time import time, startUpTestTimer, advanceTestTimer, setTestTimer, tearDownTestTimer, _inaccurate_timer_tick

class InaccurateTimeTestCase(unittest.TestCase):
    """
    Тесты на L{spamfighter.utils.time} - вариант расчета времени с точностью до 1 с.
    """

    def testTime(self):
        _inaccurate_timer_tick()
        self.assert_(int(sys_time.time()) - time() <= 1)


class TestTimerTestCase(unittest.TestCase):
    """
    Тесты на L{spamfighter.utils.time} - таймер для тестов
    """

    def setUp(self):
        startUpTestTimer(10)

    def tearDown(self):
        tearDownTestTimer()

    def testStartUp(self):
        self.assertEquals(10, time())

    def testAdvance(self):
        advanceTestTimer(20)
        self.assertEquals(30, time())

    def testSet(self):
        setTestTimer(40)
        self.assertEquals(40, time())

    def testTearDown(self):
        tearDownTestTimer()
        _inaccurate_timer_tick()
        self.assert_(int(sys_time.time()) - time() <= 1)
        startUpTestTimer(10)