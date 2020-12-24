# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_spawnkill.py
# Compiled at: 2015-05-27 19:37:28
import time, os, unittest2 as unittest
from textwrap import dedent
from mockito import when
from b3.plugins.admin import AdminPlugin
from b3.plugins.spawnkill import SpawnkillPlugin
from b3.config import CfgConfigParser
from b3.config import XmlConfigParser
from b3.cvar import Cvar
from b3.parsers.iourt42 import Iourt42Parser
from b3 import __file__ as b3_module__file__
from b3 import TEAM_BLUE, TEAM_RED
from tests import logging_disabled
ADMIN_CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(b3_module__file__), 'conf/plugin_admin.ini'))

@unittest.skipUnless(os.path.exists(ADMIN_CONFIG_FILE), reason='cannot get default plugin config file at %s' % ADMIN_CONFIG_FILE)
class SpawnkillTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with logging_disabled():
            from b3.parsers.q3a.abstractParser import AbstractParser
            from b3.fake import FakeConsole
            AbstractParser.__bases__ = (
             FakeConsole,)

    def setUp(self):
        self.parser_conf = XmlConfigParser()
        self.parser_conf.loadFromString(dedent('\n            <configuration>\n                <settings name="server">\n                    <set name="game_log"></set>\n                </settings>\n            </configuration>\n        '))
        self.console = Iourt42Parser(self.parser_conf)
        when(self.console).getCvar('auth').thenReturn(Cvar('auth', value='0'))
        when(self.console).getCvar('fs_basepath').thenReturn(Cvar('g_maxGameClients', value='/fake/basepath'))
        when(self.console).getCvar('fs_homepath').thenReturn(Cvar('sv_maxclients', value='/fake/homepath'))
        when(self.console).getCvar('fs_game').thenReturn(Cvar('fs_game', value='q3ut4'))
        when(self.console).getCvar('gamename').thenReturn(Cvar('gamename', value='q3urt42'))
        self.console.startup()
        self.admin_plugin_conf = CfgConfigParser()
        self.admin_plugin_conf.loadFromString(dedent('\n            [warn]\n            pm_global: yes\n            alert_kick_num: 3\n            instant_kick_num: 5\n            tempban_num: 6\n            tempban_duration: 1d\n            max_duration: 1d\n            message: ^1WARNING^7 [^3$warnings^7]: $reason\n            warn_delay: 15\n            reason: ^7too many warnings: $reason\n            duration_divider: 30\n            alert: ^1ALERT^7: $name^7 auto-kick from warnings if not cleared [^3$warnings^7] $reason\n            warn_command_abusers: no'))
        with logging_disabled():
            self.adminPlugin = AdminPlugin(self.console, self.admin_plugin_conf)
            self.adminPlugin.onLoadConfig()
            self.adminPlugin.onStartup()
        when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)

    def tearDown(self):
        self.console.working = False


