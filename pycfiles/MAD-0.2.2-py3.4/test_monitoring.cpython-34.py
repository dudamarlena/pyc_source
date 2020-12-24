# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_monitoring.py
# Compiled at: 2016-04-21 06:15:58
# Size of source mod 2**32: 2247 bytes
from unittest import TestCase
from mock import MagicMock
from tests.fakes import InMemoryFileSystem
from io import StringIO
from mad.monitoring import CSVReport
from mad.ui import Controller, Arguments

class MonitoringTests(TestCase):
    MAD_FILE = 'test.mad'

    def setUp(self):
        self.file_system = InMemoryFileSystem()

    def test_loading(self):
        Arguments._identifier = lambda s: '1'
        self.file_system.define(self.MAD_FILE, 'service DB {  operation Select {      think 5   }}client Browser {  every 10 {      query DB/Select   }}')
        controller = Controller(StringIO(), self.file_system)
        controller.execute('test.mad', '25')
        data = self.file_system.opened_files['test_1/DB.log'].getvalue().split('\n')
        self.assertEqual(4, len(data), data)


class ReportTests(TestCase):

    def test_report(self):
        output = StringIO()
        report = CSVReport(output, [
         ('time', '%3d'),
         ('queue_length', '%3d')])
        report(time=5, queue_length=3)
        report(time=10, queue_length=6)
        expected_csv = 'time, queue length\n  5,   3\n 10,   6\n'
        self.assertEqual(expected_csv, output.getvalue())