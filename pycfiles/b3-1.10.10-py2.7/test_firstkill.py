# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_firstkill.py
# Compiled at: 2015-05-27 19:37:28
import unittest2
from textwrap import dedent
from mock import Mock
from mockito import when
from b3 import TEAM_RED, TEAM_BLUE
from b3.cvar import Cvar
from b3.config import MainConfig
from b3.config import XmlConfigParser
from b3.config import CfgConfigParser
from b3.parsers.iourt42 import Iourt42Parser
from b3.plugins.admin import AdminPlugin
from b3.plugins.firstkill import FirstkillPlugin
from tests import logging_disabled

class FirstKillCase(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        with logging_disabled():
            from b3.parsers.q3a.abstractParser import AbstractParser
            from b3.fake import FakeConsole
            AbstractParser.__bases__ = (
             FakeConsole,)

    def setUp(self):
        parser_conf = XmlConfigParser()
        parser_conf.loadFromString(dedent('\n            <configuration>\n                <settings name="server">\n                    <set name="game_log"></set>\n                </settings>\n            </configuration>\n        '))
        self.parser_conf = MainConfig(parser_conf)
        self.console = Iourt42Parser(self.parser_conf)
        when(self.console).getCvar('auth').thenReturn(Cvar('auth', value='0'))
        when(self.console).getCvar('fs_basepath').thenReturn(Cvar('fs_basepath', value='/fake/basepath'))
        when(self.console).getCvar('fs_homepath').thenReturn(Cvar('fs_homepath', value='/fake/homepath'))
        when(self.console).getCvar('fs_game').thenReturn(Cvar('fs_game', value='q3ut4'))
        when(self.console).getCvar('gamename').thenReturn(Cvar('gamename', value='q3urt42'))
        self.console.startup()
        with logging_disabled():
            self.adminPlugin = AdminPlugin(self.console, '@b3/conf/plugin_admin.ini')
            self.adminPlugin.onLoadConfig()
            self.adminPlugin.onStartup()
        when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)
        self.conf = CfgConfigParser()
        self.conf.loadFromString(dedent('\n            [settings]\n            firstkill: on\n            firsttk: on\n            firsths: on\n\n            [commands]\n            firstkill: superadmin\n            firsttk: superadmin\n            firsths: superadmin\n\n            [messages]\n            ## $client = the client who made the kill\n            ## $target = the client who suffered the kill\n            first_kill: ^2First Kill^3: $client killed $target\n            first_kill_by_headshot: ^2First Kill ^5by Headshot^3: $client killed $target\n            first_teamkill: ^1First TeamKill^3: $client teamkilled $target\n        '))
        self.p = FirstkillPlugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

    def tearDown(self):
        self.console.working = False


