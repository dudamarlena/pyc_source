# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbrun/Projets/Perso/projets/dev/testlinkconsole/testlinkconsole/tests/libs/testConsoleBase.py
# Compiled at: 2014-07-08 03:11:00
import unittest, mock, sys
from mock import call
from StringIO import StringIO
import ConfigParser
from libs.consoleBase import ConsoleBase

class TestconsoleBase(unittest.TestCase):

    def setUp(self):
        sav_stdout = sys.stdout
        self.out = StringIO()
        sys.stdout = self.out
        self.consoleBase = ConsoleBase(ConfigParser.RawConfigParser())

    def test_read_config(self):
        self.consoleBase.LIST_VARIABLE = {'commande': 'Un commande'}
        self.assertEquals(self.consoleBase.read_config(), None)
        return

    @mock.patch('__builtin__.print')
    def test_help_config(self, mock_print):
        mock_print.assert_has_calls([])
        self.assertEquals(self.consoleBase.help_config(), None)
        output = self.out.getvalue().strip()
        self.assertEquals(output, 'config\nshow configuration')
        return

    @mock.patch('__builtin__.print')
    def test_do_config(self, mock_print):
        mock_print.assert_has_calls([])
        self.consoleBase.LIST_VARIABLE = {'commande': 'Un commande'}
        self.consoleBase.commande = 'test'
        self.assertEquals(self.consoleBase.do_config('line'), None)
        return

    @mock.patch('__builtin__.open')
    def test_do_save(self, mock_open):
        configuration = ConfigParser.RawConfigParser()
        configuration.add_section('console')
        self.consoleBase.LIST_VARIABLE = {'commande': 'une commande'}
        self.consoleBase.commande = 'test'
        self.consoleBase.config = configuration
        mock_open.assert_has_calls([])
        self.assertEquals(self.consoleBase.do_save('line'), None)
        return

    @mock.patch('__builtin__.print')
    def test_help_save(self, mock_print):
        mock_print.assert_has_calls([])
        self.assertEquals(self.consoleBase.help_save(), None)
        return

    @mock.patch('__builtin__.print')
    def test_help_get(self, mock_print):
        mock_print.assert_has_calls([])
        self.assertEquals(self.consoleBase.help_get(), None)
        return

    @mock.patch('__builtin__.print')
    def test_do_get_variableNotFound(self, mock_print):
        mock_print.assert_has_calls([])
        self.assertEquals(self.consoleBase.do_get('line'), None)
        return

    @mock.patch('__builtin__.print')
    def test_do_get_variable(self, mock_print):
        self.consoleBase.LIST_VARIABLE = {'commande': 'une commande'}
        self.consoleBase.commande = 'test'
        mock_print.assert_has_calls([])
        self.assertEquals(self.consoleBase.do_get('commande'), None)
        return

    def test_complete_get_notext(self):
        self.consoleBase.LIST_VARIABLE = {'commande': 'une commande'}
        self.assertEquals(self.consoleBase.complete_get('', 'line', 'ids', 'idx'), ['commande'])
        self.assertEquals(self.consoleBase.complete_get('com', 'line', 'ids', 'idx'), ['commande'])

    def test_complete_get_cmd(self):
        self.consoleBase.LIST_VARIABLE = {'commande': 'une commande', 'autre': 'autre commande'}
        self.assertItemsEqual(self.consoleBase.complete_get('', 'line', 'ids', 'idx'), ['commande', 'autre'])
        self.assertEquals(self.consoleBase.complete_get('com', 'line', 'ids', 'idx'), ['commande'])

    @mock.patch('__builtin__.print')
    def test_help_set(self, mock_print):
        mock_print.assert_has_calls([])
        self.assertEquals(self.consoleBase.help_set(), None)
        return

    @mock.patch('__builtin__.print')
    def test_do_set(self, mock_print):
        mock_print.assert_has_calls([])
        self.assertEquals(self.consoleBase.do_set('variable value'), None)
        return

    def test_complete_set_notext(self):
        self.consoleBase.LIST_VARIABLE = {'commande': 'une commande'}
        self.assertEquals(self.consoleBase.complete_set('', 'line', 'ids', 'idx'), ['commande'])
        self.assertEquals(self.consoleBase.complete_set('com', 'line', 'ids', 'idx'), ['commande'])

    def test_complete_set_cmd(self):
        self.consoleBase.LIST_VARIABLE = {'commande': 'une commande', 'autre': 'autre commande'}
        self.assertItemsEqual(self.consoleBase.complete_set('', 'line', 'ids', 'idx'), ['commande', 'autre'])
        self.assertEquals(self.consoleBase.complete_set('com', 'line', 'ids', 'idx'), ['commande'])


if __name__ == '__main__':
    unittest.main()