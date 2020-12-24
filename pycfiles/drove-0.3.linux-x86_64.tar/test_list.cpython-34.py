# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/command/test_list.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 798 bytes
import os, unittest
from drove.config import Config
from drove.util.log import getLogger
from drove.command import CommandError
from drove.command.list import ListCommand
import drove

class TestListCommand(unittest.TestCase):

    def test_list_command(self, config=None):
        if config is None:
            config = Config()
            config['plugin_dir'] = [
             os.path.join(os.path.dirname(drove.__file__), 'plugins')]
        cmd = ListCommand(config, None, getLogger())
        assert cmd.__class__.__name__ == 'ListCommand'
        cmd.execute()

    def test_list_command_missing_config(self):
        with self.assertRaises(CommandError):
            self.test_list_command(Config())