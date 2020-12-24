# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/tests/test_config.py
# Compiled at: 2018-03-25 07:01:57
# Size of source mod 2**32: 2435 bytes
__doc__ = 'Config class testing.'
import unittest
from pathlib import Path
from unittest import TestCase
from clean.config import Config

class TestConfig(TestCase):
    """TestConfig"""

    def setUp(self):
        """Test setup."""
        current_dir = Path(__file__).parent.resolve()
        self.test_cleanrc_path = current_dir / '.cleanrc'
        cleanrc_template_path = current_dir / '.cleanrc.template'
        with self.test_cleanrc_path.open('w', encoding='utf_8') as (f):
            with cleanrc_template_path.open('r', encoding='utf_8') as (template):
                f.write(template.read())
        self.initialConfig = {'glob': 'fuga', 
         'path': 'hoge', 
         'use_meta_tag': False}

    def test_list_glob_path(self):
        """Test method for Config.list_glob_path."""
        config = Config(config_path=self.test_cleanrc_path)
        path_list = config.list_glob_path()
        self.assertEqual(path_list, [self.initialConfig])

    def test_add_glob_path(self):
        """Test method for Config.add_glob_path."""
        config = Config(config_path=self.test_cleanrc_path)
        is_success = config.add_glob_path('hogehoge', 'fugafuga')
        self.assertTrue(is_success)
        config = Config(config_path=self.test_cleanrc_path)
        path_list = config.list_glob_path()
        self.assertIn({'glob': 'hogehoge', 
         'path': 'fugafuga', 
         'use_meta_tag': True}, path_list)

    def test_add_same_glob_path(self):
        """Test same glob path to add a cleanrc will fail."""
        config = Config(config_path=self.test_cleanrc_path)
        is_success = config.add_glob_path('fuga', 'hoge')
        self.assertFalse(is_success)
        config = Config(config_path=self.test_cleanrc_path)
        path_list = config.list_glob_path()
        self.assertEqual(1, path_list.count(self.initialConfig))

    def test_delete_glob_path(self):
        """Test method for Config.delete_glob_path."""
        config = Config(config_path=self.test_cleanrc_path)
        deleted_config = config.delete_glob_path(0)
        self.assertEqual(deleted_config, self.initialConfig)
        config = Config(config_path=self.test_cleanrc_path)
        path_list = config.list_glob_path()
        self.assertNotIn(self.initialConfig, path_list)


if __name__ == '__main__':
    unittest.main()