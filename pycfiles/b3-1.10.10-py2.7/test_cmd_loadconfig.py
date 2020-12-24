# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminbf3\test_cmd_loadconfig.py
# Compiled at: 2016-03-08 18:42:10
from mock import Mock, ANY
import os
from mock import patch
from b3.config import CfgConfigParser
from b3.plugins.poweradminbf3 import Poweradminbf3Plugin
from tests.plugins.poweradminbf3 import Bf3TestCase

class Test_cmd_loadconfig(Bf3TestCase):

    def setUp(self):
        super(Test_cmd_loadconfig, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString('[commands]\nloadconfig: 40\n            ')
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

    def test_no_argument(self):
        self.admin.connects('admin')
        self.admin.clearMessageHistory()
        self.p._configPath = 'some_path'
        self.admin.says('!loadconfig')
        self.assertEqual(['Invalid or missing data, try !help loadconfig'], self.admin.message_history)

    def test_bad_argument(self):
        self.admin.connects('admin')
        self.admin.clearMessageHistory()
        self.p._configPath = 'some_path'
        with patch.object(os, 'listdir') as (listdir_mock):
            listdir_mock.return_value = [
             'junk.txt', 'conf1.cfg', 'conf2.cfg', 'hardcore.cfg', 'hardcore-sqdm.cfg']
            self.admin.says('!loadconfig hard')
        self.assertEqual(['Do you mean : hardcore, hardcore-sqdm ?'], self.admin.message_history)

    def test_no_config_available(self):
        self.admin.connects('admin')
        self.admin.clearMessageHistory()
        self.p._configPath = 'some_path'
        with patch.object(os, 'listdir') as (listdir_mock):
            listdir_mock.return_value = [
             'junk.txt']
            self.admin.says('!loadconfig hard')
        self.assertEqual(['Cannot find any config file named hard.cfg'], self.admin.message_history)

    def test_nominal(self):
        self.admin.connects('admin')
        self.admin.clearMessageHistory()
        self.p._load_server_config_from_file = Mock()
        self.p._configPath = 'some_path'
        with patch.object(os, 'listdir') as (listdir_mock):
            listdir_mock.return_value = [
             'theconfig.cfg']
            self.admin.says('!loadconfig theconfig')
        self.assertEqual(['Loading config theconfig ...'], self.admin.message_history)
        self.p._load_server_config_from_file.assert_called_once_with(self.admin, config_name='theconfig', file_path=ANY, threaded=ANY)