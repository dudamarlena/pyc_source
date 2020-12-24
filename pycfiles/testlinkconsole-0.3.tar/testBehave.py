# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbrun/Projets/Perso/projets/dev/testlinkconsole/testlinkconsole/tests/plugins/testBehave.py
# Compiled at: 2014-07-04 08:06:50
import unittest, mock
from plugins.behave import BehavePlugin

class TestBehavePlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = BehavePlugin()

    def test_activate(self):
        self.assertEquals(self.plugin.activate(), 'Behave plugin actif')

    def test_deactivate(self):
        self.assertEquals(self.plugin.deactivate(), 'Behave plugin inactif')

    @mock.patch('__builtin__.print')
    def test_run(self, mock_print):
        mock_print.assert_has_calls([])
        self.assertEquals(self.plugin.run('profile', 'script'), None)
        return


if __name__ == '__main__':
    unittest.main()