# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_status.py
# Compiled at: 2015-02-24 17:29:43
from textwrap import dedent
from mock import patch
from tests import B3TestCase
from b3.plugins.status import StatusPlugin
from b3.config import CfgConfigParser

class Test_config(B3TestCase):

    @patch('b3.cron.PluginCronTab')
    def test_no_svar_table(self, pluginCronTab_mock):
        conf = CfgConfigParser()
        conf.loadFromString(dedent('\n            [settings]\n            interval: 60\n            output_file: ~/status.xml\n            enableDBsvarSaving: no\n            enableDBclientSaving: no\n            '))
        self.p = StatusPlugin(self.console, conf)
        self.p._tables = {'svars': 'current_svars', 'cvars': 'current_clients'}
        self.p.onLoadConfig()
        self.assertEqual('current_svars', self.p._tables['svars'])

    @patch('b3.cron.PluginCronTab')
    def test_svar_table(self, pluginCronTab_mock):
        conf = CfgConfigParser()
        conf.loadFromString(dedent('\n            [settings]\n            interval: 60\n            output_file: ~/status.xml\n            enableDBsvarSaving: yes\n            enableDBclientSaving: no\n            svar_table: alternate_svar_table\n            '))
        self.p = StatusPlugin(self.console, conf)
        self.p._tables = {'svars': 'current_svars', 'cvars': 'current_clients'}
        self.p.onLoadConfig()
        self.assertEqual('alternate_svar_table', self.p._tables['svars'])

    @patch('b3.cron.PluginCronTab')
    def test_no_client_table(self, pluginCronTab_mock):
        conf = CfgConfigParser()
        conf.loadFromString(dedent('\n            [settings]\n            interval: 60\n            output_file: ~/status.xml\n            enableDBsvarSaving: no\n            enableDBclientSaving: no\n            '))
        self.p = StatusPlugin(self.console, conf)
        self.p._tables = {'svars': 'current_svars', 'cvars': 'current_clients'}
        self.p.onLoadConfig()
        self.assertEqual('current_clients', self.p._tables['cvars'])

    @patch('b3.cron.PluginCronTab')
    def test_client_table(self, pluginCronTab_mock):
        conf = CfgConfigParser()
        conf.loadFromString(dedent('\n            [settings]\n            interval: 60\n            output_file: ~/status.xml\n            enableDBsvarSaving: no\n            enableDBclientSaving: yes\n            client_table: alternate_client_table\n            '))
        self.p = StatusPlugin(self.console, conf)
        self.p._tables = {'svars': 'current_svars', 'cvars': 'current_clients'}
        self.p.onLoadConfig()
        self.assertEqual('alternate_client_table', self.p._tables['cvars'])