# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/command/test_remove.py
# Compiled at: 2015-02-16 15:07:00
# Size of source mod 2**32: 1801 bytes
import unittest
from drove.util import temp
from drove.config import Config
from drove.util.log import getLogger
from drove.command import CommandError
from drove.command.remove import RemoveCommand

class TestRemoveCommand(unittest.TestCase):
    name = 'test.remove'

    class _mock_str(str):
        pass

    class _mock_remove(object):

        def __init__(self, *arg, **kwarg):
            pass

        def remove(self):
            pass

    @staticmethod
    def _mock_find(path=None, pattern=None):
        return [TestRemoveCommand._mock_remove()]

    def test_remove_command(self, install_global=False, plugin=__file__):
        self.plugin = TestRemoveCommand._mock_str(plugin)
        self.plugin.endswith = lambda x: True
        self.install_global = install_global
        self.upgrade = True
        with temp.directory() as (tmp_dir):
            config = Config()
            config['plugin_dir'] = [tmp_dir]
            with temp.variables({'drove.command.remove.find_package': TestRemoveCommand._mock_find}):
                cmd = RemoveCommand(config, self, getLogger())
                assert cmd.__class__.__name__ == 'RemoveCommand'
                cmd.execute()

    def test_remove_command_global(self):
        self.test_remove_command(True)

    def test_remove_command_error(self, plugin_name='author.plugin'):
        self.plugin = plugin_name
        self.install_global = False
        config = Config()
        config['plugin_dir'] = None
        with self.assertRaises(CommandError):
            RemoveCommand(config, self, getLogger()).execute()

    def test_remove_command_error_plugin(self):
        self.test_remove_command_error('author')