# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\core\parsers\test_insurgency.py
# Compiled at: 2016-03-08 18:42:10
import os, sys, unittest2 as unittest
from mock import Mock
from mock import patch
from mock import call
from mockito import when
from b3 import TEAM_BLUE, TEAM_FREE
from b3 import TEAM_RED
from b3 import TEAM_UNKNOWN
from b3 import TEAM_SPEC
from b3.clients import Client
from b3.config import XmlConfigParser
from b3.config import CfgConfigParser
from b3.fake import FakeClient
from b3.parsers.insurgency import InsurgencyParser
from b3.plugins.admin import AdminPlugin
from b3 import __file__ as b3_module__file__
ADMIN_CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(b3_module__file__), 'conf/plugin_admin.ini'))
STATUS_RESPONSE = 'hostname: Courgette\'s Server\nversion : 1.17.5.1/11751 5038 secure\nudp/ip  : 11.23.32.44:27015  (public ip: 11.23.32.44)\nos      :  Linux\ntype    :  community dedicated\nmap     : cs_foobar\nplayers : 1 humans, 10 bots (20/20 max) (not hibernating)\n\n# userid name uniqueid connected ping loss state rate adr\n#224 "Moe" BOT active\n#194 2 "courgette" STEAM_1:0:1111111 33:48 67 0 active 20000 11.222.111.222:27005\n#225 "Quintin" BOT active\n#226 "Kurt" BOT active\n#227 "Arnold" BOT active\n#228 "Rip" BOT active\n#229 "Zach" BOT active\n#230 "Wolf" BOT active\n#231 "Minh" BOT active\n#232 "Ringo" BOT active\n#233 "Quade" BOT active\n#end\nL 08/28/2012 - 01:28:40: rcon from "11.222.111.222:4181": command "status"\n'

def client_equal(client_a, client_b):
    if client_a is None and client_b is not None:
        return False
    else:
        if client_a is not None and client_b is None:
            return False
        return all(map(lambda x: getattr(client_a, x, None) == getattr(client_b, x, None), ('cid',
                                                                                            'guid',
                                                                                            'name',
                                                                                            'ip',
                                                                                            'ping')))


WHATEVER = object()

class InsurgencyTestCase(unittest.TestCase):
    """
    Test case that is suitable for testing Insurgency parser specific features
    """

    @classmethod
    def setUpClass(cls):
        from b3.fake import FakeConsole
        InsurgencyParser.__bases__ = (FakeConsole,)

    def setUp(self):
        self.status_response = None
        self.conf = XmlConfigParser()
        self.conf.loadFromString('<configuration></configuration>')
        self.parser = InsurgencyParser(self.conf)
        self.parser.output = Mock()
        self.parser.output.write = Mock(wraps=self.output_write)
        when(self.parser).is_sourcemod_installed().thenReturn(True)
        when(self.parser).getMap().thenReturn('buhriz')
        self.evt_queue = []

        def queue_event(evt):
            self.evt_queue.append(evt)

        self.queueEvent_patcher = patch.object(self.parser, 'queueEvent', wraps=queue_event)
        self.queueEvent_mock = self.queueEvent_patcher.start()
        self.parser.startup()
        return

    def tearDown(self):
        self.queueEvent_patcher.stop()
        if hasattr(self, 'parser'):
            del self.parser.clients
            self.parser.working = False

    def clear_events(self):
        """
        clear the event queue, so when assert_has_event is called, it will look only at the newly caught events.
        """
        self.evt_queue = []

    def assert_has_event(self, event_type, data=WHATEVER, client=WHATEVER, target=WHATEVER):
        """
        assert that self.evt_queue contains at least one event for the given type that has the given characteristics.
        """
        if not isinstance(event_type, basestring):
            raise AssertionError
            expected_event = self.parser.getEvent(event_type, data, client, target)
            len(self.evt_queue) or self.fail('expecting %s. Got no event instead' % expected_event)
        elif len(self.evt_queue) == 1:
            actual_event = self.evt_queue[0]
            self.assertEqual(expected_event.type, actual_event.type)
            if data != WHATEVER:
                self.assertEqual(expected_event.data, actual_event.data)
            if client != WHATEVER:
                self.assertTrue(client_equal(expected_event.client, actual_event.client))
            if target != WHATEVER:
                self.assertTrue(client_equal(expected_event.target, actual_event.target))
        else:
            for evt in self.evt_queue:
                if expected_event.type == evt.type and (expected_event.data == evt.data or data == WHATEVER) and (client_equal(expected_event.client, evt.client) or client == WHATEVER) and (client_equal(expected_event.target, evt.target) or target == WHATEVER):
                    return

            self.fail('expecting event %s. Got instead: %s' % (expected_event, map(str, self.evt_queue)))

    def assert_has_not_event(self, event_type, data=None, client=None, target=None):
        """
        assert that self.evt_queue does not contain at least one event for the given type that has the given characteristics.
        """
        if not isinstance(event_type, basestring):
            raise AssertionError
            unexpected_event = self.parser.getEvent(event_type, data, client, target)
            return len(self.evt_queue) or None

        def event_match(evt):
            return unexpected_event.type == evt.type and (data is None or data == evt.data) and (client is None or client_equal(client, evt.client)) and (target is None or client_equal(target, evt.target))

        if any(map(event_match, self.evt_queue)):
            self.fail('not expecting event %s' % filter(event_match, self.evt_queue))

    def output_write(self, *args, **kwargs):
        """
        Used to override parser self.output.write method so we can control the
        response given to the 'status' rcon command
        """
        if len(args) and args[0] == 'status':
            if self.status_response is not None:
                return self.status_response
            else:
                return STATUS_RESPONSE

        return


