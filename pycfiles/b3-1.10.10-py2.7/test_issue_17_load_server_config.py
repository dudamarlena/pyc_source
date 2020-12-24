# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminbf3\test_issue_17_load_server_config.py
# Compiled at: 2016-03-08 18:42:10
import unittest
from mock import Mock
from b3.plugins.poweradminbf3 import Poweradminbf3Plugin

class Test_issue_17_load_server_config(unittest.TestCase):

    def setUp(self):
        self.console = Mock()
        self.p = Poweradminbf3Plugin(self.console)

    def test_write_cvars_no_result(self):
        self.console.write.return_value = []
        self.p = self.p
        client = Mock()
        self.p.load_server_config(client, 'theConfName', ('## some comment line', '',
                                                          ' vars.serverMessage "Welcome to our Server Play as a team" ',
                                                          '   '))
        self.assertEqual(1, self.console.write.call_count)
        self.console.write.assert_any_call(('vars.serverMessage', '"Welcome to our Server Play as a team"'))


if __name__ == '__main__':
    unittest.main(verbosity=2)