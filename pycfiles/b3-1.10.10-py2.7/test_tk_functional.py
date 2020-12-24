# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_tk_functional.py
# Compiled at: 2015-02-24 17:29:43
import os
from textwrap import dedent
from mock import Mock, patch
import unittest2 as unittest
from mockito import when
import b3
from b3.plugins.admin import AdminPlugin
from b3.plugins.tk import TkPlugin
from b3.config import CfgConfigParser
from b3.fake import FakeClient
from tests import B3TestCase
from b3 import __file__ as b3_module__file__
ADMIN_CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(b3_module__file__), 'conf/plugin_admin.ini'))

@unittest.skipUnless(os.path.exists(ADMIN_CONFIG_FILE), reason='cannot get default plugin config file at %s' % ADMIN_CONFIG_FILE)
class Tk_functional_test(B3TestCase):

    def setUp(self):
        B3TestCase.setUp(self)
        self.console.gameName = 'f00'
        self.adminPlugin = AdminPlugin(self.console, ADMIN_CONFIG_FILE)
        when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)
        self.adminPlugin.onLoadConfig()
        self.adminPlugin.onStartup()
        self.conf = CfgConfigParser()
        self.conf.loadFromString(dedent('\n            [settings]\n            max_points: 400\n            levels: 0,1,2,20,40\n            round_grace: 7\n            issue_warning: sfire\n            grudge_enable: True\n            private_messages: True\n            damage_threshold: 100\n            warn_level: 2\n            halflife: 0\n            warn_duration: 1h\n\n            [messages]\n            ban: ^7team damage over limit\n            forgive: ^7$vname^7 has forgiven $aname [^3$points^7]\n            grudged: ^7$vname^7 has a ^1grudge ^7against $aname [^3$points^7]\n            forgive_many: ^7$vname^7 has forgiven $attackers\n            forgive_warning: ^1ALERT^7: $name^7 auto-kick if not forgiven. Type ^3!forgive $cid ^7to forgive. [^3damage: $points^7]\n            no_forgive: ^7no one to forgive\n            no_punish: ^7no one to punish\n            players: ^7Forgive who? %s\n            forgive_info: ^7$name^7 has ^3$points^7 TK points\n            grudge_info: ^7$name^7 is ^1grudged ^3$points^7 TK points\n            forgive_clear: ^7$name^7 cleared of ^3$points^7 TK points\n            tk_warning_reason: ^3Do not attack teammates, ^1Attacked: ^7$vname ^7[^3$points^7]\n            tk_request_action: ^7type ^3!fp ^7 to forgive ^3%s\n\n            [level_0]\n            kill_multiplier: 2\n            damage_multiplier: 1\n            ban_length: 2\n\n            [level_1]\n            kill_multiplier: 2\n            damage_multiplier: 1\n            ban_length: 2\n\n            [level_2]\n            kill_multiplier: 1\n            damage_multiplier: 0.5\n            ban_length: 1\n\n            [level_20]\n            kill_multiplier: 1\n            damage_multiplier: 0.5\n            ban_length: 0\n\n            [level_40]\n            kill_multiplier: 0.75\n            damage_multiplier: 0.5\n            ban_length: 0\n        '))
        self.p = TkPlugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.joe = FakeClient(self.console, name='Joe', guid='joeguid', groupBits=1, team=b3.TEAM_RED)
        self.mike = FakeClient(self.console, name='Mike', guid='mikeguid', groupBits=1, team=b3.TEAM_RED)
        self.bill = FakeClient(self.console, name='Bill', guid='billguid', groupBits=1, team=b3.TEAM_RED)
        self.superadmin = FakeClient(self.console, name='superadmin', guid='superadminguid', groupBits=128, team=b3.TEAM_RED)


@patch('threading.Timer')
class Test_tk_detected(Tk_functional_test):

    def test_damage_different_teams(self, timer_patch):
        self.joe.warn = Mock()
        self.joe.connects(0)
        self.mike.connects(1)
        self.mike.team = b3.TEAM_BLUE
        self.joe.damages(self.mike)
        self.assertEqual(0, self.joe.warn.call_count)

    def test_kill_different_teams(self, timer_patch):
        self.joe.warn = Mock()
        self.joe.connects(0)
        self.mike.connects(1)
        self.mike.team = b3.TEAM_BLUE
        self.joe.kills(self.mike)
        self.assertEqual(0, self.joe.warn.call_count)

    def test_kill_within_10s(self, timer_patch):
        self.p._round_grace = 10
        self.joe.warn = Mock()
        self.joe.connects(0)
        self.mike.connects(1)
        self.joe.kills(self.mike)
        self.assertEqual(1, self.joe.warn.call_count)

    def test_damage(self, timer_patch):
        self.p._round_grace = 0
        self.joe.warn = Mock()
        self.joe.connects(0)
        self.mike.connects(1)
        self.joe.damages(self.mike)
        self.joe.damages(self.mike)
        self.joe.damages(self.mike)
        self.joe.damages(self.mike)
        self.joe.damages(self.mike)
        self.assertEqual(0, self.joe.warn.call_count)

    def test_kill(self, timer_patch):
        self.p._round_grace = 0
        self.joe.warn = Mock()
        self.joe.connects(0)
        self.mike.connects(1)
        self.joe.kills(self.mike)
        self.assertEqual(1, self.joe.warn.call_count)
        self.assertIsNotNone(self.mike.getMessageHistoryLike('^7type ^3!fp ^7 to forgive'))

    def test_multikill(self, timer_patch):
        self.p._round_grace = 0
        with patch.object(self.console, 'say') as (patched_say):
            self.joe.warn = Mock()
            self.joe.tempban = Mock()
            self.joe.connects(0)
            self.mike.connects(1)
            self.mike.clearMessageHistory()
            self.joe.kills(self.mike)
            self.assertEqual(1, self.joe.warn.call_count)
            self.assertEquals(1, len(self.mike.getAllMessageHistoryLike('^7type ^3!fp ^7 to forgive')))
            self.joe.kills(self.mike)
            self.assertEqual(1, len([ call_args[0][0] for call_args in patched_say.call_args_list if 'auto-kick if not forgiven' in call_args[0][0] ]))
            self.joe.kills(self.mike)
            self.assertEqual(1, self.joe.tempban.call_count)


