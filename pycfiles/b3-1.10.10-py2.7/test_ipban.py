# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_ipban.py
# Compiled at: 2015-05-27 19:37:28
import unittest2
from textwrap import dedent
from mockito import when
from mock import Mock
from b3.plugins.ipban import IpbanPlugin
from b3.fake import FakeConsole
from b3.config import CfgConfigParser
from b3.config import MainConfig
from b3.plugins.admin import AdminPlugin
from tests import logging_disabled

class IpbanTestCase(unittest2.TestCase):

    def setUp(self):
        self.parser_conf = MainConfig(CfgConfigParser(allow_no_value=True))
        self.parser_conf.loadFromString(dedent(''))
        self.console = FakeConsole(self.parser_conf)
        self.console.gameName = 'f00'
        self.console.startup()
        with logging_disabled():
            self.adminPlugin = AdminPlugin(self.console, '@b3/conf/plugin_admin.ini')
            self.adminPlugin.onLoadConfig()
            self.adminPlugin.onStartup()
        self.evt_queue = []
        when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)
        with logging_disabled():
            from b3.fake import FakeClient
        self.mike = FakeClient(self.console, name='Mike', exactName='Mike', guid='MIKEGUID', groupBits=16, ip='1.1.1.1')
        self.paul = FakeClient(self.console, name='Paul', exactName='Paul', guid='PAULGUID', groupBits=1, ip='2.2.2.2')
        self.john = FakeClient(self.console, name='John', exactName='John', guid='JOHNGUID', groupBits=0, ip='3.3.3.3')
        self.mary = FakeClient(self.console, name='Mary', exactName='Mary', guid='MARYGUID', groupBits=0, ip='4.4.4.4')
        self.conf = CfgConfigParser()
        self.p = IpbanPlugin(self.console, self.conf)
        when(self.p).getBanIps().thenReturn(['2.2.2.2', '6.6.6.6', '7.7.7.7'])
        when(self.p).getTempBanIps().thenReturn(['3.3.3.3', '8.8.8.8', '9.9.9.9'])

    def tearDown(self):
        self.console.working = False
        self.mike.disconnects()
        self.paul.disconnects()
        self.john.disconnects()
        self.mary.disconnects()

    def init(self, config_content=None):
        if config_content:
            self.conf.loadFromString(config_content)
        else:
            self.conf.loadFromString(dedent('\n                [settings]\n                maxlevel: user\n            '))
        self.p.onLoadConfig()
        self.p.onStartup()

    def test_with_config_content(self):
        self.init(dedent('\n            [settings]\n            maxlevel: admin\n        '))
        self.assertEqual(self.p._maxLevel, 40)

    def test_with_empty_config(self):
        self.init(dedent('\n            [settings]\n        '))
        self.assertEqual(self.p._maxLevel, 1)

    def test_higher_group_level_client_connect(self):
        self.init()
        self.mike.kick = Mock()
        self.mike.connects('1')
        self.assertGreater(self.mike.maxLevel, self.p._maxLevel)
        self.assertEqual(self.mike.kick.call_count, 0)

    def test_ip_banned_client_connect(self):
        self.init()
        self.paul.kick = Mock()
        self.paul.connects('1')
        self.assertLessEqual(self.paul.maxLevel, self.p._maxLevel)
        self.assertIn(self.paul.ip, self.p.getBanIps())
        self.paul.kick.assert_called_once_with('IPBan: client refused: 2.2.2.2 (Paul) has an active Ban')

    def test_ip_temp_banned_client_connect(self):
        self.init()
        self.john.kick = Mock()
        self.john.connects('1')
        self.assertLessEqual(self.paul.maxLevel, self.p._maxLevel)
        self.assertIn(self.john.ip, self.p.getTempBanIps())
        self.john.kick.assert_called_once_with('IPBan: client refused: 3.3.3.3 (John) has an active TempBan')

    def test_clean_client_connect(self):
        self.init()
        self.mary.kick = Mock()
        self.mary.connects('1')
        self.assertLessEqual(self.paul.maxLevel, self.p._maxLevel)
        self.assertNotIn(self.mary.ip, self.p.getBanIps())
        self.assertNotIn(self.mary.ip, self.p.getTempBanIps())
        self.assertEqual(self.mary.kick.call_count, 0)