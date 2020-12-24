# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\core\parsers\test_arma2.py
# Compiled at: 2016-03-08 18:42:10
import unittest2 as unittest
from mock import Mock, patch, call
from mockito import when
from b3.fake import FakeClient
from b3.parsers.arma2 import Arma2Parser
from b3.config import XmlConfigParser

class Arma2TestCase(unittest.TestCase):
    """
    Test case that is suitable for testing Arma2 parser specific features
    """

    @classmethod
    def setUpClass(cls):
        from b3.parsers.battleye.abstractParser import AbstractParser
        from b3.fake import FakeConsole
        AbstractParser.__bases__ = (FakeConsole,)

    def tearDown(self):
        if hasattr(self, 'parser'):
            self.parser.working = False


class EventParsingTestCase(Arma2TestCase):

    def setUp(self):
        """ran before each test"""
        self.conf = XmlConfigParser()
        self.conf.loadFromString('\n                <configuration>\n                </configuration>\n            ')
        self.parser = Arma2Parser(self.conf)
        self.parser.output = Mock()
        self.evt_queue = []

        def queue_event(evt):
            self.evt_queue.append(evt)

        self.queueEvent_patcher = patch.object(self.parser, 'queueEvent', wraps=queue_event)
        self.queueEvent_mock = self.queueEvent_patcher.start()
        self.write_patcher = patch.object(self.parser, 'write')
        self.write_mock = self.write_patcher.start()
        self.parser.startup()

    def tearDown(self):
        """ran after each test to clean up"""
        Arma2TestCase.tearDown(self)
        self.queueEvent_patcher.stop()
        self.write_patcher.stop()
        if hasattr(self, 'parser'):
            self.parser.working = False

    def clear_events(self):
        """
        clear the event queue, so when assert_has_event is called, it will look only at the newly caught events.
        """
        self.evt_queue = []

    def assert_has_event(self, event_type, data=None, client=None, target=None):
        """
        assert that self.evt_queue contains at least one event for the given type that has the given characteristics.
        """
        if not isinstance(event_type, basestring):
            raise AssertionError

            def assert_event_equals(expected_event, actual_event):
                if expected_event is None:
                    self.assertIsNone(actual_event)
                self.assertEqual(expected_event.type, actual_event.type, 'expecting type %s, but got %s' % (
                 self.parser.getEventKey(expected_event.type), self.parser.getEventKey(actual_event.type)))
                self.assertEqual(expected_event.client, actual_event.client, 'expecting client %s, but got %s' % (expected_event.client, actual_event.client))
                self.assertEqual(expected_event.target, actual_event.target, 'expecting target %s, but got %s' % (expected_event.target, actual_event.target))
                self.assertEqual(expected_event.data, actual_event.data, 'expecting data %s, but got %s' % (expected_event.data, actual_event.data))
                return

            expected_event = self.parser.getEvent(event_type, data, client, target)
            len(self.evt_queue) or self.fail('expecting %s. Got no event instead' % expected_event)
        elif len(self.evt_queue) == 1:
            assert_event_equals(expected_event, self.evt_queue[0])
        else:
            for evt in self.evt_queue:
                try:
                    assert_event_equals(expected_event, evt)
                    return
                except Exception:
                    pass

            self.fail('expecting event %s. Got instead: %s' % (expected_event, map(str, self.evt_queue)))


