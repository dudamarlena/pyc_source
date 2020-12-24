# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_jumper.py
# Compiled at: 2015-05-27 19:37:28
import json, unittest2
from textwrap import dedent
from mock import Mock
from mockito import when
from b3 import TEAM_FREE, TEAM_SPEC
from b3.cvar import Cvar
from b3.config import MainConfig
from b3.config import XmlConfigParser
from b3.config import CfgConfigParser
from b3.parsers.iourt42 import Iourt42Parser
from b3.plugins.admin import AdminPlugin
from b3.plugins.jumper import JumperPlugin
from b3.plugins.jumper import JumpRun
from tests import logging_disabled
MAPDATA_JSON = '{"ut4_uranus_beta1a": {"size": 1841559, "nom": "Uranus", "njump": "22", "mdate": "2013-01-16", "pk3":\n"ut4_uranus_beta1a", "level": 50, "id": 308, "utversion": 2, "nway": 1, "howjump": "", "mapper": "Levant"},\n"ut4_crouchtraining_a1": {"size": 993461, "nom": "Crouch Training", "njump": "11", "mdate": "2010-12-31",\n"pk3": "ut4_crouchtraining_a1", "level": 79, "id": 346, "utversion": 2, "nway": 1, "howjump": "", "mapper": "spidercochon"}}'

class JumperTestCase(unittest2.TestCase):

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
        self.conf.loadFromString(dedent('\n            [settings]\n            demorecord: no\n            skipstandardmaps: yes\n            minleveldelete: senioradmin\n\n            [commands]\n            delrecord: guest\n            maprecord: guest\n            mapinfo: guest\n            record: guest\n            setway: senioradmin\n            topruns: guest\n            map: fulladmin\n            maps: user\n            setnextmap: admin\n        '))
        self.p = JumperPlugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        when(self.p).getMapsDataFromApi().thenReturn(json.loads(MAPDATA_JSON))

    def tearDown(self):
        self.console.working = False


