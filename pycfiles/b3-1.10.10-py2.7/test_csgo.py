# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\core\parsers\test_csgo.py
# Compiled at: 2016-03-08 18:42:10
from mock import Mock, call, patch
from mockito import when, verify
import sys, unittest2 as unittest
from b3 import TEAM_BLUE, TEAM_RED, TEAM_UNKNOWN, TEAM_SPEC
from b3.clients import Client
from b3.config import XmlConfigParser
from b3.fake import FakeClient
from b3.parsers.csgo import CsgoParser
WAS_FROSTBITE_LOADED = 'b3.parsers.frostbite' in sys.modules.keys() or 'b3.parsers.frostbite2' in sys.modules.keys()
STATUS_RESPONSE = 'hostname: Courgette\'s Server\nversion : 1.17.5.1/11751 5038 secure\nudp/ip  : 11.23.32.44:27015  (public ip: 11.23.32.44)\nos      :  Linux\ntype    :  community dedicated\nmap     : cs_foobar\nplayers : 1 humans, 10 bots (20/20 max) (not hibernating)\n\n# userid name uniqueid connected ping loss state rate adr\n#224 "Moe" BOT active\n# 194 2 "courgette" STEAM_1:0:1111111 33:48 67 0 active 20000 11.222.111.222:27005\n#225 "Quintin" BOT active\n#226 "Kurt" BOT active\n#227 "Arnold" BOT active\n#228 "Rip" BOT active\n#229 "Zach" BOT active\n#230 "Wolf" BOT active\n#231 "Minh" BOT active\n#232 "Ringo" BOT active\n#233 "Quade" BOT active\n#end\nL 08/28/2012 - 01:28:40: rcon from "11.222.111.222:4181": command "status"\n'

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

class CsgoTestCase(unittest.TestCase):
    """
    Test case that is suitable for testing CS:GO parser specific features
    """

    @classmethod
    def setUpClass(cls):
        from b3.fake import FakeConsole
        CsgoParser.__bases__ = (FakeConsole,)

    def setUp(self):
        self.status_response = None
        self.conf = XmlConfigParser()
        self.conf.loadFromString('<configuration></configuration>')
        self.parser = CsgoParser(self.conf)
        self.parser.output = Mock()
        self.parser.output.write = Mock(wraps=self.output_write)
        when(self.parser).is_sourcemod_installed().thenReturn(True)
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
        """Used to override parser self.output.write method so we can control the response given to the 'status'
        rcon command"""
        if len(args) and args[0] == 'status':
            if self.status_response is not None:
                return self.status_response
            else:
                return STATUS_RESPONSE

        return