class Test_game_events_parsing(EventParsingTestCase):

    def test_player_connected(self):
        self.clear_events()
        self.parser.routeBattleyeEvent('Player #0 Bravo17 (76.108.91.78:2304) connected')
        self.assertEqual(1, len(self.evt_queue))
        event = self.evt_queue[0]
        self.assertEqual(self.parser.getEventID('EVT_CLIENT_CONNECT'), event.type)
        self.assertEqual('Bravo17', event.client.name)
        self.assertEqual('0', event.client.cid)
        self.assertEqual('76.108.91.78', event.client.ip)

    def test_Verified_guid__with_connected_player(self):
        bravo17 = FakeClient(self.parser, name='Bravo17')
        bravo17.connects('0')
        self.clear_events()
        self.parser.routeBattleyeEvent('Verified GUID (80a5885ebe2420bab5e158a310fcbc7d) of player #0 Bravo17')
        self.assert_has_event('EVT_CLIENT_AUTH', data=bravo17, client=bravo17)

    def test_Verified_guid__with_unknown_player(self):
        self.clear_events()
        self.parser.routeBattleyeEvent('Verified GUID (80a5885ebe2420bab5e158a310fcbc7d) of player #0 Bravo17')
        self.assertTrue(len(self.evt_queue))
        event = self.evt_queue[0]
        self.assertEqual(self.parser.getEventID('EVT_CLIENT_CONNECT'), event.type)
        self.assertEqual('Bravo17', event.client.name)
        self.assertEqual('0', event.client.cid)
        bravo17 = event.client
        self.assert_has_event('EVT_CLIENT_AUTH', data=bravo17, client=bravo17)

    def test_player_disconnect(self):
        bravo17 = FakeClient(self.parser, name='Bravo17', guid='80a5885ebe2420bab5e158a310fcbc7d')
        bravo17.connects('12')
        self.clear_events()
        self.parser.routeBattleyeEvent('Player #12 Bravo17 disconnected')
        self.assert_has_event('EVT_CLIENT_DISCONNECT', client=bravo17, data='12')

    def test_Lobby_chat(self):
        bravo17 = FakeClient(self.parser, name='Bravo17', guid='80a5885ebe2420bab5e158a310fcbc7d')
        bravo17.connects('12')
        self.clear_events()
        self.parser.routeBattleyeEvent('(Lobby) Bravo17: hello b3')
        self.assert_has_event('EVT_CLIENT_SAY', client=bravo17, data='hello b3 (Lobby)')

    def test_Global_chat(self):
        bravo17 = FakeClient(self.parser, name='Bravo17', guid='80a5885ebe2420bab5e158a310fcbc7d')
        bravo17.connects('12')
        self.clear_events()
        self.parser.routeBattleyeEvent('(Global) Bravo17: global channel')
        self.assert_has_event('EVT_CLIENT_SAY', client=bravo17, data='global channel (Global)')

    def test_Direct_chat(self):
        bravo17 = FakeClient(self.parser, name='Bravo17', guid='80a5885ebe2420bab5e158a310fcbc7d')
        bravo17.connects('12')
        self.clear_events()
        self.parser.routeBattleyeEvent('(Direct) Bravo17: test direct channel')
        self.assert_has_event('EVT_CLIENT_SAY', client=bravo17, data='test direct channel (Direct)')

    def test_Vehicule_chat(self):
        bravo17 = FakeClient(self.parser, name='Bravo17', guid='80a5885ebe2420bab5e158a310fcbc7d')
        bravo17.connects('12')
        self.clear_events()
        self.parser.routeBattleyeEvent('(Vehicle) Bravo17: test vehicle channel')
        self.assert_has_event('EVT_CLIENT_SAY', client=bravo17, data='test vehicle channel (Vehicle)')

    def test_Group_chat(self):
        bravo17 = FakeClient(self.parser, name='Bravo17', guid='80a5885ebe2420bab5e158a310fcbc7d')
        bravo17.connects('12')
        self.clear_events()
        self.parser.routeBattleyeEvent('(Group) Bravo17: test group channel')
        self.assert_has_event('EVT_CLIENT_SAY', client=bravo17, data='test group channel (Group)')

    def test_Side_chat(self):
        bravo17 = FakeClient(self.parser, name='Bravo17', guid='80a5885ebe2420bab5e158a310fcbc7d')
        bravo17.connects('12')
        self.clear_events()
        self.parser.routeBattleyeEvent('(Side) Bravo17: test side channel')
        self.assert_has_event('EVT_CLIENT_SAY', client=bravo17, data='test side channel (Side)')

    def test_Command_chat(self):
        bravo17 = FakeClient(self.parser, name='Bravo17', guid='80a5885ebe2420bab5e158a310fcbc7d')
        bravo17.connects('12')
        self.clear_events()
        self.parser.routeBattleyeEvent('(Command) Bravo17: test command channel')
        self.assert_has_event('EVT_CLIENT_SAY', client=bravo17, data='test command channel (Command)')


class Test_utf8_issues(EventParsingTestCase):

    def test_player_connected_utf8(self):
        self.clear_events()
        self.parser.routeBattleyeEvent('Player #0 F00Åéxx (11.1.1.8:2304) connected')
        self.assertEqual(1, len(self.evt_queue))
        event = self.evt_queue[0]
        self.assertEqual(self.parser.getEventID('EVT_CLIENT_CONNECT'), event.type)
        self.assertEqual('F00Åéxx', event.client.name)

    def test_player_connected_utf8_2(self):
        self.clear_events()
        self.parser.routeBattleyeEvent('Player #1 étoiléàtèsté (77.205.193.131:2304) connected')
        self.assertEqual(1, len(self.evt_queue))
        event = self.evt_queue[0]
        self.assertEqual(self.parser.getEventID('EVT_CLIENT_CONNECT'), event.type)
        self.assertEqual('étoiléàtèsté', event.client.name)

    def test_verified_guid(self):
        self.clear_events()
        self.parser.routeBattleyeEvent('Verified GUID (a4c3eba0a790300fd7d9d39e26e00eb0) of player #1 étoiléàtèsté')
        self.assertTrue(len(self.evt_queue))
        event = self.evt_queue[0]
        self.assertEqual(self.parser.getEventID('EVT_CLIENT_CONNECT'), event.type)
        self.assertEqual('étoiléàtèsté', event.client.name)


