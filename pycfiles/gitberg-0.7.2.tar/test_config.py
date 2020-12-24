# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/tests/test_config.py
# Compiled at: 2018-09-05 10:03:00
import errno, os, os.path, unittest
from gitenberg import config

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.app_name = 'test_application_gitberg_delete'
        self.cf = config.ConfigFile(appname=self.app_name)
        try:
            os.unlink(self.cf.file_path)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    def test_config_file_path(self):
        self.assertNotEqual(self.cf.file_path, None)
        return

    def test_config_parse(self):
        config.data

    def test_from_environment(self):
        os.environ['gitberg_rdf_library'] = 'test library path'
        self.assertFalse(os.path.exists(self.cf.file_path))
        self.cf = config.ConfigFile(appname=self.app_name)
        self.assertEqual('test library path', config.data['rdf_library'])
        del os.environ['gitberg_rdf_library']
        config.data = {}

    def test_from_environment_uppercase(self):
        os.environ['GITBERG_RDF_LIBRARY'] = 'test library path'
        self.cf = config.ConfigFile(appname=self.app_name)
        self.assertEqual('test library path', config.data['rdf_library'])
        del os.environ['GITBERG_RDF_LIBRARY']
        config.data = {}

    def tearDown(self):
        pass