class Test_events(JumperTestCase):

    def setUp(self):
        JumperTestCase.setUp(self)
        with logging_disabled():
            from b3.fake import FakeClient
        self.mike = FakeClient(console=self.console, name='Mike', guid='mikeguid', team=TEAM_FREE, groupBits=1)
        self.bill = FakeClient(console=self.console, name='Bill', guid='billguid', team=TEAM_FREE, groupBits=1)
        self.mike.connects('1')
        self.bill.connects('2')
        self.console.game.mapName = 'ut42_bstjumps_u2'

    def tearDown(self):
        self.mike.disconnects()
        self.bill.disconnects()
        JumperTestCase.tearDown(self)

    def test_event_client_jumprun_started(self):
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.mike, data={'way_id': '1'}))
        self.assertEqual(True, self.mike.isvar(self.p, 'jumprun'))
        self.assertIsNone(self.mike.var(self.p, 'jumprun').value.demo)
        self.assertIsInstance(self.mike.var(self.p, 'jumprun').value, JumpRun)

    def test_event_client_jumprun_stopped(self):
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_STOP', client=self.mike, data={'way_id': '1', 'way_time': '12345'}))
        self.assertEqual(False, self.mike.isvar(self.p, 'jumprun'))
        self.assertListEqual([], self.p.getClientRecords(self.mike, self.console.game.mapName))

    def test_event_client_jumprun_canceled(self):
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_CANCEL', client=self.mike, data={'way_id': '1'}))
        self.assertEqual(False, self.mike.isvar(self.p, 'jumprun'))
        self.assertListEqual([], self.p.getClientRecords(self.mike, self.console.game.mapName))

    def test_event_client_jumprun_started_stopped(self):
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.mike, data={'way_id': '1'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_STOP', client=self.mike, data={'way_id': '1', 'way_time': '12345'}))
        self.assertEqual(False, self.mike.isvar(self.p, 'jumprun'))
        self.assertEqual(1, len(self.p.getClientRecords(self.mike, self.console.game.mapName)))

    def test_event_client_jumprun_started_canceled(self):
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.mike, data={'way_id': '1'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_CANCEL', client=self.mike, data={'way_id': '1'}))
        self.assertEqual(False, self.mike.isvar(self.p, 'jumprun'))
        self.assertEqual(0, len(self.p.getClientRecords(self.mike, self.console.game.mapName)))

    def test_event_client_jumprun_started_stopped_multiple_clients(self):
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.mike, data={'way_id': '1'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_STOP', client=self.mike, data={'way_id': '1', 'way_time': '12345'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.bill, data={'way_id': '1'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_STOP', client=self.bill, data={'way_id': '1', 'way_time': '12345'}))
        self.assertEqual(False, self.mike.isvar(self.p, 'jumprun'))
        self.assertEqual(False, self.bill.isvar(self.p, 'jumprun'))
        self.assertEqual(1, len(self.p.getClientRecords(self.mike, self.console.game.mapName)))
        self.assertEqual(1, len(self.p.getClientRecords(self.bill, self.console.game.mapName)))

    def test_event_client_jumprun_started_stopped_multiple_ways(self):
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.mike, data={'way_id': '1'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_STOP', client=self.mike, data={'way_id': '1', 'way_time': '12345'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.mike, data={'way_id': '2'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_STOP', client=self.mike, data={'way_id': '2', 'way_time': '12345'}))
        self.assertEqual(False, self.mike.isvar(self.p, 'jumprun'))
        self.assertEqual(2, len(self.p.getClientRecords(self.mike, self.console.game.mapName)))

    def test_event_client_jumprun_started_stopped_multiple_clients_multiple_ways(self):
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.mike, data={'way_id': '1'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_STOP', client=self.mike, data={'way_id': '1', 'way_time': '12345'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.mike, data={'way_id': '2'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_STOP', client=self.mike, data={'way_id': '2', 'way_time': '12345'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.bill, data={'way_id': '1'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_STOP', client=self.bill, data={'way_id': '1', 'way_time': '12345'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.bill, data={'way_id': '2'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_STOP', client=self.bill, data={'way_id': '2', 'way_time': '12345'}))
        self.assertEqual(False, self.mike.isvar(self.p, 'jumprun'))
        self.assertEqual(False, self.bill.isvar(self.p, 'jumprun'))
        self.assertEqual(2, len(self.p.getClientRecords(self.mike, self.console.game.mapName)))
        self.assertEqual(2, len(self.p.getClientRecords(self.bill, self.console.game.mapName)))

    def test_event_game_map_change(self):
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.mike, data={'way_id': '1'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.bill, data={'way_id': '1'}))
        self.console.queueEvent(self.console.getEvent('EVT_GAME_MAP_CHANGE', data='\\sv_allowdownload\x00\\g_matchmode\x00\\g_gametype\\9\\sv_maxclients\x1a\\sv_floodprotect\x01'))
        self.assertEqual(False, self.mike.isvar(self.p, 'jumprun'))
        self.assertEqual(False, self.bill.isvar(self.p, 'jumprun'))
        self.assertListEqual([], self.p.getClientRecords(self.mike, self.console.game.mapName))
        self.assertListEqual([], self.p.getClientRecords(self.bill, self.console.game.mapName))

    def test_event_client_disconnect(self):
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.mike, data={'way_id': '1'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_DISCONNECT', client=self.mike, data=None))
        self.assertEqual(False, self.mike.isvar(self.p, 'jumprun'))
        return

    def test_event_client_team_change(self):
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.mike, data={'way_id': '1'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.bill, data={'way_id': '1'}))
        self.mike.team = TEAM_SPEC
        self.bill.team = TEAM_FREE
        self.assertEqual(TEAM_SPEC, self.mike.team)
        self.assertEqual(TEAM_FREE, self.bill.team)
        self.assertEqual(False, self.mike.isvar(self.p, 'jumprun'))
        self.assertEqual(True, self.bill.isvar(self.p, 'jumprun'))
        self.assertIsInstance(self.bill.var(self.p, 'jumprun').value, JumpRun)

    def test_plugin_disable(self):
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.mike, data={'way_id': '1'}))
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_JUMP_RUN_START', client=self.bill, data={'way_id': '1'}))
        self.p.disable()
        self.assertEqual(False, self.mike.isvar(self.p, 'jumprun'))
        self.assertEqual(False, self.bill.isvar(self.p, 'jumprun'))

    def test_plugin_enable(self):
        self.p.console.write = Mock()
        self.p.disable()
        self.p._cycle_count = 0
        self.console.game.mapName = 'ut4_casa'
        self.p.enable()
        self.p.console.write.assert_called_with('cyclemap')
        self.assertEqual(1, self.p._cycle_count)


