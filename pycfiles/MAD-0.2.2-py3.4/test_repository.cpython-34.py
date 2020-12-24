# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_repository.py
# Compiled at: 2016-03-16 03:52:05
# Size of source mod 2**32: 2782 bytes
from unittest import TestCase
from mad.ast import Sequence, DefineService, DefineOperation, DefineClientStub, Think, Query
from mock import MagicMock
from mad.datasource import Mad, InFilesDataSource, Project, Settings

class MadTests(TestCase):

    def test_loading(self):
        Settings.new_identifier = MagicMock()
        Settings.new_identifier.return_value = 1
        parser = self._make_fake_parser()
        source = MagicMock(InFilesDataSource)
        mad = Mad(parser, source)
        simulation = mad.load(Project('test.mad', 25))
        self.assertTrue(parser.parse.called)
        source.open_stream_to.assert_called_once_with('test_1/trace.log')
        self.assertEqual(len(simulation.services), 1)
        self.assertEqual(len(simulation.clients), 1)

    def _make_fake_parser(self):
        parser = MagicMock()
        parser.parse = MagicMock()
        parser.parse.return_value = Sequence(DefineService('DB', DefineOperation('Select', Think(5))), DefineClientStub('Client', 10, Query('DB', 'Select')))
        return parser


class ProjectTests(TestCase):
    TEST_FILE = 'home/test.mad'
    LIMIT = 25

    def setUp(self):
        Settings.new_identifier = MagicMock()
        Settings.new_identifier.return_value = '2016-03-10_8-34-56'
        self.project = Project(self.TEST_FILE, self.LIMIT)

    def test_limit(self):
        self.assertEqual(25, self.project.limit)

    def test_root_file(self):
        self.assertEqual('home/test.mad', self.project.root_file)

    def test_name(self):
        self.assertEqual('test', self.project.name)

    def test_output_directory(self):
        self.assertEqual('test_2016-03-10_8-34-56', self.project.output_directory)

    def test_log_file(self):
        self.assertEqual('test_2016-03-10_8-34-56/trace.log', self.project.log_file)

    def test_report_file(self):
        report_name = self.project.report_for('DB')
        self.assertEqual('test_2016-03-10_8-34-56/DB.log', report_name)