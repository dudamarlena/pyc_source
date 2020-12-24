# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ant/core/tests/log_tests.py
# Compiled at: 2011-10-07 13:53:11
LOG_LOCATION = '/tmp/python-ant.logtest.ant'
import unittest
from ant.core.log import *

class LogReaderTest(unittest.TestCase):

    def setUp(self):
        lw = LogWriter(LOG_LOCATION)
        lw.logOpen()
        lw.logRead('\x01')
        lw.logWrite('\x00')
        lw.logRead('TEST')
        lw.logClose()
        lw.close()
        self.log = LogReader(LOG_LOCATION)

    def test_open_close(self):
        self.assertTrue(self.log.is_open)
        self.log.close()
        self.assertFalse(self.log.is_open)
        self.log.open(LOG_LOCATION)
        self.assertTrue(self.log.is_open)

    def test_read(self):
        t1 = self.log.read()
        t2 = self.log.read()
        t3 = self.log.read()
        t4 = self.log.read()
        t5 = self.log.read()
        self.assertEquals(self.log.read(), None)
        self.assertEquals(t1[0], EVENT_OPEN)
        self.assertTrue(isinstance(t1[1], int))
        self.assertEquals(len(t1), 2)
        self.assertEquals(t2[0], EVENT_READ)
        self.assertTrue(isinstance(t1[1], int))
        self.assertEquals(len(t2), 3)
        self.assertEquals(t2[2], '\x01')
        self.assertEquals(t3[0], EVENT_WRITE)
        self.assertTrue(isinstance(t1[1], int))
        self.assertEquals(len(t3), 3)
        self.assertEquals(t3[2], '\x00')
        self.assertEquals(t4[0], EVENT_READ)
        self.assertEquals(t4[2], 'TEST')
        self.assertEquals(t5[0], EVENT_CLOSE)
        self.assertTrue(isinstance(t1[1], int))
        self.assertEquals(len(t5), 2)
        return


class LogWriterTest(unittest.TestCase):

    def setUp(self):
        self.log = LogWriter(LOG_LOCATION)

    def test_open_close(self):
        self.assertTrue(self.log.is_open)
        self.log.close()
        self.assertFalse(self.log.is_open)
        self.log.open(LOG_LOCATION)
        self.assertTrue(self.log.is_open)

    def test_log(self):
        pass