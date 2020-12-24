# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_log.py
# Compiled at: 2016-04-11 03:21:40
# Size of source mod 2**32: 1579 bytes
from io import StringIO
from unittest import TestCase
from mad.log import FileLog
from tests.fakes import InMemoryLog

class LogTests(TestCase):

    def setUp(self):
        self.log = InMemoryLog()

    def test_record(self):
        self.assertTrue(self.log.is_empty)
        self.log.record(5, 'S1', 'something')
        self.assertFalse(self.log.is_empty)

    def test_size(self):
        self.assertTrue(self.log.is_empty)
        self.log.record(5, 'X', 'something')
        self.log.record(10, 'X', 'something else')
        self.assertEqual(self.log.size, 2)


class FileLogTests(TestCase):

    def test_record(self):
        output = StringIO()
        format = '%5d %20s %s'
        log = FileLog(output, format)
        event = (5, 'DB', 'running query')
        log.record(*event)
        self.assertEqual(output.getvalue(), format % event)