@patch('threading.Timer')
class Test_commands(Tk_functional_test):

    def test_forgiveinfo(self, timer_patch):
        self.superadmin.connects(99)
        self.p._round_grace = 0
        self.joe.warn = Mock()
        self.joe.connects(0)
        self.mike.connects(1)
        self.bill.connects(2)
        self.joe.kills(self.mike)
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!forgiveinfo joe')
        self.assertEqual(['Joe has 200 TK points, Attacked: Mike (200)'], self.superadmin.message_history)
        self.joe.damages(self.bill, points=6)
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!forgiveinfo joe')
        self.assertEqual(['Joe has 206 TK points, Attacked: Mike (200), Bill (6)'], self.superadmin.message_history)
        self.mike.damages(self.joe, points=27)
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!forgiveinfo joe')
        self.assertEqual(['Joe has 206 TK points, Attacked: Mike (200), Bill (6), Attacked By: Mike [27]'], self.superadmin.message_history)

    def test_forgive(self, timer_patch):
        self.superadmin.connects(99)
        self.p._round_grace = 0
        self.joe.warn = Mock()
        self.joe.connects(0)
        self.mike.connects(1)
        self.joe.kills(self.mike)
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!forgiveinfo joe')
        self.assertEqual(['Joe has 200 TK points, Attacked: Mike (200)'], self.superadmin.message_history)
        self.mike.says('!forgive')
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!forgiveinfo joe')
        self.assertEqual(['Joe has 0 TK points'], self.superadmin.message_history)

    def test_forgiveclear(self, timer_patch):
        self.superadmin.connects(99)
        self.p._round_grace = 0
        self.joe.warn = Mock()
        self.joe.connects(0)
        self.mike.connects(1)
        self.joe.kills(self.mike)
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!forgiveinfo joe')
        self.assertEqual(['Joe has 200 TK points, Attacked: Mike (200)'], self.superadmin.message_history)
        self.superadmin.says('!forgiveclear joe')
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!forgiveinfo joe')
        self.assertEqual(['Joe has 0 TK points'], self.superadmin.message_history)

    def test_forgivelist(self, timer_patcher):
        self.p._round_grace = 0
        self.joe.connects(0)
        self.mike.connects(1)
        self.bill.connects(2)
        self.joe.clearMessageHistory()
        self.joe.says('!forgivelist')
        self.assertEqual(['no one to forgive'], self.joe.message_history)
        self.mike.damages(self.joe, points=14)
        self.joe.clearMessageHistory()
        self.joe.says('!forgivelist')
        self.assertEqual(['Forgive who? [1] Mike [14]'], self.joe.message_history)
        self.bill.damages(self.joe, points=84)
        self.joe.clearMessageHistory()
        self.joe.says('!forgivelist')
        self.assertEqual(['Forgive who? [1] Mike [14], [2] Bill [84]'], self.joe.message_history)

    def test_forgiveall(self, timer_patcher):
        self.p._round_grace = 0
        self.joe.connects(0)
        self.mike.connects(1)
        self.bill.connects(2)
        self.mike.damages(self.joe, points=14)
        self.bill.damages(self.joe, points=84)
        self.joe.clearMessageHistory()
        self.joe.says('!forgivelist')
        self.assertEqual(['Forgive who? [1] Mike [14], [2] Bill [84]'], self.joe.message_history)
        self.joe.says('!forgiveall')
        self.joe.clearMessageHistory()
        self.joe.says('!forgivelist')
        self.assertNotIn('Mike', self.joe.message_history[0])
        self.assertNotIn('Bill', self.joe.message_history[0])

    def test_forgiveprev(self, timer_patcher):
        self.p._round_grace = 0
        self.joe.connects(0)
        self.mike.connects(1)
        self.bill.connects(2)
        self.mike.damages(self.joe, points=14)
        self.bill.damages(self.joe, points=84)
        self.joe.clearMessageHistory()
        self.joe.says('!forgivelist')
        self.assertEqual(['Forgive who? [1] Mike [14], [2] Bill [84]'], self.joe.message_history)
        self.joe.says('!forgiveprev')
        self.joe.clearMessageHistory()
        self.joe.says('!forgivelist')
        self.assertEqual(['Forgive who? [1] Mike [14]'], self.joe.message_history)