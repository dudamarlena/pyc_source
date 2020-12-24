# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_callvote.py
# Compiled at: 2015-05-27 19:37:28
import unittest2
from textwrap import dedent
from mockito import when
from b3 import TEAM_BLUE
from b3 import TEAM_RED
from b3 import TEAM_SPEC
from b3.cvar import Cvar
from b3.config import MainConfig
from b3.config import CfgConfigParser
from b3.config import XmlConfigParser
from b3.plugins.admin import AdminPlugin
from b3.plugins.callvote import CallvotePlugin
from b3.parsers.iourt42 import Iourt42Parser
from tests import logging_disabled

class CallvoteTestCase(unittest2.TestCase):

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

    def tearDown(self):
        self.console.working = False


class Test_events(CallvoteTestCase):

    def setUp(self):
        CallvoteTestCase.setUp(self)
        with logging_disabled():
            from b3.fake import FakeClient
        self.mike = FakeClient(console=self.console, name='Mike', guid='mikeguid', team=TEAM_RED, groupBits=128)
        self.bill = FakeClient(console=self.console, name='Bill', guid='billguid', team=TEAM_BLUE, groupBits=16)
        self.mark = FakeClient(console=self.console, name='Mark', guid='markguid', team=TEAM_RED, groupBits=2)
        self.sara = FakeClient(console=self.console, name='Sara', guid='saraguid', team=TEAM_SPEC, groupBits=1)
        self.conf = CfgConfigParser()
        self.p = CallvotePlugin(self.console, self.conf)

    def init(self, config_content=None):
        if config_content:
            self.conf.loadFromString(config_content)
        else:
            self.conf.loadFromString(dedent('\n                [callvoteminlevel]\n                capturelimit: guest\n                clientkick: guest\n                clientkickreason: guest\n                cyclemap: guest\n                exec: guest\n                fraglimit: guest\n                kick: guest\n                map: guest\n                reload: guest\n                restart: guest\n                shuffleteams: guest\n                swapteams: guest\n                timelimit: guest\n                g_bluewaverespawndelay: guest\n                g_bombdefusetime: guest\n                g_bombexplodetime: guest\n                g_capturescoretime: guest\n                g_friendlyfire: guest\n                g_followstrict: guest\n                g_gametype: guest\n                g_gear: guest\n                g_matchmode: guest\n                g_maxrounds: guest\n                g_nextmap: guest\n                g_redwaverespawndelay: guest\n                g_respawndelay: guest\n                g_roundtime: guest\n                g_timeouts: guest\n                g_timeoutlength: guest\n                g_swaproles: guest\n                g_waverespawns: guest\n\n                [callvotespecialmaplist]\n                #ut4_abbey: guest\n                #ut4_abbeyctf: guest\n\n                [commands]\n                lastvote: mod\n                veto: mod\n            '))
        self.p.onLoadConfig()
        self.p.onStartup()
        when(self.p).getTime().thenReturn(1399725576)

    def tearDown(self):
        self.mike.disconnects()
        self.bill.disconnects()
        self.mark.disconnects()
        self.sara.disconnects()
        CallvoteTestCase.tearDown(self)

    def test_client_callvote_legit(self):
        self.init()
        self.mike.connects('1')
        self.bill.connects('2')
        self.mark.connects('3')
        self.sara.connects('4')
        self.console.parseLine('Callvote: 1 - "map ut4_dressingroom"')
        self.assertIsNotNone(self.p.callvote)
        self.assertEqual(self.mike, self.p.callvote['client'])
        self.assertEqual('map', self.p.callvote['type'])
        self.assertEqual('ut4_dressingroom', self.p.callvote['args'])
        self.assertEqual(1399725576, self.p.callvote['time'])
        self.assertEqual(3, self.p.callvote['max_num'])

    def test_client_callvote_not_enough_level(self):
        self.init(dedent('\n            [callvoteminlevel]\n            clientkick: admin\n            clientkickreason: admin\n            kick: admin\n        '))
        self.mike.connects('1')
        self.bill.connects('2')
        self.mark.connects('3')
        self.sara.connects('4')
        self.sara.clearMessageHistory()
        self.console.parseLine('Callvote: 4 - "kick bill"')
        self.assertIsNone(self.p.callvote)
        self.assertListEqual(["You can't issue this callvote. Required level: Admin"], self.sara.message_history)

    def test_client_callvote_map_not_enough_level(self):
        self.init(dedent('\n            [callvotespecialmaplist]\n            ut4_abbey: admin\n            ut4_abbeyctf: superadmin\n        '))
        self.mike.connects('1')
        self.bill.connects('2')
        self.mark.connects('3')
        self.sara.connects('4')
        self.sara.clearMessageHistory()
        self.console.parseLine('Callvote: 4 - "map ut4_abbey"')
        self.assertIsNone(self.p.callvote)
        self.assertListEqual(["You can't issue this callvote. Required level: Admin"], self.sara.message_history)

    def test_client_callvote_passed(self):
        self.init()
        self.mike.connects('1')
        self.bill.connects('2')
        self.mark.connects('3')
        self.sara.connects('4')
        self.console.parseLine('Callvote: 4 - "map ut4_casa"')
        self.console.parseLine('VotePassed: 3 - 0 - "map ut4_casa"')
        self.assertIsNotNone(self.p.callvote)
        self.assertEqual(self.sara, self.p.callvote['client'])
        self.assertEqual('map', self.p.callvote['type'])
        self.assertEqual('ut4_casa', self.p.callvote['args'])
        self.assertEqual(1399725576, self.p.callvote['time'])
        self.assertEqual(4, self.p.callvote['max_num'])
        self.assertEqual(3, self.p.callvote['num_yes'])
        self.assertEqual(0, self.p.callvote['num_no'])

    def test_client_callvote_failed(self):
        self.init()
        self.mike.connects('1')
        self.bill.connects('2')
        self.mark.connects('3')
        self.sara.connects('4')
        self.console.parseLine('Callvote: 4 - "map ut4_casa"')
        self.console.parseLine('VotePassed: 1 - 3 - "map ut4_casa"')
        self.assertIsNotNone(self.p.callvote)
        self.assertEqual(self.sara, self.p.callvote['client'])
        self.assertEqual('map', self.p.callvote['type'])
        self.assertEqual('ut4_casa', self.p.callvote['args'])
        self.assertEqual(1399725576, self.p.callvote['time'])
        self.assertEqual(4, self.p.callvote['max_num'])
        self.assertEqual(1, self.p.callvote['num_yes'])
        self.assertEqual(3, self.p.callvote['num_no'])

    def test_client_callvote_finish_with_none_callvote_object(self):
        self.init()
        self.mike.connects('1')
        self.bill.connects('2')
        self.mark.connects('3')
        self.sara.connects('4')
        self.console.parseLine('VotePassed: 3 - 0 - "map ut4_casa"')
        self.assertIsNone(self.p.callvote)

    def test_client_callvote_finish_with_different_arguments(self):
        self.init()
        self.mike.connects('1')
        self.bill.connects('2')
        self.mark.connects('3')
        self.sara.connects('4')
        self.console.parseLine('Callvote: 4 - "map ut4_casa"')
        self.console.parseLine('VotePassed: 1 - 3 - "reload"')
        self.assertIsNone(self.p.callvote)


