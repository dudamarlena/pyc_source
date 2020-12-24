# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/test_config.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 1405 bytes
import os, unittest
from drove import config
from drove.config import Config, ConfigError

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(config.__file__)), 'config', 'drove.conf')

    def test_config_hierarchy(self):
        """Testing Config: hierarchy"""
        c = Config()
        c['value'] = 'lowlevel'
        c['plugin.one.value'] = 'value'
        c['plugin.one.othervalue'] = 'other'
        c['plugin.two'] = 'second'
        assert c.get_childs('plugin') == {'one', 'two'}
        assert c.get_childs('plugin.one') == {'value', 'othervalue'}
        assert c.get('plugin.one.value') == 'value'
        assert c.get('plugin.two.value') == 'lowlevel'

    def test_config_include(self):
        """Testing Config: include"""
        c = Config(os.devnull)
        c['include'] = self.config_file
        c.reload()
        assert c.get('plugin_dir', False)

    def test_config_default(self):
        """Testing Config: get with default"""
        c = Config()
        assert c.get('none', 'value') == 'value'

    def test_config_notfound(self):
        """Testing Config: value not found"""
        c = Config()
        with self.assertRaises(ConfigError):
            c.get('notfound')