@patch('time.sleep')
class Test_parser_API(Arma2TestCase):

    def setUp(self):
        self.conf = XmlConfigParser()
        self.conf.loadFromString('<configuration></configuration>')
        self.parser = Arma2Parser(self.conf)
        self.parser.output = Mock()
        self.parser.sayqueue.put = Mock(side_effect=self.parser._say)
        self.parser.startup()
        self.player = self.parser.clients.newClient(cid='4', guid='theGuid', name='theName', ip='11.22.33.44')

    def test_getPlayerList(self, sleep_mock):
        when(self.parser.output).write('players').thenReturn('Players on server:\n[#] [IP Address]:[Port] [Ping] [GUID] [Name]\n--------------------------------------------------\n0   11.111.11.11:2304     63   80a5885eb00000000000000000000000(OK) étoiléàÄ\n0   192.168.0.100:2316    0    80a5885eb00000000000000000000000(OK) étoiléàÄ (Lobby)\n(1 players in total)\n')
        players = self.parser.getPlayerList()
        self.maxDiff = 1024
        self.assertDictEqual({'0': {'cid': '0', 'guid': '80a5885eb00000000000000000000000', 
                 'ip': '192.168.0.100', 
                 'lobby': True, 
                 'name': 'étoiléàÄ', 
                 'ping': '0', 
                 'port': '2316', 
                 'verified': 'OK'}}, players)

    def test_say(self, sleep_mock):
        self.parser.msgPrefix = '[Pre]'
        self.parser.say('f00')
        self.parser.output.write.assert_has_calls([call('say -1 [Pre] f00')])

    def test_saybig(self, sleep_mock):
        self.parser.msgPrefix = '[Pre]'
        self.parser.saybig('f00')
        self.parser.output.write.assert_has_calls([call('say -1 [Pre] f00')])

    def test_message(self, sleep_mock):
        self.parser.msgPrefix = '[Pre]'
        self.parser.message(self.player, 'f00')
        self.parser.output.write.assert_has_calls([call('say 4 [Pre] f00')])

    def test_kick(self, sleep_mock):
        self.parser.kick(self.player, reason='f00')
        self.parser.output.write.assert_has_calls([call('kick 4 f00')])

    def test_ban__by_cid(self, sleep_mock):
        self.assertIsNotNone(self.player.cid)
        self.parser.ban(self.player, reason='f00')
        self.parser.output.write.assert_has_calls([call('ban 4 0 f00'), call('writeBans')])

    def test_ban__by_guid(self, sleep_mock):
        self.player.cid = None
        self.assertIsNone(self.player.cid)
        self.parser.ban(self.player, reason='f00')
        self.parser.output.write.assert_has_calls([call('addBan theGuid 0 f00'), call('writeBans')])
        return

    def test_unban(self, sleep_mock):
        self.player.cid = None
        self.assertIsNone(self.player.cid)
        when(self.parser).getBanlist().thenReturn({'theGuid': {'ban_index': '152', 'guid': 'theGuid', 'reason': 'the ban reason', 'min_left': 'perm'}})
        self.parser.unban(self.player, reason='f00')
        self.parser.output.write.assert_has_calls([call('removeBan 152'), call('writeBans')])
        return

    def test_tempban__by_cid(self, sleep_mock):
        self.assertIsNotNone(self.player.cid)
        self.parser.tempban(self.player, reason='f00', duration='2h')
        self.parser.output.write.assert_has_calls([call('ban 4 120 f00'),
         call('writeBans')])

    def test_tempban__by_guid(self, sleep_mock):
        self.player.cid = None
        self.assertIsNone(self.player.cid)
        self.parser.tempban(self.player, reason='f00', duration='2h')
        self.parser.output.write.assert_has_calls([call('addBan theGuid 120 f00'),
         call('writeBans')])
        return

    def test_getPlayerPings(self, sleep_mock):
        when(self.parser.output).write('players').thenReturn('Players on server:\n[#] [IP Address]:[Port] [Ping] [GUID] [Name]\n--------------------------------------------------\n0   76.108.91.78:2304     63   80a5885ebe2420bab5e158a310fcbc7d(OK) Bravo17\n0   192.168.0.100:2316    0    80a5885ebe2420bab5e158a310fcbc7d(OK) Bravo17 (Lobby)\n2   111.22.3.4:2316       47   80a50000000000000000000000fcbc7d(?)  bob\n(1 players in total)\n')
        pings = self.parser.getPlayerPings()
        self.maxDiff = 1024
        self.assertDictEqual({'0': 63, '2': 47}, pings)