class Test_events(SpawnkillTestCase):

    def setUp(self):
        SpawnkillTestCase.setUp(self)
        with logging_disabled():
            from b3.fake import FakeClient
        self.mike = FakeClient(console=self.console, name='Mike', guid='mikeguid', team=TEAM_RED, groupBits=1)
        self.bill = FakeClient(console=self.console, name='Bill', guid='billguid', team=TEAM_BLUE, groupBits=1)
        self.mark = FakeClient(console=self.console, name='Mark', guid='markguid', team=TEAM_BLUE, groupBits=128)
        self.conf = CfgConfigParser()
        self.p = SpawnkillPlugin(self.console, self.conf)

    def init(self, config_content=None):
        if config_content:
            self.conf.loadFromString(config_content)
        else:
            self.conf.loadFromString(dedent('\n                [hit]\n                maxlevel: admin\n                delay: 2\n                penalty: warn\n                duration: 3m\n                reason: do not shoot to spawning players!\n\n                [kill]\n                maxlevel: admin\n                delay: 3\n                penalty: warn\n                duration: 5m\n                reason: spawnkilling is not allowed on this server!\n            '))
        self.p.onLoadConfig()
        self.p.onStartup()

    def tearDown(self):
        self.mike.disconnects()
        self.bill.disconnects()
        self.mark.disconnects()
        SpawnkillTestCase.tearDown(self)

    def test_client_spawntime_mark(self):
        self.init()
        self.mike.connects('1')
        self.bill.connects('2')
        self.console.parseLine('ClientSpawn: 1')
        self.console.parseLine('ClientSpawn: 2')
        self.assertEqual(True, self.mike.isvar(self.p, 'spawntime'))
        self.assertEqual(True, self.bill.isvar(self.p, 'spawntime'))

    def test_client_spawn_hit_admin_level_bypass(self):
        self.init(dedent('\n            [hit]\n            maxlevel: admin\n            delay: 10\n            penalty: warn\n            duration: 3m\n            reason: do not shoot to spawning players!\n        '))
        self.mark.connects('1')
        self.bill.connects('2')
        self.mark.setvar(self.p, 'spawntime', time.time() - 5)
        self.bill.setvar(self.p, 'spawntime', time.time() - 5)
        self.mark.damages(self.bill)
        self.assertEqual(0, self.console.storage.numPenalties(self.mark, 'Warning'))

    def test_client_spawn_hit_no_spawntime_marked(self):
        self.init(dedent('\n            [hit]\n            maxlevel: admin\n            delay: 10\n            penalty: warn\n            duration: 3m\n            reason: do not shoot to spawning players!\n        '))
        self.mike.connects('1')
        self.bill.connects('2')
        self.mike.damages(self.bill)
        self.assertEqual(0, self.console.storage.numPenalties(self.mike, 'Warning'))

    def test_client_spawn_hit_warn(self):
        self.init(dedent('\n            [hit]\n            maxlevel: admin\n            delay: 10\n            penalty: warn\n            duration: 3m\n            reason: do not shoot to spawning players!\n        '))
        self.mike.connects('1')
        self.bill.connects('2')
        self.mike.setvar(self.p, 'spawntime', time.time() - 5)
        self.bill.setvar(self.p, 'spawntime', time.time() - 5)
        self.mike.clearMessageHistory()
        self.mike.damages(self.bill)
        self.assertEqual(1, self.console.storage.numPenalties(self.mike, 'Warning'))
        self.assertListEqual(['WARNING [1]: Mike,  do not shoot to spawning players!'], self.mike.message_history)

    def test_client_spawn_hit_kick(self):
        self.init(dedent('\n            [hit]\n            maxlevel: admin\n            delay: 10\n            penalty: kick\n            duration: 3m\n            reason: do not shoot to spawning players!\n        '))
        self.mike.connects('1')
        self.bill.connects('2')
        self.mike.setvar(self.p, 'spawntime', time.time() - 5)
        self.bill.setvar(self.p, 'spawntime', time.time() - 5)
        self.mike.clearMessageHistory()
        self.mike.damages(self.bill)
        self.assertEqual(1, self.console.storage.numPenalties(self.mike, 'Kick'))

    def test_client_spawn_hit_tempban(self):
        self.init(dedent('\n            [hit]\n            maxlevel: admin\n            delay: 10\n            penalty: tempban\n            duration: 3m\n            reason: do not shoot to spawning players!\n        '))
        self.mike.connects('1')
        self.bill.connects('2')
        self.mike.setvar(self.p, 'spawntime', time.time() - 5)
        self.bill.setvar(self.p, 'spawntime', time.time() - 5)
        self.mike.clearMessageHistory()
        self.mike.damages(self.bill)
        self.assertEqual(1, self.console.storage.numPenalties(self.mike, 'TempBan'))

    def test_client_spawn_hit_slap(self):
        pass

    def test_client_spawn_hit_nuke(self):
        pass

    def test_client_spawn_hit_kill(self):
        pass

    def test_client_spawn_kill_admin_level_bypass(self):
        self.init(dedent('\n            [hit]\n            maxlevel: admin\n            delay: 10\n            penalty: warn\n            duration: 3m\n            reason: do not shoot to spawning players!\n        '))
        self.mark.connects('1')
        self.bill.connects('2')
        self.mark.setvar(self.p, 'spawntime', time.time() - 5)
        self.bill.setvar(self.p, 'spawntime', time.time() - 5)
        self.mark.kills(self.bill)
        self.assertEqual(0, self.console.storage.numPenalties(self.mark, 'Warning'))

    def test_client_spawn_kill_no_spawntime_marked(self):
        self.init(dedent('\n            [hit]\n            maxlevel: admin\n            delay: 10\n            penalty: warn\n            duration: 3m\n            reason: do not shoot to spawning players!\n        '))
        self.mike.connects('1')
        self.bill.connects('2')
        self.mike.kills(self.bill)
        self.assertEqual(0, self.console.storage.numPenalties(self.mike, 'Warning'))

    def test_client_spawn_kill_warn(self):
        self.init(dedent('\n            [kill]\n            maxlevel: admin\n            delay: 10\n            penalty: warn\n            duration: 5m\n            reason: spawnkilling is not allowed on this server!\n        '))
        self.mike.connects('1')
        self.bill.connects('2')
        self.mike.setvar(self.p, 'spawntime', time.time() - 5)
        self.bill.setvar(self.p, 'spawntime', time.time() - 5)
        self.mike.clearMessageHistory()
        self.mike.kills(self.bill)
        self.assertEqual(1, self.console.storage.numPenalties(self.mike, 'Warning'))
        self.assertListEqual(['WARNING [1]: Mike,  spawnkilling is not allowed on this server!'], self.mike.message_history)

    def test_client_spawn_kill_kick(self):
        self.init(dedent('\n            [kill]\n            maxlevel: admin\n            delay: 10\n            penalty: kick\n            duration: 5m\n            reason: spawnkilling is not allowed on this server!\n        '))
        self.mike.connects('1')
        self.bill.connects('2')
        self.mike.setvar(self.p, 'spawntime', time.time() - 5)
        self.bill.setvar(self.p, 'spawntime', time.time() - 5)
        self.mike.clearMessageHistory()
        self.mike.kills(self.bill)
        self.assertEqual(1, self.console.storage.numPenalties(self.mike, 'Kick'))

    def test_client_spawn_kill_tempban(self):
        self.init(dedent('\n            [kill]\n            maxlevel: admin\n            delay: 10\n            penalty: tempban\n            duration: 5m\n            reason: spawnkilling is not allowed on this server!\n        '))
        self.mike.connects('1')
        self.bill.connects('2')
        self.mike.setvar(self.p, 'spawntime', time.time() - 5)
        self.bill.setvar(self.p, 'spawntime', time.time() - 5)
        self.mike.clearMessageHistory()
        self.mike.kills(self.bill)
        self.assertEqual(1, self.console.storage.numPenalties(self.mike, 'TempBan'))

    def test_client_spawn_kill_slap(self):
        pass

    def test_client_spawn_kill_nuke(self):
        pass

    def test_client_spawn_kill_kill(self):
        pass