class Test_commands(CallvoteTestCase):

    def setUp(self):
        CallvoteTestCase.setUp(self)
        with logging_disabled():
            from b3.fake import FakeClient
        self.mike = FakeClient(console=self.console, name='Mike', guid='mikeguid', team=TEAM_RED, groupBits=128)
        self.bill = FakeClient(console=self.console, name='Bill', guid='billguid', team=TEAM_BLUE, groupBits=16)
        self.mark = FakeClient(console=self.console, name='Mark', guid='markguid', team=TEAM_RED, groupBits=2)
        self.sara = FakeClient(console=self.console, name='Sara', guid='saraguid', team=TEAM_SPEC, groupBits=1)
        self.conf = CfgConfigParser()
        self.p = CallvotePlugin(self.console, self.conf)

    def init(self, config_content=None):
        if config_content:
            self.conf.loadFromString(config_content)
        else:
            self.conf.loadFromString(dedent('\n                [callvoteminlevel]\n                capturelimit: guest\n                clientkick: guest\n                clientkickreason: guest\n                cyclemap: guest\n                exec: guest\n                fraglimit: guest\n                kick: guest\n                map: guest\n                reload: guest\n                restart: guest\n                shuffleteams: guest\n                swapteams: guest\n                timelimit: guest\n                g_bluewaverespawndelay: guest\n                g_bombdefusetime: guest\n                g_bombexplodetime: guest\n                g_capturescoretime: guest\n                g_friendlyfire: guest\n                g_followstrict: guest\n                g_gametype: guest\n                g_gear: guest\n                g_matchmode: guest\n                g_maxrounds: guest\n                g_nextmap: guest\n                g_redwaverespawndelay: guest\n                g_respawndelay: guest\n                g_roundtime: guest\n                g_timeouts: guest\n                g_timeoutlength: guest\n                g_swaproles: guest\n                g_waverespawns: guest\n\n                [callvotespecialmaplist]\n                #ut4_abbey: guest\n                #ut4_abbeyctf: guest\n\n                [commands]\n                lastvote: mod\n                veto: mod\n            '))
        self.p.onLoadConfig()
        self.p.onStartup()
        when(self.p).getTime().thenReturn(1399725576)

    def tearDown(self):
        self.mike.disconnects()
        self.bill.disconnects()
        self.mark.disconnects()
        self.sara.disconnects()
        CallvoteTestCase.tearDown(self)

    def test_cmd_veto(self):
        self.init()
        self.mike.connects('1')
        self.bill.connects('2')
        self.mark.connects('3')
        self.sara.connects('4')
        self.console.parseLine('Callvote: 4 - "map ut4_dressingroom"')
        self.mike.says('!veto')
        self.assertIsNone(self.p.callvote)

    def test_cmd_lastvote_legit(self):
        self.init()
        self.mike.connects('1')
        self.bill.connects('2')
        self.mark.connects('3')
        self.sara.connects('4')
        self.console.parseLine('Callvote: 4 - "map ut4_casa"')
        self.p.callvote['time'] = self.p.getTime() - 10
        self.console.parseLine('VotePassed: 3 - 0 - "map ut4_casa"')
        self.mike.clearMessageHistory()
        self.mike.says('!lastvote')
        self.assertIsNotNone(self.p.callvote)
        self.assertListEqual(['Last vote issued by Sara 10 seconds ago',
         'Type: map - Data: ut4_casa',
         'Result: 3:0 on 4 clients'], self.mike.message_history)