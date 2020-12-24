# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/tests/test_config.py
# Compiled at: 2016-03-02 12:26:52
import os, unittest
from gitenberg import config

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.app_name = 'test_application_gitberg_delete'
        self.cf = config.ConfigFile(appname=self.app_name)

    def test_config_file_path(self):
        self.assertNotEqual(self.cf.file_path, None)
        return

    def test_config_parse(self):
        config.data

    def tearDown(self):
        pass