class AdminTestCase(unittest.TestCase):
    """
    Test case that is suitable for testing Insurgency parser specific features with the B3 admin plugin available
    """

    @classmethod
    def setUpClass(cls):
        from b3.fake import FakeConsole
        InsurgencyParser.__bases__ = (FakeConsole,)

    def setUp(self):
        self.status_response = None
        self.conf = XmlConfigParser()
        self.conf.loadFromString('<configuration></configuration>')
        self.parser = InsurgencyParser(self.conf)
        self.parser.output = Mock()
        self.parser.output.write = Mock(wraps=sys.stdout.write)
        when(self.parser).is_sourcemod_installed().thenReturn(True)
        adminPlugin_conf = CfgConfigParser()
        adminPlugin_conf.load(ADMIN_CONFIG_FILE)
        adminPlugin = AdminPlugin(self.parser, adminPlugin_conf)
        adminPlugin.onLoadConfig()
        adminPlugin.onStartup()
        when(self.parser).getPlugin('admin').thenReturn(adminPlugin)
        when(self.parser).getAllAvailableMaps().thenReturn(['buhriz', 'district', 'sinjar', 'siege', 'uprising', 'ministry', 'revolt', 'heights', 'contact', 'peak', 'panj', 'market'])
        when(self.parser).getMap().thenReturn('buhriz')
        self.parser.startup()
        self.parser.patch_b3_admin_plugin()
        return

    def tearDown(self):
        if hasattr(self, 'parser'):
            del self.parser.clients
            self.parser.working = False