class test_sync(EventParsingTestCase):

    def test_known_client_with_unverified_guid_but_same_ip_is_auth(self):
        bob = FakeClient(self.parser, name='bob', guid='80a50000000000000000000000fcbc7d', ip='111.22.3.4')
        bob.save()
        when(self.parser.output).write('players').thenReturn('Players on server:\n[#] [IP Address]:[Port] [Ping] [GUID] [Name]\n--------------------------------------------------\n2   111.22.3.4:2316       47   80a50000000000000000000000fcbc7d(?)  bob\n(1 players in total)\n')
        rv = self.parser.sync()
        self.assertIn('2', rv)
        client = rv['2']
        self.assertEqual(bob.guid, client.guid)
        self.assertEqual(bob.ip, client.ip)
        self.assertTrue(client.authed)

    def test_known_client_with_unverified_guid_and_different_ip_is_not_auth(self):
        bob = FakeClient(self.parser, name='bob', guid='80a50000000000000000000000fcbc7d', ip='1.2.3.4')
        bob.save()
        when(self.parser.output).write('players').thenReturn('Players on server:\n[#] [IP Address]:[Port] [Ping] [GUID] [Name]\n--------------------------------------------------\n2   4.6.8.10:2316       47   80a50000000000000000000000fcbc7d(?)  bob\n(1 players in total)\n')
        rv = self.parser.sync()
        self.assertIn('2', rv)
        client = rv['2']
        self.assertEqual('bob', client.name)
        self.assertEqual('4.6.8.10', client.ip)
        self.assertEqual('', client.guid)
        self.assertFalse(client.authed)

    def test_unknown_client_with_unverified_guid(self):
        when(self.parser.output).write('players').thenReturn('Players on server:\n[#] [IP Address]:[Port] [Ping] [GUID] [Name]\n--------------------------------------------------\n2   4.6.8.10:2316       47   80a50000000000000000000000fcbc7d(?)  bob\n(1 players in total)\n')
        rv = self.parser.sync()
        self.assertIn('2', rv)
        client = rv['2']
        self.assertEqual('bob', client.name)
        self.assertEqual('4.6.8.10', client.ip)
        self.assertEqual('', client.guid)
        self.assertFalse(client.authed)

    def test_unknown_client_with_verified_guid(self):
        when(self.parser.output).write('players').thenReturn('Players on server:\n[#] [IP Address]:[Port] [Ping] [GUID] [Name]\n--------------------------------------------------\n2   4.6.8.10:2316       47   80a50000000000000000000000fcbc7d(OK)  bob\n(1 players in total)\n')
        rv = self.parser.sync()
        self.assertIn('2', rv)
        client = rv['2']
        self.assertEqual('bob', client.name)
        self.assertEqual('4.6.8.10', client.ip)
        self.assertEqual('80a50000000000000000000000fcbc7d', client.guid)
        self.assertTrue(client.authed)


class test_others(Arma2TestCase):

    def setUp(self):
        self.conf = XmlConfigParser()
        self.conf.loadFromString('<configuration></configuration>')
        self.parser = Arma2Parser(self.conf)
        self.parser.output = Mock()
        self.parser.startup()
        self.player = self.parser.clients.newClient(cid='4', guid='theGuid', name='theName', ip='11.22.33.44')

    def test_getBanlist(self):
        self.maxDiff = 1024
        when(self.parser.output).write('bans').thenReturn('GUID Bans:\n[#] [GUID] [Minutes left] [Reason]\n----------------------------------------\n0  b57c222222a76f458893641000000005 perm Script Detection: Gerk\n1  8ac61111111cd2ff4235140000000026 perm Script Detection: setVehicleInit DoThis;')
        rv = self.parser.getBanlist()
        self.assertDictEqual({'b57c222222a76f458893641000000005': {'ban_index': '0', 'guid': 'b57c222222a76f458893641000000005', 'reason': 'Script Detection: Gerk', 'min_left': 'perm'}, '8ac61111111cd2ff4235140000000026': {'ban_index': '1', 'guid': '8ac61111111cd2ff4235140000000026', 'reason': 'Script Detection: setVehicleInit DoThis;', 'min_left': 'perm'}}, rv)