class Test_gamelog_parsing(CsgoTestCase):

    def test_server_cvars_start(self):
        self.queueEvent_mock.reset_mock()
        self.parser.parseLine('L 08/26/2012 - 05:46:50: server cvars start')
        self.assertFalse(self.queueEvent_mock.called)

    def test_server_cvars_end(self):
        self.queueEvent_mock.reset_mock()
        self.parser.parseLine('L 08/26/2012 - 05:46:50: server cvars end')
        self.assertFalse(self.queueEvent_mock.called)

    def test_killed(self):
        bot22 = FakeClient(self.parser, name='Pheonix', guid='BOT_22')
        bot17 = FakeClient(self.parser, name='Ringo', guid='BOT_17')
        bot22.connects('22')
        bot17.connects('17')
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 03:46:44: "Pheonix<22><BOT><TERRORIST>" killed "Ringo<17><BOT><CT>" with "glock" (headshot)')
        self.assert_has_event('EVT_CLIENT_KILL', client=bot22, target=bot17, data=(100,
                                                                                   'glock',
                                                                                   'head',
                                                                                   None))
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 03:46:44: "Pheonix<22><BOT><TERRORIST>" killed "Ringo<17><BOT><CT>" with "glock"')
        self.assert_has_event('EVT_CLIENT_KILL', client=bot22, target=bot17, data=(100,
                                                                                   'glock',
                                                                                   'body',
                                                                                   None))
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 03:46:44: "Pheonix<22><BOT><TERRORIST>" [280 -133 -223] killed "Ringo<17><BOT><CT>" [-216 397 -159] with "aug"')
        self.assert_has_event('EVT_CLIENT_KILL', client=bot22, target=bot17, data=(100,
                                                                                   'aug',
                                                                                   'body',
                                                                                   None))
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 03:46:44: "Pheonix<22><BOT><TERRORIST>" [280 -133 -223] killed "Ringo<17><BOT><CT>" [-216 397 -159] with "aug" (headshot)')
        self.assert_has_event('EVT_CLIENT_KILL', client=bot22, target=bot17, data=(100,
                                                                                   'aug',
                                                                                   'head',
                                                                                   None))
        return

    def test_killed_but_really_is_teamkill(self):
        bot22 = FakeClient(self.parser, name='Pheonix', guid='BOT_22')
        bot17 = FakeClient(self.parser, name='Ringo', guid='BOT_17')
        bot22.connects('22')
        bot17.connects('17')
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 03:46:44: "Pheonix<22><BOT><TERRORIST>" killed "Ringo<17><BOT><TERRORIST>" with "glock"')
        self.assert_has_event('EVT_CLIENT_KILL_TEAM', client=bot22, target=bot17, data=(100,
                                                                                        'glock',
                                                                                        'body',
                                                                                        None))
        return

    def test_killed_but_really_is_suicide(self):
        bot22 = FakeClient(self.parser, name='Pheonix', guid='BOT_22')
        bot22.connects('22')
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 03:46:44: "Pheonix<22><BOT><TERRORIST>" killed "Pheonix<22><BOT><TERRORIST>" with "glock"')
        self.assert_has_event('EVT_CLIENT_SUICIDE', client=bot22, target=bot22, data=(100,
                                                                                      'glock',
                                                                                      'body',
                                                                                      None))
        return

    def test_committed_suicide(self):
        bot22 = FakeClient(self.parser, name='Pheonix', guid='BOT_22')
        bot22.connects('22')
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 03:38:04: "Pheonix<22><BOT><TERRORIST>" committed suicide with "world"')
        self.assert_has_event('EVT_CLIENT_SUICIDE', client=bot22, target=bot22, data=(100,
                                                                                      'world',
                                                                                      'body',
                                                                                      None))
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 03:38:04: "Pheonix<22><BOT><TERRORIST>" [-1889 1328 -152] committed suicide with "world"')
        self.assert_has_event('EVT_CLIENT_SUICIDE', client=bot22, target=bot22, data=(100,
                                                                                      'world',
                                                                                      'body',
                                                                                      None))
        return

    def test_server_cvar(self):
        self.parser.game.cvar = {}
        self.parser.parseLine('L 08/26/2012 - 03:49:58: server_cvar: "mp_freezetime" "5"')
        self.assertDictEqual({'mp_freezetime': '5'}, self.parser.game.cvar)

    def test_cvar(self):
        self.parser.game.cvar = {}
        self.parser.parseLine('L 08/26/2012 - 03:49:56: "decalfrequency" = "10"')
        self.assertDictEqual({'decalfrequency': '10'}, self.parser.game.cvar)

    def test_map_change(self):
        self.parser.game.mapName = 'old'
        self.parser.parseLine('L 08/27/2012 - 23:57:14: -------- Mapchange to de_dust --------')
        self.assertEqual('de_dust', self.parser.game.mapName)

    def test_loading_map(self):
        self.parser.game.mapName = 'old'
        self.parser.parseLine('L 08/26/2012 - 03:49:56: Loading map "de_nuke"')
        self.assertEqual('de_nuke', self.parser.game.mapName)

    def test_started_map(self):
        self.parser.game.mapName = 'old'
        self.parser.parseLine('L 08/26/2012 - 03:22:35: Started map "de_dust" (CRC "1592693790")')
        self.assertEqual('de_dust', self.parser.game.mapName)

    def test_userid_validated(self):
        self.assertIsNone(self.parser.clients.getByCID('2'))
        self.parser.parseLine('L 08/26/2012 - 03:22:36: "courgette<2><STEAM_1:0:1111111><>" STEAM USERID validated')
        client = self.parser.clients.getByCID('2')
        self.assertIsNotNone(client)
        self.assertEqual('courgette', client.name)
        self.assertEqual('STEAM_1:0:1111111', client.guid)
        self.assert_has_event('EVT_CLIENT_CONNECT', data=client, client=client)
        self.assert_has_event('EVT_CLIENT_AUTH', data=client, client=client)

    def test_player_connected(self):
        self.assertIsNone(self.parser.clients.getByCID('2'))
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 03:22:36: "courgette<2><STEAM_1:0:1111111><>" connected, address "11.222.111.222:27005"')
        client = self.parser.clients.getByCID('2')
        self.assertIsNotNone(client)
        self.assertEqual('courgette', client.name)
        self.assertEqual('STEAM_1:0:1111111', client.guid)
        self.assertEqual('11.222.111.222', client.ip)
        self.assert_has_event('EVT_CLIENT_CONNECT', data=client, client=client)
        self.assert_has_event('EVT_CLIENT_AUTH', data=client, client=client)
        clients_from_storage = self.parser.storage.getClientsMatching({'%name%': 'courgette'})
        self.assertEqual(1, len(clients_from_storage))
        client_from_storage = clients_from_storage[0]
        self.assertEqual('courgette', client_from_storage.name)
        self.assertEqual('STEAM_1:0:1111111', client_from_storage.guid)
        self.assertEqual('11.222.111.222', client_from_storage.ip)
        self.assertDictContainsSubset({'clients': 2}, self.parser.storage.getCounts())

    def test_player_connected__unicode(self):
        self.assertIsNone(self.parser.clients.getByCID('2'))
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 03:22:36: "Spoon««<2><STEAM_1:0:1111111><>" connected, address "11.222.111.222:27005"')
        client = self.parser.clients.getByCID('2')
        self.assertIsNotNone(client)
        self.assertFalse(client.hide)
        self.assertEqual('Spoon««', client.name)
        self.assertEqual('STEAM_1:0:1111111', client.guid)
        self.assertEqual('11.222.111.222', client.ip)
        self.assert_has_event('EVT_CLIENT_CONNECT', data=client, client=client)
        self.assert_has_event('EVT_CLIENT_AUTH', data=client, client=client)
        clients_from_storage = self.parser.storage.getClientsMatching({'%name%': 'Spoon'})
        self.assertEqual(1, len(clients_from_storage))
        client_from_storage = clients_from_storage[0]
        self.assertEqual('Spoon««', client_from_storage.name)
        self.assertEqual('STEAM_1:0:1111111', client_from_storage.guid)
        self.assertEqual('11.222.111.222', client_from_storage.ip)
        self.assertDictContainsSubset({'clients': 2}, self.parser.storage.getCounts())

    def test_bot_connected(self):
        self.assertIsNone(self.parser.clients.getByCID('3'))
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 03:22:36: "Moe<3><BOT><>" connected, address "none"')
        client = self.parser.clients.getByCID('3')
        self.assertIsNotNone(client)
        self.assertTrue(client.bot)
        self.assertEqual('Moe', client.name)
        self.assertEqual('BOT3', client.guid)
        self.assertEqual('', client.ip)
        self.assert_has_event('EVT_CLIENT_CONNECT', data=client, client=client)
        self.assert_has_not_event('EVT_CLIENT_AUTH', data=client, client=client)
        clients_from_storage = self.parser.storage.getClientsMatching({'%name%': 'Moe'})
        self.assertListEqual([], clients_from_storage)
        self.assertDictContainsSubset({'clients': 2}, self.parser.storage.getCounts())

    def test_kicked_by_console(self):
        bot22 = FakeClient(self.parser, name='Pheonix', guid='BOT_22')
        bot22.connects('22')
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 04:45:04: "Pheonix<22><BOT><TERRORIST>" disconnected (reason "Kicked by Console")')
        self.assert_has_event('EVT_CLIENT_KICK', data={'reason': 'Kicked by Console', 'admin': None}, client=bot22)
        self.assert_has_event('EVT_CLIENT_DISCONNECT', data='22', client=bot22)
        return

    def test_player_entered(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111')
        player.connects('2')
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 05:38:36: "courgette<2><STEAM_1:0:1111111><>" entered the game')
        self.assert_has_event('EVT_CLIENT_JOIN', client=player)

    def test_bot_entered(self):
        bot22 = FakeClient(self.parser, name='Pheonix', guid='BOT_22')
        bot22.connects('22')
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 05:29:48: "Pheonix<22><BOT><>" entered the game')
        self.assert_has_event('EVT_CLIENT_JOIN', client=bot22)

    def test_player_join_team(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111')
        player.connects('2')
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 03:22:36: "courgette<2><STEAM_1:0:1111111><Unassigned>" joined team "CT"')
        self.assert_has_event('EVT_CLIENT_TEAM_CHANGE', data=TEAM_RED, client=player)
        self.assertEqual(TEAM_RED, player.team)

    def test_bot_join_team(self):
        bot22 = FakeClient(self.parser, name='Pheonix', guid='BOT_11')
        bot22.connects('11')
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 03:22:36: "Pheonix<11><BOT><Unassigned>" joined team "TERRORIST"')
        self.assert_has_event('EVT_CLIENT_TEAM_CHANGE', data=TEAM_BLUE, client=bot22)
        self.assertEqual(TEAM_BLUE, bot22.team)

    def test_player_switched_team(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111', team=TEAM_RED)
        player.connects('2')
        self.assertEqual(TEAM_RED, player.team)
        self.clear_events()
        self.parser.parseLine('L 07/17/2013 - 20:27:54: "courgette<2><STEAM_1:0:1111111>" switched from team <CT> to <TERRORIST>')
        self.assert_has_event('EVT_CLIENT_TEAM_CHANGE', data=TEAM_BLUE, client=player)
        self.assertEqual(TEAM_BLUE, player.team)

    def test_player_switched_team_to_Unassigned(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111', team=TEAM_RED)
        player.connects('2')
        self.assertEqual(TEAM_RED, player.team)
        self.clear_events()
        self.parser.parseLine('L 07/17/2013 - 20:27:54: "courgette<2><STEAM_1:0:1111111>" switched from team <CT> to <Unassigned>')
        self.assert_has_event('EVT_CLIENT_TEAM_CHANGE', data=TEAM_UNKNOWN, client=player)
        self.assertEqual(TEAM_UNKNOWN, player.team)

    def test_bot_switched_team(self):
        bot22 = FakeClient(self.parser, name='Pheonix', guid='BOT_11')
        bot22.connects('11')
        self.clear_events()
        self.parser.parseLine('L 07/17/2013 - 20:27:54: "Pheonix<11><BOT>" switched from team <Unassigned> to <TERRORIST>')
        self.assert_has_event('EVT_CLIENT_TEAM_CHANGE', data=TEAM_BLUE, client=bot22)
        self.assertEqual(TEAM_BLUE, bot22.team)

    def test_player_purchased_item(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111')
        player.connects('2')
        self.clear_events()
        self.parser.parseLine('L 07/17/2013 - 20:27:54: "courgette<2><STEAM_1:0:1111111><CT>" purchased "negev"')
        self.assert_has_event('EVT_CLIENT_ACTION', data='purchased "negev"', client=player)

    def test_player_threw_item(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111')
        player.connects('2')
        self.clear_events()
        self.parser.parseLine('L 07/17/2013 - 20:27:54: "courgette<2><STEAM_1:0:1111111><CT>" threw molotov [59 386 -225]')
        self.assert_has_event('EVT_CLIENT_ACTION', data='threw "molotov"', client=player)

    def test_player_assited_killing(self):
        bot22 = FakeClient(self.parser, name='Pheonix', guid='BOT_22')
        bot17 = FakeClient(self.parser, name='Ringo', guid='BOT_17')
        bot22.connects('22')
        bot17.connects('17')
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 03:46:44: "Pheonix<22><BOT><TERRORIST>" assisted killing "Ringo<17><BOT><CT>"')
        self.assert_has_event('EVT_CLIENT_ACTION', client=bot22, target=bot17, data='assisted killing')

    def test_world_triggered_event__Round_End(self):
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 03:22:36: World triggered "Round_End"')
        self.assert_has_event('EVT_GAME_ROUND_END')

    def test_world_triggered_event__Round_Start(self):
        with patch.object(self.parser.game, 'startRound') as (startRound_mock):
            self.assertFalse(startRound_mock.called)
            self.parser.parseLine('L 08/26/2012 - 03:22:36: World triggered "Round_Start"')
            self.assertTrue(startRound_mock.called)
            self.assert_has_event('EVT_GAME_ROUND_START')

    def test_world_triggered_event__Game_Commencing(self):
        with patch.object(self.parser, 'warning') as (warning_mock):
            self.clear_events()
            self.parser.parseLine('L 08/26/2012 - 03:22:36: World triggered "Game_Commencing"')
            self.assertEqual([], self.evt_queue)
            self.assertFalse(warning_mock.called)

    def test_world_triggered_event__killlocation(self):
        with patch.object(self.parser, 'warning') as (warning_mock):
            self.clear_events()
            self.assertIsNone(self.parser.last_killlocation_properties)
            self.parser.parseLine('L 08/29/2012 - 22:26:59: World triggered "killlocation" (attacker_position "-282 749 -21") (victim_position "68 528 64")')
            self.assertEqual([], self.evt_queue)
            self.assertEqual(' (attacker_position "-282 749 -21") (victim_position "68 528 64")', self.parser.last_killlocation_properties)
            self.assertFalse(warning_mock.called)

    def test_world_triggered_event__unknown_event(self):
        with patch.object(self.parser, 'warning') as (warning_mock):
            self.clear_events()
            self.parser.parseLine('L 08/26/2012 - 03:22:36: World triggered "f00"')
            self.assertEqual([], self.evt_queue)
            self.assertTrue(warning_mock.called)
            warning_mock.assert_has_calls([call("unexpected world event : 'f00' : please report this on the B3 forums")])

    def test_client_triggered_event__known(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111')
        player.connects('2')

        def assertEvent(event_name):
            self.clear_events()
            self.parser.parseLine('L 08/26/2012 - 05:04:55: "courgette<2><STEAM_1:0:1111111><CT>" triggered "%s"' % event_name)
            self.assert_has_event('EVT_CLIENT_ACTION', data=event_name, client=player)

        assertEvent('Got_The_Bomb')
        assertEvent('Dropped_The_Bomb')
        assertEvent('Begin_Bomb_Defuse_Without_Kit')
        assertEvent('Begin_Bomb_Defuse_With_Kit')
        assertEvent('Planted_The_Bomb')
        assertEvent('headshot')
        assertEvent('Rescued_A_Hostage')
        assertEvent('Touched_A_Hostage')
        assertEvent('Escaped_As_VIP')
        assertEvent('Became_VIP')
        assertEvent('Killed_A_Hostage')

    def test_client_triggered_event__unknown(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111', team=TEAM_RED)
        player.connects('2')
        with patch.object(self.parser, 'warning') as (warning_mock):
            self.clear_events()
            self.parser.parseLine('L 08/26/2012 - 05:04:55: "courgette<2><STEAM_1:0:1111111><CT>" triggered "f00"')
            self.assertEqual([], self.evt_queue)
            self.assertTrue(warning_mock.called)
            warning_mock.assert_has_calls([call("unknown client event : 'f00' : please report this on the B3 forums")])

    def test_team_triggered_event__known(self):

        def assert_unknown_event_warning_called(event_name, expect_unknown=True):
            with patch.object(self.parser, 'warning') as (warning_mock):
                self.clear_events()
                self.parser.parseLine('L 08/26/2012 - 03:48:09: Team "CT" triggered "%s" (CT "3") (T "5")' % event_name)
            self.assertEqual([], self.evt_queue)
            self.assertEqual(expect_unknown, warning_mock.called, warning_mock.mock_calls)
            if expect_unknown:
                warning_mock.assert_has_calls([call("unexpected team event : '%s' : please report this on the B3 forums" % event_name)])

        assert_unknown_event_warning_called('bar')
        assert_unknown_event_warning_called('SFUI_Notice_Target_Saved', expect_unknown=False)
        assert_unknown_event_warning_called('SFUI_Notice_Target_Bombed', expect_unknown=False)
        assert_unknown_event_warning_called('SFUI_Notice_Terrorists_Win', expect_unknown=False)
        assert_unknown_event_warning_called('SFUI_Notice_CTs_Win', expect_unknown=False)
        assert_unknown_event_warning_called('SFUI_Notice_Bomb_Defused', expect_unknown=False)

    def test_client_say(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111', team=TEAM_BLUE)
        player.connects('2')
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 05:09:55: "courgette<2><STEAM_1:0:1111111><CT>" say "!iamgod"')
        self.assert_has_event('EVT_CLIENT_SAY', '!iamgod', player)

    def test_client_say__no_team(self):
        player = FakeClient(self.parser, name='Spoon', guid='STEAM_1:0:10000000', team=TEAM_UNKNOWN)
        player.connects('2')
        self.clear_events()
        self.parser.parseLine('L 09/16/2012 - 04:55:17: "Spoon<2><STEAM_1:0:10000000><>" say "!h"')
        self.assert_has_event('EVT_CLIENT_SAY', '!h', player)

    def test_client_teamsay(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111', team=TEAM_BLUE)
        player.connects('2')
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 05:04:44: "courgette<2><STEAM_1:0:1111111><CT>" say_team "team say"')
        self.assert_has_event('EVT_CLIENT_TEAM_SAY', 'team say', player)

    def test_bad_rcon_password(self):
        with patch.object(self.parser, 'error') as (error_mock):
            self.parser.parseLine('L 08/26/2012 - 05:21:23: rcon from "78.207.134.100:15073": Bad Password')
            self.assertTrue(error_mock.called)
            error_mock.assert_has_calls([call('Bad RCON password, check your b3.xml file')])

    def test_clantag(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111', team=TEAM_BLUE)
        player.connects('2')
        self.assertFalse(hasattr(player, 'clantag'))
        self.parser.parseLine('L 08/26/2012 - 05:43:31: "courgette<2><STEAM_1:0:1111111><CT>" triggered "clantag" (value "f00")')
        self.assertEqual('f00', player.clantag)

    def test_Banid(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111')
        player.connects('2')
        player.disconnects()
        self.clear_events()
        self.parser.parseLine('L 08/28/2012 - 00:03:01: Banid: "courgette<91><STEAM_1:0:1111111><>" was banned "for 1.00 minutes" by "Console"')
        self.assert_has_event('EVT_CLIENT_BAN_TEMP', {'reason': None, 'duration': '1.00 minutes', 'admin': 'Console'}, player)
        return

    def test_kick(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111')
        player.connects('2')
        player.disconnects()
        self.clear_events()
        self.parser.parseLine('L 08/28/2012 - 00:12:07: [basecommands.smx] "Console<0><Console><Console>" kicked "courgette<91><STEAM_1:0:1111111><>" (reason "f00")')
        self.assert_has_event('EVT_CLIENT_KICK', {'reason': 'f00', 'admin': None}, player)
        return

    def test_EVT_SUPERLOGS_WEAPONSTATS(self):
        bot48 = FakeClient(self.parser, name='Gunner', guid='BOT_48', team=TEAM_RED)
        bot48.connects('48')
        self.clear_events()
        self.parser.parseLine('L 08/28/2012 - 14:58:55: "Gunner<48><BOT><CT>" triggered "weaponstats" (weapon "m4a1") (shots "13") (hits "2") (kills "0") (headshots "0") (tks "0") (damage "42") (deaths "0")')
        self.assert_has_event('EVT_SUPERLOGS_WEAPONSTATS', client=bot48, data={'weapon': 'm4a1', 
           'shots': '13', 
           'hits': '2', 
           'kills': '0', 
           'headshots': '0', 
           'tks': '0', 
           'damage': '42', 
           'deaths': '0'})

    def test_EVT_SUPERLOGS_WEAPONSTATS2(self):
        bot = FakeClient(self.parser, name='Vitaliy', guid='BOT_51', team=TEAM_RED)
        bot.connects('51')
        self.clear_events()
        self.parser.parseLine('L 08/28/2012 - 14:58:55: "Vitaliy<51><BOT><CT>" triggered "weaponstats2" (weapon "famas") (head "0") (chest "0") (stomach "1") (leftarm "0") (rightarm "0") (leftleg "0") (rightleg "0")')
        self.assert_has_event('EVT_SUPERLOGS_WEAPONSTATS2', client=bot, data={'weapon': 'famas', 
           'head': '0', 
           'chest': '0', 
           'stomach': '1', 
           'leftarm': '0', 
           'rightarm': '0', 
           'leftleg': '0', 
           'rightleg': '0'})

    def test_unknown_line(self):
        with patch.object(self.parser, 'warning') as (warning_mock):
            self.clear_events()
            self.parser.parseLine('L 08/26/2012 - 05:04:55: f00')
            self.assertEqual([], self.evt_queue)
            self.assertTrue(warning_mock.called)
            warning_mock.assert_has_calls([call('unhandled log line : f00 : please report this on the B3 forums')])

    def test_killed_with_SuperLogs_plugin(self):
        bot22 = FakeClient(self.parser, name='Pheonix', guid='BOT_22', team=TEAM_BLUE)
        bot17 = FakeClient(self.parser, name='Ringo', guid='BOT_17', team=TEAM_RED)
        bot4 = FakeClient(self.parser, name='F00', guid='BOT_4', team=TEAM_BLUE)
        bot22.connects('22')
        bot17.connects('17')
        bot4.connects('4')
        self.clear_events()
        self.parser.parseLine('L 08/29/2012 - 22:26:59: World triggered "killlocation" (attacker_position "-282 749 -21") (victim_position "68 528 64")')
        self.parser.parseLine('L 08/26/2012 - 03:46:44: "Pheonix<22><BOT><TERRORIST>" killed "Ringo<17><BOT><CT>" with "glock" (headshot)')
        self.parser.parseLine('L 08/26/2012 - 03:46:44: "F00<4><BOT><TERRORIST>" killed "Ringo<17><BOT><CT>" with "glock" (headshot)')
        self.assert_has_event('EVT_CLIENT_KILL', client=bot22, target=bot17, data=(100, 'glock', 'head', None, {'attacker_position': '-282 749 -21', 'victim_position': '68 528 64'}))
        self.assert_has_event('EVT_CLIENT_KILL', client=bot4, target=bot17, data=(100,
                                                                                  'glock',
                                                                                  'head',
                                                                                  None))
        return

    def test_basechat_smx(self):
        self.clear_events()
        self.parser.parseLine('L 09/12/2012 - 23:15:47: [basechat.smx] "Console<0><Console><Console>" triggered sm_say (text f00)')
        self.assertListEqual([], self.evt_queue)

    def test_rcon_from(self):
        self.clear_events()
        self.parser.parseLine('L 09/12/2012 - 23:24:02: rcon from "78.207.134.100:3804": command "sm_say fOO)"')
        self.assertListEqual([], self.evt_queue)

    def test_server_need_restart(self):
        self.clear_events()
        self.parser.parseLine('L 09/17/2012 - 23:41:44: Your server needs to be restarted in order to receive the latest update.')
        self.assert_has_event('EVT_SERVER_REQUIRES_RESTART', data='Your server needs to be restarted in order to receive the latest update.')

    def test_server_need_restart_2(self):
        self.clear_events()
        self.parser.parseLine('L 09/17/2012 - 23:41:44: Your server is out of date.  Please update and restart.')
        self.assert_has_event('EVT_SERVER_REQUIRES_RESTART', data='Your server is out of date.  Please update and restart.')


class Test_parser_API(CsgoTestCase):

    def setUp(self):
        self.conf = XmlConfigParser()
        self.conf.loadFromString('<configuration></configuration>')
        self.parser = CsgoParser(self.conf)
        self.parser.output = Mock()
        when(self.parser.output).write('status').thenReturn(STATUS_RESPONSE)
        when(self.parser).is_sourcemod_installed().thenReturn(True)
        self.parser.startup()

    def tearDown(self):
        if hasattr(self, 'parser'):
            del self.parser.clients
            self.parser.working = False

    def test_getPlayerList(self):
        with patch.object(self.parser, 'queryServerInfo') as (queryServerInfo_Mock):
            c3 = Mock()
            c4 = Mock()
            c12 = Mock()
            queryServerInfo_Mock.return_value = {'3': c3, '4': c4, '12': c12}
            rv = self.parser.getPlayerList()
            self.assertDictEqual({'3': c3, '4': c4, '12': c12}, rv)

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

    def test_kick(self):
        player = Client(console=self.parser, cid='4', guid='theGuid', name='theName')
        with patch.object(self.parser.output, 'write') as (write_mock):
            player.kick(reason='f00')
            write_mock.assert_has_calls([call('sm_kick #4 f00')])

    def test_ban(self):
        player = Client(console=self.parser, cid='2', name='courgette', guid='STEAM_1:0:1111111')
        self.clear_events()
        with patch.object(self.parser.output, 'write') as (write_mock):
            self.parser.ban(player, reason='test')
        write_mock.assert_has_calls([call('sm_addban 0 "STEAM_1:0:1111111" test'),
         call('sm_kick #2 test'),
         call('sm_say courgette was banned test')])

    def test_ban__not_connected(self):
        player = Client(console=self.parser, cid=None, name='courgette', guid='STEAM_1:0:1111111')
        self.clear_events()
        with patch.object(self.parser.output, 'write') as (write_mock):
            self.parser.ban(player, reason='test')
        write_mock.assert_has_calls([call('sm_addban 0 "STEAM_1:0:1111111" test'),
         call('sm_say courgette was banned test')])
        return

    def test_unban(self):
        player = Client(console=self.parser, cid=None, name='courgette', guid='STEAM_1:0:1111111')
        self.clear_events()
        with patch.object(self.parser.output, 'write') as (write_mock):
            self.parser.unban(player)
        write_mock.assert_has_calls([call('sm_unban "STEAM_1:0:1111111"')])
        return

    def test_tempban(self):
        player = Client(console=self.parser, cid='2', name='courgette', guid='STEAM_1:0:1111111')
        self.clear_events()
        with patch.object(self.parser.output, 'write') as (write_mock):
            self.parser.tempban(player, reason='test', duration='45m')
        write_mock.assert_has_calls([call('sm_addban 45 "STEAM_1:0:1111111" test'),
         call('sm_kick #2 test'),
         call('sm_say courgette was temp banned for 45 minutes test')])

    def test_getMap(self):
        rv = self.parser.getMap()
        self.assertEqual('cs_foobar', rv)

    def test_getMaps(self):
        when(self.parser.output).write('listmaps').thenReturn('Map Cycle:\ncs_italy\nde_dust\nde_aztec\ncs_office\nde_dust2\nde_train\nde_inferno\nde_nuke\nL 08/28/2012 - 01:16:28: rcon from "11.222.111.222:4107": command "listmaps"\n')
        maps = self.parser.getMaps()
        verify(self.parser.output).write('listmaps')
        self.assertListEqual(['cs_italy',
         'de_dust',
         'de_aztec',
         'cs_office',
         'de_dust2',
         'de_train',
         'de_inferno',
         'de_nuke'], maps)

    @patch('time.sleep')
    def test_rotateMap(self, sleep_mock):
        when(self.parser).getNextMap().thenReturn('the_next_map')
        with patch.object(self.parser.output, 'write') as (write_mock):
            self.parser.rotateMap()
        write_mock.assert_has_calls([call('sm_hsay Changing to next map : the_next_map'),
         call('map the_next_map')])
        sleep_mock.assert_called_once_with(1)

    def test_changeMap(self):
        when(self.parser).getMapsSoundingLike('de_f00').thenReturn('de_f00')
        with patch.object(self.parser.output, 'write') as (write_mock):
            self.parser.changeMap('de_f00')
        write_mock.assert_has_calls([call('sm_map de_f00')])

    def test_changeMap__suggestions(self):
        when(self.parser).getMapsSoundingLike('f00').thenReturn(['de_f001', 'de_f002'])
        with patch.object(self.parser.output, 'write') as (write_mock):
            rv = self.parser.changeMap('f00')
        self.assertSetEqual(set(['de_f001', 'de_f002']), set(rv))
        self.assertEqual(0, write_mock.call_count)

    def test_getPlayerPings(self):
        with patch.object(self.parser, 'queryServerInfo') as (queryServerInfo_Mock):
            queryServerInfo_Mock.return_value = {'3': Client(ping='45'), 
               '4': Client(ping='112'), 
               '12': Client(ping='54')}
            rv = self.parser.getPlayerPings()
            self.assertEqual(3, len(rv))
            self.assertEqual('45', rv['3'])
            self.assertEqual('112', rv['4'])
            self.assertEqual('54', rv['12'])

    @unittest.skip('TODO')
    def test_getPlayerScores(self):
        pass

    @unittest.skip('TODO')
    def test_inflictCustomPenalty(self):
        pass


class Test_parser_other(CsgoTestCase):

    def test_getTeam(self):
        self.assertEqual(TEAM_RED, self.parser.getTeam('CT'))
        self.assertEqual(TEAM_BLUE, self.parser.getTeam('TERRORIST'))
        self.assertEqual(TEAM_UNKNOWN, self.parser.getTeam('Unassigned'))
        self.assertEqual(TEAM_SPEC, self.parser.getTeam('Spectator'))

    def test_getNextMap(self):
        when(self.parser.output).write('sm_nextmap').thenReturn('"sm_nextmap" = "de_dust" ( def. "" ) notify\nL 09/18/2012 - 00:10:00: rcon from "78.207.134.100:4652": command "sm_nextmap"\n')
        nextmap = self.parser.getNextMap()
        verify(self.parser.output).write('sm_nextmap')
        self.assertEqual('de_dust', nextmap)

    def test_getAvailableMaps(self):
        when(self.parser.output).write('maps *').thenReturn('-------------\nPENDING:   (fs) ar_baggage.bsp\nPENDING:   (fs) ar_shoots.bsp\nPENDING:   (fs) cs_italy.bsp\nPENDING:   (fs) cs_italy_se.bsp\nPENDING:   (fs) cs_office.bsp\nPENDING:   (fs) training1.bsp')
        maps = self.parser.getAvailableMaps()
        verify(self.parser.output).write('maps *')
        self.assertListEqual(['ar_baggage', 'ar_shoots', 'cs_italy', 'cs_italy_se', 'cs_office', 'training1'], maps)

    def test_getMapsSoundingLike(self):
        available_maps = [
         'ar_baggage', 'ar_shoots', 'cs_italy', 'cs_italy_se', 'de_bank', 'de_dust']
        when(self.parser).getAvailableMaps().thenReturn(available_maps)
        for available_map in available_maps:
            self.assertEqual(available_map, self.parser.getMapsSoundingLike(available_map))

        self.assertEqual('ar_baggage', self.parser.getMapsSoundingLike('baggage'))
        self.assertEqual('ar_baggage', self.parser.getMapsSoundingLike('bagg'))
        self.assertEqual('ar_baggage', self.parser.getMapsSoundingLike('bag'))
        self.assertEqual('ar_shoots', self.parser.getMapsSoundingLike('shoots'))
        self.assertEqual('ar_shoots', self.parser.getMapsSoundingLike('shoot'))
        self.assertEqual('de_bank', self.parser.getMapsSoundingLike('bank'))
        self.assertEqual('de_dust', self.parser.getMapsSoundingLike('dust'))
        self.assertSetEqual(set(['ar_baggage', 'ar_shoots']), set(self.parser.getMapsSoundingLike('ar')))
        self.assertSetEqual(set(['cs_italy', 'cs_italy_se']), set(self.parser.getMapsSoundingLike('cs')))
        self.assertSetEqual(set(['de_bank', 'de_dust']), set(self.parser.getMapsSoundingLike('de')))
        self.assertSetEqual(set(['cs_italy', 'cs_italy_se']), set(self.parser.getMapsSoundingLike('italy')))

    def test_queryServerInfo(self):
        rv = self.parser.queryServerInfo()
        self.assertEqual('cs_foobar', self.parser.game.mapName)
        self.assertEqual("Courgette's Server", self.parser.game.sv_hostname)
        self.assertEqual(1, len(rv))
        client = rv['194']
        self.assertEqual('194', client.cid)
        self.assertEqual('courgette', client.name)
        self.assertEqual('STEAM_1:0:1111111', client.guid)
        self.assertEqual('67', client.ping)
        self.assertEqual('11.222.111.222', client.ip)

    def test_status_response_utf8_encoded(self):

        def assert_client(rv, cid, name, guid, ping, ip):
            self.assertIn(cid, rv)
            client = rv[cid]
            self.assertEqual(cid, client.cid)
            self.assertEqual(name, client.name)
            self.assertEqual(guid, client.guid)
            self.assertEqual(ping, client.ping)
            self.assertEqual(ip, client.ip)

        self.status_response = ('hostname: UK - #2 Zombie Escape || FastDL - EHDGaming.co.uk [B3]\nversion : 1.18.0.3/11803 5045 secure\nudp/ip  : 109.70.148.17:27017  (public ip: 109.70.148.17)\nos      :  Windows\ntype    :  community dedicated\nplayers : 14 humans, 0 bots (56/56 max) (not hibernating)\n\n# userid name uniqueid connected ping loss state rate adr\n# 12 1 "nooky treac" STEAM_1:1:00000807 28:23 505 6 spawning 30000 111.111.181.248:27005\n#  4 2 "karta218" STEAM_1:0:00000003 34:30 548 0 spawning 10000 111.111.114.142:27005\n# 30 3 "骨 xX Assassine Xx 骨 ;)" STEAM_1:0:00000823 00:05 111 82 spawning 30000 194.208.143.16:27005\n#  6 4 "Spoon" STEAM_1:0:00000181 33:33 43 0 active 30000 111.111.82.35:27005\n#  7 5 "MercenarianWolf" STEAM_1:1:00000526 30:31 320 0 spawning 10000 111.111.13.88:27005\n# 10 6 "eci" STEAM_1:0:00000740 28:47 35 16 active 30000 111.111.74.202:27005\n# 11 8 "The Artist" STEAM_1:1:00000719 28:37 64 0 active 30000 111.111.93.239:27005\n# 27 9 "=LIS=" STEAM_1:1:00000643 03:41 61 0 active 30000 111.111.30.26:27005\n# 15 10 "ErayTR" STEAM_1:1:00000976 25:32 108 0 active 30000 111.111.117.145:27005\n# 28 11 "ackop6uhka96" STEAM_1:1:00000052 02:16 90 0 active 30000 111.111.229.26:27005\n# 25 12 "кровососуший" STEAM_1:1:00000018 04:11 91 0 active 20000 111.111.237.162:27594\n# 29 13 "WahOO" STEAM_1:1:00000678 00:22 69 0 active 20000 111.111.98.248:27005\n# 23 14 "MṢ Xilver" STEAM_1:0:00000813 09:22 131 0 spawning 30000 111.111.215.27:27005\n# 26 15 "Argon" STEAM_1:1:00000243 04:04 163 0 spawning 30000 111.111.197.113:27005\n#end\nL 09/10/2012 - 15:21:28: rcon from "109.70.148.17:3552": command "status"').decode('UTF-8')
        rv = self.parser.queryServerInfo()
        self.assertEqual('cs_foobar', self.parser.game.mapName)
        self.assertEqual('UK - #2 Zombie Escape || FastDL - EHDGaming.co.uk [B3]', self.parser.game.sv_hostname)
        self.assertEqual(14, len(rv))
        assert_client(rv, '12', 'nooky treac', 'STEAM_1:1:00000807', '505', '111.111.181.248')
        assert_client(rv, '4', 'karta218', 'STEAM_1:0:00000003', '548', '111.111.114.142')
        assert_client(rv, '30', '骨 xX Assassine Xx 骨 ;)', 'STEAM_1:0:00000823', '111', '194.208.143.16')
        self.assertIn('6', rv)
        self.assertIn('7', rv)
        self.assertIn('10', rv)
        self.assertIn('11', rv)
        self.assertIn('27', rv)
        self.assertIn('15', rv)
        self.assertIn('28', rv)
        assert_client(rv, '25', 'кровососуший', 'STEAM_1:1:00000018', '91', '111.111.237.162')
        assert_client(rv, '23', 'MṢ Xilver', 'STEAM_1:0:00000813', '131', '111.111.215.27')
        self.assertIn('26', rv)

    def test_loaded_sm_plugins(self):
        when(self.parser.output).write('sm plugins list').thenReturn('[SM] Listing 19 plugins:\n01 "Basic Ban Commands" (1.5.0-dev+3635) by AlliedModders LLC\n02 "B3 Say" (1.0.0.0) by Spoon\n03 "Basic Commands" (1.5.0-dev+3635) by AlliedModders LLC\n04 "Fun Commands" (1.5.0-dev+3635) by AlliedModders LLC\n05 "Basic Chat" (1.5.0-dev+3635) by AlliedModders LLC\n06 "Admin Help" (1.5.0-dev+3635) by AlliedModders LLC\n07 "Reserved Slots" (1.5.0-dev+3635) by AlliedModders LLC\n08 "Sound Commands" (1.5.0-dev+3635) by AlliedModders LLC\n09 "Player Commands" (1.5.0-dev+3635) by AlliedModders LLC\n10 "Admin Menu" (1.5.0-dev+3635) by AlliedModders LLC\n11 "Basic Votes" (1.5.0-dev+3635) by AlliedModders LLC\n12 "Client Preferences" (1.5.0-dev+3635) by AlliedModders LLC\n13 "Nextmap" (1.5.0-dev+3635) by AlliedModders LLC\n14 "SuperLogs: CSS" (1.2.4) by psychonic\n15 "Admin File Reader" (1.5.0-dev+3635) by AlliedModders LLC\n16 "Basic Comm Control" (1.5.0-dev+3635) by AlliedModders LLC\n17 "Basic Info Triggers" (1.5.0-dev+3635) by AlliedModders LLC\n18 "Anti-Flood" (1.5.0-dev+3635) by AlliedModders LLC\n19 "Fun Votes" (1.5.0-dev+3635) by AlliedModders LLC\nL 09/13/2012 - 09:06:45: rcon from "78.207.134.100:2212": command "sm plugins list"')
        rv = self.parser.get_loaded_sm_plugins()
        self.assertDictEqual({'Basic Ban Commands': ('01', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'B3 Say': ('02', '1.0.0.0', 'Spoon'), 
           'Basic Commands': ('03', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'Fun Commands': ('04', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'Basic Chat': ('05', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'Admin Help': ('06', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'Reserved Slots': ('07', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'Sound Commands': ('08', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'Player Commands': ('09', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'Admin Menu': ('10', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'Basic Votes': ('11', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'Client Preferences': ('12', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'Nextmap': ('13', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'SuperLogs: CSS': ('14', '1.2.4', 'psychonic'), 
           'Admin File Reader': ('15', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'Basic Comm Control': ('16', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'Basic Info Triggers': ('17', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'Anti-Flood': ('18', '1.5.0-dev+3635', 'AlliedModders LLC'), 
           'Fun Votes': ('19', '1.5.0-dev+3635', 'AlliedModders LLC')}, rv)


class Test_getClientOrCreate(CsgoTestCase):

    def test_new_client_with_cid_guid_name_team(self):
        self.assertEqual(2, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 2}, self.parser.storage.getCounts())
        client = self.parser.getClientOrCreate(cid='2', guid='AAAAAAAAAAAA000000000000000', name='theName', team='CT')
        self.assertIsInstance(client, Client)
        self.assertEqual('2', client.cid)
        self.assertEqual('AAAAAAAAAAAA000000000000000', client.guid)
        self.assertEqual('theName', client.name)
        self.assertEqual(TEAM_RED, client.team)
        self.assertTrue(client.authed)
        self.assertEqual(3, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 3}, self.parser.storage.getCounts())

    def test_new_client_with_cid_guid_name(self):
        self.assertEqual(2, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 2}, self.parser.storage.getCounts())
        client = self.parser.getClientOrCreate(cid='2', guid='AAAAAAAAAAAA000000000000000', name='theName')
        self.assertIsInstance(client, Client)
        self.assertEqual('2', client.cid)
        self.assertEqual('AAAAAAAAAAAA000000000000000', client.guid)
        self.assertEqual('theName', client.name)
        self.assertEqual(TEAM_UNKNOWN, client.team)
        self.assertTrue(client.authed)
        self.assertEqual(3, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 3}, self.parser.storage.getCounts())

    def test_connected_client_by_cid(self):
        self.parser.clients.newClient(cid='2', guid='AAAAAAAAAAAA000000000000000', name='theName', team=TEAM_BLUE)
        self.assertEqual(3, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 3}, self.parser.storage.getCounts())
        client = self.parser.getClientOrCreate(cid='2', guid=None, name=None)
        self.assertIsInstance(client, Client)
        self.assertEqual('2', client.cid)
        self.assertEqual('AAAAAAAAAAAA000000000000000', client.guid)
        self.assertEqual('theName', client.name)
        self.assertEqual(TEAM_BLUE, client.team)
        self.assertTrue(client.authed)
        self.assertEqual(3, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 3}, self.parser.storage.getCounts())
        return

    def test_connected_client_by_cid_different_name(self):
        self.parser.clients.newClient(cid='2', guid='AAAAAAAAAAAA000000000000000', name='theName', team=TEAM_BLUE)
        self.assertEqual(3, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 3}, self.parser.storage.getCounts())
        client = self.parser.getClientOrCreate(cid='2', guid=None, name='newName')
        self.assertIsInstance(client, Client)
        self.assertEqual('2', client.cid)
        self.assertEqual('AAAAAAAAAAAA000000000000000', client.guid)
        self.assertEqual('newName', client.name)
        self.assertEqual(TEAM_BLUE, client.team)
        self.assertTrue(client.authed)
        self.assertEqual(3, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 3}, self.parser.storage.getCounts())
        return

    def test_known_client_by_cid(self):
        known_client = Client(console=self.parser, guid='AAAAAAAAAAAA000000000000000', name='theName')
        known_client.save()
        self.assertEqual(2, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 3}, self.parser.storage.getCounts())
        client = self.parser.getClientOrCreate(cid='2', guid='AAAAAAAAAAAA000000000000000', name='newName', team='CT')
        self.assertIsInstance(client, Client)
        self.assertEqual(known_client.id, client.id)
        self.assertEqual('2', client.cid)
        self.assertEqual('AAAAAAAAAAAA000000000000000', client.guid)
        self.assertEqual('newName', client.name)
        self.assertEqual(TEAM_RED, client.team)
        self.assertTrue(client.authed)
        self.assertEqual(3, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 3}, self.parser.storage.getCounts())

    def test_changing_team(self):
        client = self.parser.getClientOrCreate(cid='2', guid='AAAAAAAAAAAA000000000000000', name='theName', team='CT')
        self.assertEqual(TEAM_RED, client.team)

        def assertTeam(excepted_team, new_team):
            self.parser.getClientOrCreate(cid='2', guid='AAAAAAAAAAAA000000000000000', name='theName', team=new_team)
            self.assertEqual(excepted_team, client.team)

        assertTeam(TEAM_RED, 'CT')
        assertTeam(TEAM_RED, None)
        assertTeam(TEAM_RED, '')
        assertTeam(TEAM_RED, 'f00')
        assertTeam(TEAM_RED, 'Unassigned')
        assertTeam(TEAM_BLUE, 'TERRORIST')
        return

    def test_disconnecting_switched_team_unassigned_does_not_reconnect_player(self):
        """
        When a player disconnects here's what we see in the log :
        L 07/19/2013 - 17:18:44: "f00<2008><STEAM_1:0:11111111><TERRORIST>" disconnected (reason "Disconnect by user.")
        L 07/19/2013 - 17:18:44: "f00<2008><STEAM_1:0:11111111>" switched from team <TERRORIST> to <Unassigned>

        When parsing the 2nd line, B3 MUST NOT recreate the client object
        """
        client = self.parser.getClient('194')
        self.assertEqual('courgette', client.name)
        self.assertListEqual(['courgette'], map(lambda x: x.name, self.parser.clients.getList()))
        self.parser.parseLine('L 07/19/2013 - 17:18:44: "courgette<194><STEAM_1:0:1111111><CT>" disconnected (reason "Disconnect by user.")')
        self.parser.parseLine('L 07/19/2013 - 17:18:44: "courgette<194><STEAM_1:0:1111111><CT>" switched from team <TERRORIST> to <Unassigned>')
        self.assertListEqual([], map(lambda x: x.name, self.parser.clients.getList()))


class Test_functional(CsgoTestCase):

    def test_banned_player_reconnects(self):
        player = FakeClient(self.parser, name='courgette', guid='STEAM_1:0:1111111')
        player.connects('2')
        self.assertEqual(0, player.numBans)
        player.ban(reason='test')
        self.assertEqual(1, player.numBans)
        player.disconnects()
        with patch.object(player, 'reBan') as (ban_mock):
            player.connects('3')
        self.assertTrue(ban_mock.called)

    def test_clantag_and_say_with_weird_line(self):
        """
        Sometimes (is it from CS:GO patch http://store.steampowered.com/news/8855/ released on 9/14/2012 ?) we got the following line :

        L 09/18/2012 - 18:26:21: "Spoon<3><STEAM_1:0:11111111><EHD Gaming>" triggered "clantag" (value "EHD")
        where we find the Clan name in place of the player team and the Clan tag in the 'value' property.

        It would have been better to have something like
        L 09/18/2012 - 18:26:21: "Spoon<3><STEAM_1:0:11111111><CT>" triggered "clantag" (value "EHD") (clanname "EHD Gaming")

        Also, after that, 'say' lines get affected in the same way :
        L 09/18/2012 - 18:26:35: "Spoon<3><STEAM_1:0:11111111><EHD Gaming>" say "!lt"
        In such case we need to make sure we are not loosing the correct team value
        """
        self.parser.parseLine('L 08/26/2012 - 03:22:36: "courgette<2><STEAM_1:0:1111111><>" connected, address "11.222.111.222:27005"')
        player = self.parser.getClient('2')
        self.assertEqual('STEAM_1:0:1111111', player.guid)
        self.assertFalse(hasattr(player, 'clantag'))
        self.parser.parseLine('L 08/26/2012 - 03:22:36: "courgette<2><STEAM_1:0:1111111><Unassigned>" joined team "CT"')
        self.assertEqual(TEAM_RED, player.team)
        self.parser.parseLine('L 08/26/2012 - 05:43:31: "courgette<2><STEAM_1:0:1111111><The Clan Name>" triggered "clantag" (value "TCN")')
        self.assertEqual('TCN', getattr(player, 'clantag', None))
        self.assertEqual(TEAM_RED, player.team)
        self.clear_events()
        self.parser.parseLine('L 08/26/2012 - 05:09:55: "courgette<2><STEAM_1:0:1111111><The Clan Name>" say "blah blah blah"')
        self.assert_has_event('EVT_CLIENT_SAY', 'blah blah blah', player)
        self.assertEqual(TEAM_RED, player.team)
        return