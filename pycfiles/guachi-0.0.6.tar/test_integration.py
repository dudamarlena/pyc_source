# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alfredo/python/vguachi/guachi/guachi/tests/test_integration.py
# Compiled at: 2010-09-19 22:54:14
from os import path, remove, mkdir
import unittest
from guachi import ConfigMapper

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.mapped_options = {'guachi.db.host': 'db_host', 
           'guachi.db.port': 'db_port', 
           'guachi.web.host': 'web_host', 
           'guachi.web.port': 'web_port'}
        self.mapped_defaults = {'db_host': 'localhost', 
           'db_port': 27017, 
           'web_host': 'localhost', 
           'web_port': '8080'}
        try:
            if path.exists('/tmp/guachi'):
                remove('/tmp/guachi')
            else:
                mkdir('/tmp/guachi')
        except Exception:
            pass

    def tearDown(self):
        try:
            if path.exists('/tmp/guachi'):
                remove('/tmp/guachi')
            else:
                mkdir('/tmp/guachi')
        except Exception:
            pass

    def test_access_mapped_configs_empty_dict(self):
        foo = ConfigMapper('/tmp/guachi')
        foo.set_ini_options(self.mapped_options)
        foo.set_default_options(self.mapped_defaults)
        foo.set_config({})
        self.assertEqual(foo(), {})
        self.assertEqual(foo.path, '/tmp/guachi/guachi.db')
        self.assertEqual(foo.get_ini_options(), {})
        self.assertEqual(foo.get_default_options(), {})
        self.assertEqual(foo.get_dict_config(), self.mapped_defaults)
        self.assertEqual(foo.stored_config(), {})
        self.assertTrue(foo.integrity_check())

    def test_access_mapped_configs_dict(self):
        foo = ConfigMapper('/tmp/guachi')
        foo.set_ini_options(self.mapped_options)
        foo.set_default_options(self.mapped_defaults)
        foo.set_config({'db_host': 'example.com', 'db_port': 0})
        self.assertEqual(foo(), {})
        self.assertEqual(foo.path, '/tmp/guachi/guachi.db')
        self.assertEqual(foo.get_ini_options(), {})
        self.assertEqual(foo.get_default_options(), {})
        self.assertEqual(foo.get_dict_config(), {'web_port': '8080', 'web_host': 'localhost', 
           'db_host': 'example.com', 
           'db_port': 0})
        self.assertEqual(foo.stored_config(), {})
        self.assertTrue(foo.integrity_check())