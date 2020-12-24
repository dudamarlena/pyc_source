# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: tests/testTestLinkConsole.py
# Compiled at: 2014-07-09 16:53:35
import unittest, mock, mox, sys, ConfigParser, logging
from StringIO import StringIO
from testlinkconsole import TestLinkConsole

class TestTestLinkConsole(unittest.TestCase):

    def setUp(self):
        logger = logging.getLogger('logger')
        self.testlinkconsole = TestLinkConsole(ConfigParser.RawConfigParser(), logger)

    def test_do_plugins(self):
        self.assertEquals(self.testlinkconsole.do_plugins('line'), None)
        return

    @unittest.skip('Refactoring')
    def test_do_list_project(self):
        self.assertEquals(self.testlinkconsole.do_list('projects'), None)
        return

    @unittest.skip('Refactoring')
    def test_do_list_campagnes(self):
        self.assertEquals(self.testlinkconsole.do_list('campagnes'), None)
        return

    @unittest.skip('Refactoring')
    def test_do_list_toto(self):
        self.assertEquals(self.testlinkconsole.do_list('toto'), None)
        return

    @unittest.skip('Refactoring')
    def test_complete_list(self):
        self.assertItemsEqual(self.testlinkconsole.complete_list('', 'line', 'ids', 'idx'), ['projets', 'campagnes', 'tests'])
        self.assertEquals(self.testlinkconsole.complete_list('pro', 'line', 'ids', 'idx'), ['projets'])

    @mock.patch('__builtin__.print')
    def test_help_list(self, mock_print):
        sav_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        mock_print.assert_has_call([])
        self.assertEquals(self.testlinkconsole.help_list(), None)
        output = out.getvalue().strip()
        self.assertEquals(output, 'list [content]\n list content from testlink')
        return

    @unittest.skip('Refactoring')
    def test_run(self):
        self.assertEquals(self.testlinkconsole.do_run('line'), None)
        return

    @mock.patch('__builtin__.print')
    def test_help_run(self, mock_print):
        sav_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        mock_print.assert_has_call([])
        self.assertEquals(self.testlinkconsole.help_run(), None)
        output = out.getvalue().strip()
        self.assertEquals(output, 'run\n  run campagne')
        return