class Test_gamelog_parsing(InsurgencyTestCase):

    def assertLineIsIgnored(self, line):
        with patch.object(self.parser, 'warning') as (warning_mock):
            self.parser.parseLine(line)
        self.assertFalse(warning_mock.called, line)

    def test_teams(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111', team=None)
        player.connects('194')
        self.clear_events()
        self.parser.parseLine('L 04/01/2014 - 12:56:51: "courgette<194><STEAM_1:0:1111111><#Team_Security>" say "!pb @531 rule1"')
        self.assertEqual(TEAM_RED, player.team)
        self.parser.parseLine('L 04/01/2014 - 12:56:51: "courgette<194><STEAM_1:0:1111111><#Team_Insurgent>" say "!pb @531 rule1"')
        self.assertEqual(TEAM_BLUE, player.team)
        self.parser.parseLine('L 04/01/2014 - 12:56:51: "courgette<194><STEAM_1:0:1111111><#Team_Unassigned>" say "!pb @531 rule1"')
        self.assertEqual(TEAM_UNKNOWN, player.team)
        self.parser.parseLine('L 04/01/2014 - 12:56:51: "courgette<194><STEAM_1:0:1111111><Spectator>" say "!pb @531 rule1"')
        self.assertEqual(TEAM_SPEC, player.team)
        return

    def test_client_say(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111', team=TEAM_BLUE)
        player.connects('194')
        self.clear_events()
        self.parser.parseLine('L 04/01/2014 - 12:56:51: "courgette<194><STEAM_1:0:1111111><#Team_Security>" say "!pb @531 rule1"')
        self.assert_has_event('EVT_CLIENT_SAY', '!pb @531 rule1', player)

    def test_client_disconnect(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111', team=TEAM_BLUE)
        player.connects('194')
        self.clear_events()
        self.parser.parseLine('L 04/01/2014 - 12:56:51: "courgette<194><STEAM_1:0:1111111><#Team_Security>" disconnected (reason "Disconnected.")')
        self.assert_has_event('EVT_CLIENT_DISCONNECT', '194', player)

    def test_client_kick_byconsole(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111', team=TEAM_BLUE)
        player.connects('194')
        self.clear_events()
        self.parser.parseLine('L 04/01/2014 - 12:56:51: "courgette<194><STEAM_1:0:1111111><#Team_Security>" disconnected (reason "Kicked by Console")')
        self.assert_has_event('EVT_CLIENT_DISCONNECT', '194', player)
        self.assert_has_event('EVT_CLIENT_KICK', data={'reason': 'Kicked by Console', 'admin': None}, client=player, target=None)
        return

    def test_client_changed_name__known_client(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111', team=TEAM_UNKNOWN)
        player.connects('194')
        self.clear_events()
        self.parser.parseLine('L 02/07/2015 - 19:36:25: "courgette<194><STEAM_1:0:1111111><#Team_Security>" changed name to "fooobar"')
        self.assert_has_event('EVT_CLIENT_NAME_CHANGE', client=player, data='fooobar')

    def test_client_changed_name__unknown_client(self):
        self.clear_events()
        self.parser.parseLine('L 02/07/2015 - 19:36:25: "courgette2<4><STEAM_1:0:1111112><#Team_Security>" changed name to "fooobar"')
        self.assert_has_event('EVT_CLIENT_NAME_CHANGE', data='fooobar')

    def test_bot_stuck(self):
        with patch.object(self.parser, 'warning') as (warning_mock):
            self.parser.parseLine('L 02/07/2015 - 12:30:01: "Minh<338><BOT><193>" stuck (position "4355.51 -2602.87 143.98") (duration "19.97") L 02/07/2015 - 12:30:01:    path_goal ( "4370.00 -2703.29 148.56" )')
        self.assertFalse(warning_mock.called)

    def test_on_bot_stuck__no_pathgoal(self):
        with patch.object(self.parser, 'warning') as (warning_mock):
            self.parser.parseLine('L 02/07/2015 - 14:53:25: "Abento<616><BOT><193>" stuck (position "-165.03 -705.59 222.38") (duration "1.50")')
        self.assertFalse(warning_mock.called)

    def test_on_cvar_with_space(self):
        self.parser.parseLine('L 02/07/2015 - 14:48:24: "mp_lobbytime" = "10"')
        self.assertEqual('10', self.parser.game.cvar['mp_lobbytime'])
        self.parser.parseLine('L 02/07/2015 - 14:48:24: "nextlevel" = "heights_coop checkpoint"')
        self.assertEqual('heights_coop checkpoint', self.parser.game.cvar['nextlevel'])
        self.parser.parseLine('L 02/07/2015 - 14:48:24: "tv_password" = ""')
        self.assertEqual('', self.parser.game.cvar['tv_password'])
        self.parser.parseLine('L 02/07/2015 - 14:48:24: server_cvar: "nextlevel" ""')
        self.assertEqual('', self.parser.game.cvar['nextlevel'])
        self.parser.parseLine('L 02/07/2015 - 14:48:24: server_cvar: "sv_tags" "cid brutal coop bots hunt unforgiving"')
        self.assertEqual('cid brutal coop bots hunt unforgiving', self.parser.game.cvar['sv_tags'])

    def test_ignored_line(self):
        self.assertLineIsIgnored('L 02/07/2015 - 15:15:22: Log file closed')
        self.assertLineIsIgnored('L 02/07/2015 - 15:15:24: Log file started (file "logs\\L023_081_154_166_23274_201502071515_001.log") (game "C:\\servers\\insurgency") (version "5885")')
        self.assertLineIsIgnored('L 02/07/2015 - 14:53:26:    path_goal ( "-162.50 -750.00 182.68" )')
        self.assertLineIsIgnored('L 02/07/2015 - 19:13:07: Vote succeeded "Kick Based God Allah [U:1:120000090]"')
        self.assertLineIsIgnored('L 02/13/2015 - 18:08:52: "courgette<18><STEAM_1:1:1111111><STEAM_1:1:1111111>" STEAM USERID validated')

    def test_on_team_action(self):
        self.clear_events()
        self.parser.parseLine('L 02/07/2015 - 12:53:23: Team "#Team_Insurgent" triggered "Round_Win"')
        self.assert_has_event('EVT_GAME_ROUND_END', data={'event_name': 'Round_Win', 'properties': '', 
           'team': TEAM_BLUE})

    def test_on_client_action__obj_captured(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111', team=TEAM_BLUE)
        player.connects('194')
        self.clear_events()
        self.parser.parseLine('L 02/07/2015 - 12:31:34: "courgette<195><STEAM_1:0:1111111><#Team_Security>" triggered "obj_captured" (name "#unknown_controlpoint")')
        self.assert_has_event('EVT_CLIENT_ACTION', data='obj_captured')

    def test_on_client_action__obj_destroyed(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111', team=TEAM_BLUE)
        player.connects('194')
        self.clear_events()
        self.parser.parseLine('L 02/07/2015 - 12:55:01: "courgette<195><STEAM_1:0:1111111><#Team_Security>" triggered "obj_destroyed" (name "#unknown_controlpoint")')
        self.assert_has_event('EVT_CLIENT_ACTION', data='obj_destroyed')

    def test_gamerules(self):

        def assertGR(state, event_type):
            self.parser.parseLine("Gamerules: entering state '%s'" % state)
            self.assert_has_event(event_type)

        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111', team=TEAM_BLUE)
        player.connects('194')
        assertGR('GR_STATE_PREGAME', 'EVT_GAME_WARMUP')
        assertGR('GR_STATE_STARTGAME', 'EVT_CLIENT_JOIN')
        assertGR('GR_STATE_RND_RUNNING', 'EVT_GAME_ROUND_START')
        assertGR('GR_STATE_POSTROUND', 'EVT_GAME_ROUND_END')
        assertGR('GR_STATE_GAME_OVER', 'EVT_GAME_EXIT')


class Test_parser_other(InsurgencyTestCase):

    def test_getTeam(self):
        self.assertEqual(TEAM_RED, self.parser.getTeam('#Team_Security'))
        self.assertEqual(TEAM_BLUE, self.parser.getTeam('#Team_Insurgent'))
        self.assertEqual(TEAM_SPEC, self.parser.getTeam('Spectator'))
        self.assertEqual(TEAM_UNKNOWN, self.parser.getTeam('#Team_Unassigned'))
        self.assertEqual(None, self.parser.getTeam(''))
        self.assertEqual(None, self.parser.getTeam(None))
        return


class FunctionalTest(AdminTestCase):

    def test_permban(self):
        superadmin = FakeClient(self.parser, name='superadmin', guid='guid_superadmin', groupBits=128, team=TEAM_UNKNOWN)
        superadmin.connects('1')
        bill = FakeClient(self.parser, name='bill', guid='guid_bill', team=TEAM_UNKNOWN)
        bill.connects('2')
        superadmin.says('!permban bill rule1')
        superadmin.says('!baninfo @%s' % bill.id)
        self.assertListEqual(['Banned: bill (@3) has been added to banlist', 'bill has 1 active bans'], superadmin.message_history)

    def test_map_with_invalid_map_name(self):
        superadmin = FakeClient(self.parser, name='superadmin', guid='guid_superadmin', groupBits=128, team=TEAM_UNKNOWN)
        superadmin.connects('1')
        superadmin.says('!map blargh blub')
        self.assertListEqual(['do you mean : buhriz, district, sinjar, siege, uprising, ministry, revolt, heights, contact, peak, panj, market ?'], superadmin.message_history)

    def test_map_with_correct_parameters(self):
        superadmin = FakeClient(self.parser, name='superadmin', guid='guid_superadmin', groupBits=128, team=TEAM_UNKNOWN)
        superadmin.connects('1')
        superadmin.says('!map market push')
        self.parser.output.write.assert_has_calls([call('changelevel market push')])

    def test_say(self):
        self.parser.msgPrefix = '[Pre]'
        with patch.object(self.parser.output, 'write') as (write_mock):
            self.parser.say('f00')
            write_mock.assert_has_calls([call('sm_say [Pre] f00')])

    def test_say_with_color_codes(self):
        self.parser.msgPrefix = '[Pre]'
        with patch.object(self.parser.output, 'write') as (write_mock):
            self.parser.say('^7message ^1with ^2color ^8codes')
            write_mock.assert_has_calls([call('sm_say [Pre] message with color codes')])

    def test_saybig(self):
        self.parser.msgPrefix = '[Pre]'
        with patch.object(self.parser.output, 'write') as (write_mock):
            self.parser.saybig('f00')
            write_mock.assert_has_calls([call('sm_hsay [Pre] f00')])

    def test_saybig_with_color_codes(self):
        self.parser.msgPrefix = '[Pre]'
        with patch.object(self.parser.output, 'write') as (write_mock):
            self.parser.saybig('^7message ^1with ^2color ^8codes')
            write_mock.assert_has_calls([call('sm_hsay [Pre] message with color codes')])

    def test_message(self):
        self.parser.msgPrefix = '[Pre]'
        player = Client(console=self.parser, guid='theGuid')
        with patch.object(self.parser.output, 'write') as (write_mock):
            player.message('f00')
            write_mock.assert_has_calls([call('sm_psay #theGuid "[Pre] f00"')])

    def test_message_with_color_codes(self):
        self.parser.msgPrefix = '[Pre]'
        player = Client(console=self.parser, guid='theGuid')
        with patch.object(self.parser.output, 'write') as (write_mock):
            player.message('^7message ^1with ^2color ^8codes')
            write_mock.assert_has_calls([call('sm_psay #theGuid "[Pre] message with color codes"')])


class Test_getClientOrCreate(InsurgencyTestCase):

    def test_changing_team(self):
        client = self.parser.getClientOrCreate(cid='2', guid='AAAAAAAAAAAA000000000000000', name='theName', team=TEAM_UNKNOWN)
        self.assertEqual(TEAM_UNKNOWN, client.team)

        def assertTeam(excepted_team, new_team):
            self.parser.getClientOrCreate(cid='2', guid='AAAAAAAAAAAA000000000000000', name='theName', team=new_team)
            self.assertEqual(excepted_team, client.team)

        assertTeam(TEAM_UNKNOWN, None)
        assertTeam(TEAM_UNKNOWN, '')
        assertTeam(TEAM_RED, '#Team_Security')
        assertTeam(TEAM_RED, 'f00')
        assertTeam(TEAM_BLUE, '#Team_Insurgent')
        assertTeam(TEAM_UNKNOWN, '#Team_Unassigned')
        assertTeam(TEAM_SPEC, 'Spectator')
        assertTeam(TEAM_SPEC, 'f00')
        assertTeam(TEAM_BLUE, '#Team_Insurgent')
        assertTeam(TEAM_UNKNOWN, '#Team_Unassigned')
        assertTeam(TEAM_RED, '#Team_Security')
        return