class Test_events(FirstKillCase):

    def setUp(self):
        FirstKillCase.setUp(self)
        with logging_disabled():
            from b3.fake import FakeClient
        self.mike = FakeClient(console=self.console, name='Mike', guid='mikeguid', team=TEAM_BLUE, groupBits=1)
        self.mark = FakeClient(console=self.console, name='Mark', guid='markguid', team=TEAM_BLUE, groupBits=1)
        self.bill = FakeClient(console=self.console, name='Bill', guid='billguid', team=TEAM_RED, groupBits=1)
        self.mike.connects('1')
        self.bill.connects('2')
        self.mark.connects('3')

    def tearDown(self):
        self.mike.disconnects()
        self.bill.disconnects()
        self.mark.disconnects()
        FirstKillCase.tearDown(self)

    def test_first_kill(self):
        self.p._firsths = False
        self.p._firstkill = True
        self.p._kill = 0
        self.p.announce_first_kill = Mock()
        self.p.announce_first_kill_by_headshot = Mock()
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_KILL', client=self.mike, target=self.bill, data=(100, self.console.UT_MOD_DEAGLE, self.console.HL_HEAD)))
        self.p.announce_first_kill.assert_called_with(self.mike, self.bill)
        self.assertFalse(self.p.announce_first_kill_by_headshot.called)

    def test_first_kill_already_broadcasted(self):
        self.p._firsths = False
        self.p._firstkill = True
        self.p._kill = 1
        self.p.announce_first_kill = Mock()
        self.p.announce_first_kill_by_headshot = Mock()
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_KILL', client=self.mike, target=self.bill, data=(100, self.console.UT_MOD_DEAGLE, self.console.HL_HEAD)))
        self.assertFalse(self.p.announce_first_kill.called)
        self.assertFalse(self.p.announce_first_kill_by_headshot.called)

    def test_first_kill_disabled(self):
        self.p._firsths = False
        self.p._firstkill = False
        self.p._kill = 0
        self.p.announce_first_kill = Mock()
        self.p.announce_first_kill_by_headshot = Mock()
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_KILL', client=self.mike, target=self.bill, data=(100, self.console.UT_MOD_DEAGLE, self.console.HL_HEAD)))
        self.assertFalse(self.p.announce_first_kill.called)
        self.assertFalse(self.p.announce_first_kill_by_headshot.called)

    def test_first_kill_by_headshot(self):
        self.p._firsths = True
        self.p._firstkill = True
        self.p._kill = 0
        self.p.announce_first_kill = Mock()
        self.p.announce_first_kill_by_headshot = Mock()
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_KILL', client=self.mike, target=self.bill, data=(100, self.console.UT_MOD_DEAGLE, self.console.HL_HEAD)))
        self.p.announce_first_kill_by_headshot.assert_called_with(self.mike, self.bill)
        self.assertFalse(self.p.announce_first_kill.called)

    def test_first_kill_by_headshot_already_broadcasted(self):
        self.p._firsths = True
        self.p._firstkill = True
        self.p._kill = 1
        self.p.announce_first_kill = Mock()
        self.p.announce_first_kill_by_headshot = Mock()
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_KILL', client=self.mike, target=self.bill, data=(100, self.console.UT_MOD_DEAGLE, self.console.HL_HEAD)))
        self.assertFalse(self.p.announce_first_kill.called)
        self.assertFalse(self.p.announce_first_kill_by_headshot.called)

    def test_first_kill_by_headshot_disabled(self):
        self.p._firsths = True
        self.p._firstkill = False
        self.p._kill = 0
        self.p.announce_first_kill = Mock()
        self.p.announce_first_kill_by_headshot = Mock()
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_KILL', client=self.mike, target=self.bill, data=(100, self.console.UT_MOD_DEAGLE, self.console.HL_HEAD)))
        self.assertFalse(self.p.announce_first_kill.called)
        self.assertFalse(self.p.announce_first_kill_by_headshot.called)

    def test_first_teamkill(self):
        self.p._firsttk = True
        self.p._tk = 0
        self.p.announce_first_teamkill = Mock()
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_KILL_TEAM', client=self.mike, target=self.mark, data=(100, self.console.UT_MOD_DEAGLE, self.console.HL_HEAD)))
        self.p.announce_first_teamkill.assert_called_with(self.mike, self.mark)

    def test_first_teamkill_already_broadcasted(self):
        self.p._firsttk = True
        self.p._tk = 1
        self.p.announce_first_teamkill = Mock()
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_KILL_TEAM', client=self.mike, target=self.mark, data=(100, self.console.UT_MOD_DEAGLE, self.console.HL_HEAD)))
        self.assertFalse(self.p.announce_first_teamkill.called)

    def test_first_teamkill_disabled(self):
        self.p._firsttk = False
        self.p._tk = 0
        self.p.announce_first_teamkill = Mock()
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_KILL_TEAM', client=self.mike, target=self.mark, data=(100, self.console.UT_MOD_DEAGLE, self.console.HL_HEAD)))
        self.assertFalse(self.p.announce_first_teamkill.called)