class Test_commands(JumperTestCase):

    def setUp(self):
        JumperTestCase.setUp(self)
        with logging_disabled():
            from b3.fake import FakeClient
        self.mike = FakeClient(console=self.console, name='Mike', guid='mikeguid', team=TEAM_FREE, groupBits=128)
        self.bill = FakeClient(console=self.console, name='Bill', guid='billguid', team=TEAM_FREE, groupBits=1)
        self.mark = FakeClient(console=self.console, name='Mark', guid='markguid', team=TEAM_FREE, groupBits=1)
        self.mike.connects('1')
        self.bill.connects('2')
        self.mark.connects('3')
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.console.parseLine('ClientJumpRunStarted: 1 - way: 1')
        self.console.parseLine('ClientJumpRunStopped: 1 - way: 1 - time: 537000')
        self.console.parseLine('ClientJumpRunStarted: 2 - way: 1')
        self.console.parseLine('ClientJumpRunStopped: 2 - way: 1 - time: 349000')
        self.console.parseLine('ClientJumpRunStarted: 3 - way: 1')
        self.console.parseLine('ClientJumpRunStopped: 3 - way: 1 - time: 122000')
        self.console.parseLine('ClientJumpRunStarted: 1 - way: 2')
        self.console.parseLine('ClientJumpRunStopped: 1 - way: 2 - time: 84000')
        self.console.parseLine('ClientJumpRunStarted: 2 - way: 2')
        self.console.parseLine('ClientJumpRunStopped: 2 - way: 2 - time: 91000')
        self.console.parseLine('ClientJumpRunStarted: 3 - way: 2')
        self.console.parseLine('ClientJumpRunStopped: 3 - way: 2 - time: 177000')
        self.console.game.mapName = 'ut42_jupiter'
        self.console.parseLine('ClientJumpRunStarted: 1 - way: 1')
        self.console.parseLine('ClientJumpRunStopped: 1 - way: 1 - time: 123000')
        self.console.parseLine('ClientJumpRunStarted: 2 - way: 1')
        self.console.parseLine('ClientJumpRunStopped: 2 - way: 1 - time: 543000')
        self.console.parseLine('ClientJumpRunStarted: 1 - way: 2')
        self.console.parseLine('ClientJumpRunStopped: 1 - way: 2 - time: 79000')
        when(self.console).getMaps().thenReturn(['ut4_abbey', 'ut4_abbeyctf', 'ut4_algiers', 'ut4_ambush',
         'ut4_austria', 'ut42_bstjumps_u2', 'ut4_bohemia', 'ut4_casa', 'ut4_cascade', 'ut4_commune',
         'ut4_company', 'ut4_crossing', 'ut4_docks', 'ut4_dressingroom', 'ut4_eagle', 'ut4_elgin',
         'ut4_firingrange', 'ut4_ghosttown_rc4', 'ut4_harbortown', 'ut4_herring', 'ut4_horror', 'ut42_jupiter',
         'ut4_kingdom', 'ut4_kingpin', 'ut4_mandolin', 'ut4_mars_b1', 'ut4_maya', 'ut4_oildepot', 'ut4_prague',
         'ut4_prague_v2', 'ut4_raiders', 'ut4_ramelle', 'ut4_ricochet', 'ut4_riyadh', 'ut4_sanc', 'ut4_snoppis',
         'ut4_suburbs', 'ut4_subway', 'ut4_swim', 'ut4_thingley', 'ut4_tombs', 'ut4_toxic',
         'ut4_tunis', 'ut4_turnpike', 'ut4_uptown'])

    def tearDown(self):
        self.mike.disconnects()
        self.bill.disconnects()
        self.mark.disconnects()
        JumperTestCase.tearDown(self)

    def test_cmd_client_record_no_arguments(self):
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.mike.clearMessageHistory()
        self.mike.says('!record')
        self.assertListEqual(['listing records for Mike (@%s) on ut42_bstjumps_u2:' % self.mike.id,
         '[1] 0:08:57.000 since %s' % JumperPlugin.getDateString(self.console.time()),
         '[2] 0:01:24.000 since %s' % JumperPlugin.getDateString(self.console.time())], self.mike.message_history)

    def test_cmd_client_record_single_argument(self):
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.mike.clearMessageHistory()
        self.mike.says('!record bill')
        self.assertListEqual(['listing records for Bill (@%s) on ut42_bstjumps_u2:' % self.bill.id,
         '[1] 0:05:49.000 since %s' % JumperPlugin.getDateString(self.console.time()),
         '[2] 0:01:31.000 since %s' % JumperPlugin.getDateString(self.console.time())], self.mike.message_history)

    def test_cmd_client_record_double_arguments(self):
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.mike.clearMessageHistory()
        self.mike.says('!record bill jupiter')
        self.assertListEqual(['[1] 0:09:03.000 since %s' % JumperPlugin.getDateString(self.console.time())], self.mike.message_history)

    def test_cmd_client_record_double_arguments_no_record(self):
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.mike.clearMessageHistory()
        self.mike.says('!record mark jupiter')
        self.assertListEqual(['no record found for Mark (@%s) on ut42_jupiter' % self.mark.id], self.mike.message_history)

    def test_cmd_maprecord_no_arguments(self):
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.mike.clearMessageHistory()
        self.mike.says('!maprecord')
        self.assertListEqual(['listing map records on ut42_bstjumps_u2:',
         '[1] Mark (@%s) with 0:02:02.000' % self.mark.id,
         '[2] Mike (@%s) with 0:01:24.000' % self.mike.id], self.mike.message_history)

    def test_cmd_maprecord_with_arguments(self):
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.mike.clearMessageHistory()
        self.mike.says('!maprecord jupiter')
        self.assertListEqual(['listing map records on ut42_jupiter:',
         '[1] Mike (@%s) with 0:02:03.000' % self.mike.id,
         '[2] Mike (@%s) with 0:01:19.000' % self.mike.id], self.mike.message_history)

    def test_cmd_maprecord_with_arguments_no_record(self):
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.mike.clearMessageHistory()
        self.mike.says('!maprecord mars')
        self.assertListEqual(['no record found on ut4_mars_b1'], self.mike.message_history)

    def test_cmd_topruns_no_arguments(self):
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.mike.clearMessageHistory()
        self.mike.says('!topruns')
        self.assertListEqual(['listing top runs on ut42_bstjumps_u2:',
         '[1] #1 Mark (@%s) with 0:02:02.000' % self.mark.id,
         '[1] #2 Bill (@%s) with 0:05:49.000' % self.bill.id,
         '[1] #3 Mike (@%s) with 0:08:57.000' % self.mike.id,
         '[2] #1 Mike (@%s) with 0:01:24.000' % self.mike.id,
         '[2] #2 Bill (@%s) with 0:01:31.000' % self.bill.id,
         '[2] #3 Mark (@%s) with 0:02:57.000' % self.mark.id], self.mike.message_history)

    def test_cmd_topruns_with_arguments(self):
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.mike.clearMessageHistory()
        self.mike.says('!topruns jupiter')
        self.assertListEqual(['listing top runs on ut42_jupiter:',
         '[1] #1 Mike (@%s) with 0:02:03.000' % self.mike.id,
         '[1] #2 Bill (@%s) with 0:09:03.000' % self.bill.id,
         '[2] #1 Mike (@%s) with 0:01:19.000' % self.mike.id], self.mike.message_history)

    def test_cmd_topruns_with_arguments_no_record(self):
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.mike.clearMessageHistory()
        self.mike.says('!topruns mars')
        self.assertListEqual(['no record found on ut4_mars_b1'], self.mike.message_history)

    def test_cmd_delrecord_no_arguments(self):
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.mike.clearMessageHistory()
        self.mike.says('!delrecord')
        self.assertListEqual(['removed 2 records for Mike (@%s) on ut42_bstjumps_u2' % self.mike.id], self.mike.message_history)
        self.assertListEqual([], self.p.getClientRecords(self.mike, 'ut42_bstjumps_u2'))

    def test_cmd_delrecord_with_one_argument(self):
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.mike.clearMessageHistory()
        self.mike.says('!delrecord bill')
        self.assertListEqual(['removed 2 records for Bill (@%s) on ut42_bstjumps_u2' % self.bill.id], self.mike.message_history)
        self.assertListEqual([], self.p.getClientRecords(self.bill, 'ut42_bstjumps_u2'))

    def test_cmd_delrecord_with_two_arguments(self):
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.mike.clearMessageHistory()
        self.mike.says('!delrecord bill jupiter')
        self.assertListEqual(['removed 1 record for Bill (@%s) on ut42_jupiter' % self.bill.id], self.mike.message_history)
        self.assertListEqual([], self.p.getClientRecords(self.bill, 'ut42_jupiter'))

    def test_cmd_delrecord_with_two_arguments_no_record(self):
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.mike.clearMessageHistory()
        self.mike.says('!delrecord mark jupiter')
        self.assertListEqual(['no record found for Mark (@%s) on ut42_jupiter' % self.mark.id], self.mike.message_history)

    def test_cmd_setway(self):
        self.console.game.mapName = 'ut42_bstjumps_u2'
        self.mike.clearMessageHistory()
        self.mike.says('!setway 1 Rookie')
        self.mike.says('!setway 2 Explorer')
        self.mike.clearMessageHistory()
        self.mike.says('!maprecord')
        self.assertListEqual(['listing map records on ut42_bstjumps_u2:',
         '[Rookie] Mark (@%s) with 0:02:02.000' % self.mark.id,
         '[Explorer] Mike (@%s) with 0:01:24.000' % self.mike.id], self.mike.message_history)

    def test_cmd_maps(self):
        self.mike.clearMessageHistory()
        self.mike.says('!maps')
        self.assertListEqual(['map rotation: ut42_bstjumps_u2, ut42_jupiter, ut4_mars_b1'], self.mike.message_history)

    def test_cmd_map_valid_name(self):
        self.mike.clearMessageHistory()
        self.mike.says('!map jup')
        self.assertListEqual(['changing map to ut42_jupiter'], self.mike.message_history)

    def test_cmd_map_invalid_name(self):
        self.mike.clearMessageHistory()
        self.mike.says('!map f00')
        self.assertListEqual(['do you mean: ut42_bstjumps_u2, ut4_mars_b1, ut42_jupiter?'], self.mike.message_history)