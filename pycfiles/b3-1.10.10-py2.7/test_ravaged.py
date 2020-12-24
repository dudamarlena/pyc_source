# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\core\parsers\test_ravaged.py
# Compiled at: 2016-03-08 18:42:10
import os
from mock import Mock, call, patch
import unittest2 as unittest
from mockito import when
from b3 import TEAM_UNKNOWN
from b3.clients import Client
from b3.config import XmlConfigParser, CfgConfigParser
from b3.fake import FakeClient
from b3.parsers.ravaged import RavagedParser, TEAM_SCAVENGERS, TEAM_RESISTANCE
from b3.plugins.admin import AdminPlugin
from b3 import __file__ as b3_module__file__
ADMIN_CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(b3_module__file__), 'conf/plugin_admin.ini'))
ADMIN_CONFIG = None

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


class RavagedTestCase(unittest.TestCase):
    """
    Test case that is suitable for testing Ravaged parser specific features
    """
    whatever = object()

    @classmethod
    def setUpClass(cls):
        from b3.fake import FakeConsole
        RavagedParser.__bases__ = (FakeConsole,)

    def setUp(self):
        self.status_response = None
        self.conf = XmlConfigParser()
        self.conf.loadFromString('<configuration></configuration>')
        self.parser = RavagedParser(self.conf)
        self.parser.output = Mock()
        self.parser.output.write = Mock()
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

    def assert_has_event(self, event_type, data=None, client=None, target=None):
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
            if data != self.whatever:
                self.assertEqual(expected_event.data, actual_event.data)
            if client != self.whatever:
                self.assertTrue(client_equal(expected_event.client, actual_event.client))
            if target != self.whatever:
                self.assertTrue(client_equal(expected_event.target, actual_event.target))
        else:
            for evt in [ e for e in self.evt_queue if e.type == expected_event.type ]:
                results = [
                 expected_event.type == evt.type]
                if data != self.whatever:
                    results.append(expected_event.data == evt.data)
                if client != self.whatever:
                    results.append(client_equal(expected_event.client, evt.client))
                if target != self.whatever:
                    results.append(client_equal(expected_event.target, evt.target))
                if all(results):
                    return

            self.fail('expecting event %s. Got instead: %s' % (expected_event, map(str, self.evt_queue)))


class Test_parser_API(RavagedTestCase):

    def test_say(self):
        self.parser.msgPrefix = '[Pre]'
        with patch.object(self.parser.output, 'write') as (write_mock):
            self.parser.say('Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
            write_mock.assert_has_calls([call("say <FONT COLOR='#F2C880'> [Pre] <FONT COLOR='#F2C880'> Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,"),
             call("say <FONT COLOR='#F2C880'> >quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla"),
             call("say <FONT COLOR='#F2C880'> >pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")])

    def test_saybig(self):
        self.parser.msgPrefix = '[Pre]'
        with patch.object(self.parser.output, 'write') as (write_mock):
            self.parser.saybig('Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.')
            write_mock.assert_has_calls([call("say <FONT COLOR='#FC00E2'> [Pre] <FONT COLOR='#FC00E2'> Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore"),
             call("say <FONT COLOR='#FC00E2'> >veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos"),
             call("say <FONT COLOR='#FC00E2'> >qui ratione voluptatem sequi nesciunt.")])

    def test_message(self):
        self.parser.msgPrefix = '[Pre]'
        with patch.object(self.parser.output, 'write') as (write_mock):
            self.parser.saybig('At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa')
            write_mock.assert_has_calls([call("say <FONT COLOR='#FC00E2'> [Pre] <FONT COLOR='#FC00E2'> At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias"),
             call("say <FONT COLOR='#FC00E2'> >excepturi sint occaecati cupiditate non provident, similique sunt in culpa")])

    def test_getMap(self):
        when(self.parser.output).write('getmaplist false').thenReturn('0 CTR_Canyon\n1 CTR_Derelict\n2 CTR_IceBreaker\n3 CTR_Liberty\n')
        rv = self.parser.getMap()
        self.assertEqual('CTR_Canyon', rv)

    def test_getNextMap(self):
        when(self.parser.output).write('getmaplist false').thenReturn('0 CTR_Canyon\n1 CTR_Derelict\n2 CTR_IceBreaker\n3 CTR_Liberty\n')
        rv = self.parser.getNextMap()
        self.assertEqual('CTR_Derelict', rv)

    def test_changeMap(self):
        when(self.parser.output).write('getmaplist false').thenReturn('0 CTR_Bridge\n1 CTR_Canyon\n2 CTR_Derelict\n3 CTR_IceBreaker\n4 CTR_Liberty\n5 CTR_Rooftop\n6 Thrust_Bridge\n7 Thrust_Canyon\n8 Thrust_Chasm\n9 Thrust_IceBreaker\n10 Thrust_Liberty\n11 Thrust_Oilrig\n12 Thrust_Rooftop\n')
        with patch.object(self.parser.output, 'write', wraps=self.parser.output.write) as (write_mock):
            rv = self.parser.changeMap('oil')
        write_mock.assert_has_calls([call('addmap Thrust_Oilrig 1'), call('nextmap')])

    def test_getPlayerPings(self):
        when(self.parser.output).write('getplayerlist').thenReturn('1 players:\ncourgette 21 pts 4:8 38ms steamid: 12312312312312312\n')
        rv = self.parser.getPlayerPings()
        self.assertDictEqual({'12312312312312312': 38}, rv)

    def test_getPlayerScores(self):
        when(self.parser.output).write('getplayerlist').thenReturn('1 players:\ncourgette 21 pts 4:8 38ms steamid: 12312312312312312\n')
        rv = self.parser.getPlayerScores()
        self.assertDictEqual({'12312312312312312': 21}, rv)


class Test_gamelog_parsing(RavagedTestCase):

    def test_unknown_line(self):
        self.queueEvent_mock.reset_mock()
        with patch.object(self.parser, 'warning') as (warning_mock):
            self.parser.route_game_event('f00 f00 f00')
        self.assertFalse(self.queueEvent_mock.called)
        warning_mock.assert_has_calls([call('unhandled log line : f00 f00 f00 : please report this on the B3 forums')])

    def test_connected(self):
        p = Client(cid='12312312312312312', guid='12312312312312312', ip='192.168.0.1')
        self.queueEvent_mock.reset_mock()
        self.parser.route_game_event('"<12312312312312312><>" connected, address "192.168.0.1"')
        self.assert_has_event('EVT_CLIENT_CONNECT', data=self.whatever, client=p)

    def test_disconnected(self):
        p = Client(cid='12312312312312312', guid='12312312312312312', name='courgette')
        self.queueEvent_mock.reset_mock()
        self.parser.route_game_event('"courgette<12312312312312312><0>"disconnected')
        self.assert_has_event('EVT_CLIENT_DISCONNECT', data='12312312312312312', client=p)

    def test_entered_the_game(self):
        p = Client(cid='12312312312312312', guid='12312312312312312', name='courgette')
        self.queueEvent_mock.reset_mock()
        self.parser.route_game_event('"courgette<12312312312312312><0>" entered the game')
        self.assert_has_event('EVT_CLIENT_JOIN', client=p)

    def test_joined_team(self):
        p = Client(cid='12312312312312312', guid='12312312312312312', name='courgette')
        self.queueEvent_mock.reset_mock()
        self.parser.route_game_event('"courgette<12312312312312312><1>" joined team "1"')
        self.assert_has_event('EVT_CLIENT_TEAM_CHANGE', data=TEAM_RESISTANCE, client=p)

    def test_Server_say(self):
        self.queueEvent_mock.reset_mock()
        self.parser.route_game_event(b'Server say "Admin: B\xb3: www.bigbrotherbot.net (b3) v1.10dev [nt] [Coco] [ONLINE]"')
        self.assertFalse(self.queueEvent_mock.called)

    def test_Server_say_team(self):
        self.queueEvent_mock.reset_mock()
        self.parser.route_game_event('Server say_team "f00" to team "1"')
        self.assertFalse(self.queueEvent_mock.called)

    def test_loading_map(self):
        self.parser.game.mapName = 'F00'
        self.queueEvent_mock.reset_mock()
        self.parser.route_game_event('Loading map "CTR_Derelict"')
        self.assert_has_event('EVT_GAME_MAP_CHANGE', data={'old': 'F00', 'new': 'CTR_Derelict'})

    def test_round_started(self):
        self.parser.game.mapName = 'F00'
        self.queueEvent_mock.reset_mock()
        self.parser.route_game_event('Round started')
        self.assert_has_event('EVT_GAME_ROUND_START', data=self.parser.game)

    def test_round_finished(self):
        self.queueEvent_mock.reset_mock()
        self.parser.route_game_event('Round finished, winning team is "0"')
        self.assert_has_event('EVT_GAME_ROUND_END', data=TEAM_SCAVENGERS)

    def test_say(self):
        p = Client(cid='12312312312312312', guid='12312312312312312', name='courgette')
        self.queueEvent_mock.reset_mock()
        self.parser.route_game_event('"courgette<12312312312312312><1>" say "<FONT COLOR=\'#FF0000\'> hi"')
        self.assert_has_event('EVT_CLIENT_SAY', data='hi', client=p)

    def test_say_team(self):
        p = Client(cid='12312312312312312', guid='12312312312312312', name='courgette')
        self.queueEvent_mock.reset_mock()
        self.parser.route_game_event('"courgette<12312312312312312><1>" say_team "(Team) <FONT COLOR=\'#66CCFF\'> hi team"')
        self.assert_has_event('EVT_CLIENT_TEAM_SAY', data='hi team', client=p)

    def test_committed_suicide(self):
        p = Client(cid='12312312312312312', guid='12312312312312312', name='courgette')
        self.queueEvent_mock.reset_mock()
        self.parser.route_game_event('"courgette<12312312312312312><1>" committed suicide with "R_DmgType_M26Grenade"')
        self.assert_has_event('EVT_CLIENT_SUICIDE', data=(100, 'R_DmgType_M26Grenade',
                                                          'body'), client=p, target=p)

    def test_kill_enemy(self):
        p1 = FakeClient(self.parser, guid='11111111111111')
        p1.connects('11111111111111')
        p2 = FakeClient(self.parser, guid='2222222222222')
        p2.connects('2222222222222')
        self.queueEvent_mock.reset_mock()
        self.clear_events()
        self.parser.route_game_event('"Name1<11111111111111><0>" killed "Name2<2222222222222><1>" with "the_weapon"')
        self.assert_has_event('EVT_CLIENT_KILL', data=(100, 'the_weapon', 'body'), client=p1, target=p2)

    def test_kill_enemy_2(self):
        p1 = FakeClient(self.parser, guid='76561000000000000')
        p1.connects('76561000000000000')
        p2 = FakeClient(self.parser, guid='70000000000000005')
        p2.connects('70000000000000005')
        self.queueEvent_mock.reset_mock()
        self.clear_events()
        self.parser.route_game_event('"txsniper<76561000000000000><1>" killed "Killer Badger<70000000000000005><0>" with R_DmgType_SniperPrimary')
        self.assert_has_event('EVT_CLIENT_KILL', data=(100, 'R_DmgType_SniperPrimary',
                                                       'body'), client=p1, target=p2)

    def test_kill_teammate(self):
        p1 = FakeClient(self.parser, guid='11111111111111')
        p1.connects('11111111111111')
        p2 = FakeClient(self.parser, guid='2222222222222')
        p2.connects('2222222222222')
        self.queueEvent_mock.reset_mock()
        self.clear_events()
        self.parser.route_game_event('"Name1<11111111111111><0>" killed "Name2<2222222222222><0>" with "the_weapon"')
        self.assert_has_event('EVT_CLIENT_KILL_TEAM', data=(100, 'the_weapon', 'body'), client=p1, target=p2)

    def test_killed(self):
        p1 = FakeClient(self.parser, guid='11111111111111')
        p1.connects('11111111111111')
        self.queueEvent_mock.reset_mock()
        self.clear_events()
        self.parser.route_game_event('"Name1<11111111111111><0>" killed  with UTDmgType_VehicleCollision')
        self.assert_has_event('EVT_CLIENT_SUICIDE', data=(100, 'UTDmgType_VehicleCollision',
                                                          'body'), client=p1, target=p1)

    def test_connected_remotely(self):
        self.queueEvent_mock.reset_mock()
        self.parser.route_game_event('(127.0.0.1:3508 has connected remotely)')
        self.assertFalse(self.queueEvent_mock.called)

    def test_connected_remotely2(self):
        self.queueEvent_mock.reset_mock()
        self.parser.route_game_event('RCon:(Admin127.0.0.1:3508 has disconnected from RCon)')
        self.assertFalse(self.queueEvent_mock.called)


class Test_getClientOrCreate(RavagedTestCase):

    def test_new_client__guid_name_team(self):
        self.assertEqual(1, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 1}, self.parser.storage.getCounts())
        client = self.parser.getClientOrCreate(guid='12312312312312312', name='courgette', team='1')
        self.assertIsInstance(client, Client)
        self.assertEqual('12312312312312312', client.cid)
        self.assertEqual('12312312312312312', client.guid)
        self.assertEqual('courgette', client.name)
        self.assertEqual(TEAM_RESISTANCE, client.team)
        self.assertTrue(client.authed)
        self.assertEqual(2, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 2}, self.parser.storage.getCounts())

    def test_new_client__guid_name(self):
        self.assertEqual(1, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 1}, self.parser.storage.getCounts())
        client = self.parser.getClientOrCreate(guid='12312312312312312', name='courgette')
        self.assertIsInstance(client, Client)
        self.assertEqual('12312312312312312', client.cid)
        self.assertEqual('12312312312312312', client.guid)
        self.assertEqual('courgette', client.name)
        self.assertEqual(TEAM_UNKNOWN, client.team)
        self.assertTrue(client.authed)
        self.assertEqual(2, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 2}, self.parser.storage.getCounts())

    def test_connected_client__guid(self):
        self.parser.clients.newClient(cid='12312312312312312', guid='12312312312312312', name='courgette', team=TEAM_SCAVENGERS)
        self.assertEqual(2, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 2}, self.parser.storage.getCounts())
        client = self.parser.getClientOrCreate(guid='12312312312312312', name=None)
        self.assertIsInstance(client, Client)
        self.assertEqual('12312312312312312', client.cid)
        self.assertEqual('12312312312312312', client.guid)
        self.assertEqual('courgette', client.name)
        self.assertEqual(TEAM_SCAVENGERS, client.team)
        self.assertTrue(client.authed)
        self.assertEqual(2, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 2}, self.parser.storage.getCounts())
        return

    def test_connected_client__guid_different_name(self):
        self.parser.clients.newClient(cid='12312312312312312', guid='12312312312312312', name='courgette', team=TEAM_SCAVENGERS)
        self.assertEqual(2, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 2}, self.parser.storage.getCounts())
        client = self.parser.getClientOrCreate(guid='12312312312312312', name='F00')
        self.assertIsInstance(client, Client)
        self.assertEqual('12312312312312312', client.cid)
        self.assertEqual('12312312312312312', client.guid)
        self.assertEqual('F00', client.name)
        self.assertEqual(TEAM_SCAVENGERS, client.team)
        self.assertTrue(client.authed)
        self.assertEqual(2, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 2}, self.parser.storage.getCounts())

    def test_known_client__guid(self):
        known_client = Client(console=self.parser, guid='12312312312312312', name='courgette', connections=15)
        known_client.save()
        self.assertEqual(1, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 2}, self.parser.storage.getCounts())
        client = self.parser.getClientOrCreate(guid='12312312312312312', name='newName', team='0')
        self.assertIsInstance(client, Client)
        self.assertEqual(known_client.id, client.id)
        self.assertEqual('12312312312312312', client.cid)
        self.assertEqual('12312312312312312', client.guid)
        self.assertEqual('newName', client.name)
        self.assertEqual(TEAM_SCAVENGERS, client.team)
        self.assertEqual(16, client.connections)
        self.assertTrue(client.authed)
        self.assertEqual(2, len(self.parser.clients))
        self.assertDictContainsSubset({'clients': 2}, self.parser.storage.getCounts())


class Test_other(RavagedTestCase):

    def test_getTeam(self):
        self.assertEqual(TEAM_SCAVENGERS, self.parser.getTeam('0'))
        self.assertEqual(TEAM_RESISTANCE, self.parser.getTeam('1'))
        self.assertEqual(TEAM_UNKNOWN, self.parser.getTeam('3'))
        self.assertEqual(TEAM_UNKNOWN, self.parser.getTeam(''))
        self.assertEqual(TEAM_UNKNOWN, self.parser.getTeam('-1'))

    def test_getmaplist(self):
        when(self.parser.output).write('getmaplist false').thenReturn('0 CTR_Canyon\n1 CTR_Derelict\n2 CTR_IceBreaker\n3 CTR_Liberty\n4 CTR_Rooftop\n5 Thrust_Bridge\n6 Thrust_Canyon\n7 Thrust_Chasm\n8 Thrust_IceBreaker\n9 Thrust_Liberty\n10 Thrust_Oilrig\n11 Thrust_Rooftop\n12 CTR_Bridge\n')
        rv = self.parser.getmaplist()
        self.assertListEqual(['CTR_Canyon',
         'CTR_Derelict',
         'CTR_IceBreaker',
         'CTR_Liberty',
         'CTR_Rooftop',
         'Thrust_Bridge',
         'Thrust_Canyon',
         'Thrust_Chasm',
         'Thrust_IceBreaker',
         'Thrust_Liberty',
         'Thrust_Oilrig',
         'Thrust_Rooftop',
         'CTR_Bridge'], rv)

    def test_getplayerlist(self):
        courgette = Client(console=self.parser, cid='12312312312312312', guid='12312312312312312', name='courgette')
        self.parser.clients['12312312312312312'] = courgette
        when(self.parser.output).write('getplayerlist').thenReturn('1 players:\ncourgette 21 pts 4:8 38ms steamid: 12312312312312312\n')
        rv = self.parser.getplayerlist()
        self.assertDictEqual({'12312312312312312': courgette}, rv)
        self.assertEqual(21, courgette.score)
        self.assertEqual(4, courgette.kills)
        self.assertEqual(8, courgette.deaths)
        self.assertEqual(38, courgette.ping)

    def test_getMapsSoundingLike_matching(self):
        when(self.parser.output).write('getmaplist false').thenReturn('0 CTR_Bridge\n1 CTR_Canyon\n2 CTR_Derelict\n3 CTR_IceBreaker\n4 CTR_Liberty\n5 CTR_Rooftop\n6 Thrust_Bridge\n7 Thrust_Canyon\n8 Thrust_Chasm\n9 Thrust_IceBreaker\n10 Thrust_Liberty\n11 Thrust_Oilrig\n12 Thrust_Rooftop\n')
        rv = self.parser.getMapsSoundingLike('oil')
        self.assertEqual('Thrust_Oilrig', rv)

    def test_getMapsSoundingLike_no_match(self):
        when(self.parser.output).write('getmaplist false').thenReturn('0 CTR_Bridge\n1 CTR_Canyon\n2 CTR_Derelict\n3 CTR_IceBreaker\n4 CTR_Liberty\n5 CTR_Rooftop\n6 Thrust_Bridge\n7 Thrust_Canyon\n8 Thrust_Chasm\n9 Thrust_IceBreaker\n10 Thrust_Liberty\n11 Thrust_Oilrig\n12 Thrust_Rooftop\n')
        rv = self.parser.getMapsSoundingLike('Canyon')
        self.assertSetEqual(set(['Thrust_Canyon', 'CTR_Canyon']), set(rv))

    def test_getMapsSoundingLike_3(self):
        when(self.parser.output).write('getmaplist false').thenReturn('0 CTR_Bridge\n1 CTR_Canyon\n2 CTR_Derelict\n3 CTR_IceBreaker\n4 CTR_Liberty\n5 CTR_Rooftop\n6 Thrust_Bridge\n7 Thrust_Canyon\n8 Thrust_Chasm\n9 Thrust_IceBreaker\n10 Thrust_Liberty\n11 Thrust_Oilrig\n12 Thrust_Rooftop\n')
        rv = self.parser.getMapsSoundingLike('CTR canyon')
        self.assertEqual('CTR_Canyon', rv)


class test_functional(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from b3.fake import FakeConsole
        RavagedParser.__bases__ = (FakeConsole,)

    def setUp(self):
        self.status_response = None
        self.conf = XmlConfigParser()
        self.conf.loadFromString('<configuration></configuration>')
        self.parser = RavagedParser(self.conf)
        self.parser.output = Mock()
        self.parser.output.write = Mock()
        ADMIN_CONFIG = CfgConfigParser()
        ADMIN_CONFIG.load(ADMIN_CONFIG_FILE)
        self.adminPlugin = AdminPlugin(self.parser, ADMIN_CONFIG)
        when(self.parser).getPlugin('admin').thenReturn(self.adminPlugin)
        self.adminPlugin.onLoadConfig()
        self.adminPlugin.onStartup()
        self.parser.startup()
        return

    def tearDown(self):
        if hasattr(self, 'parser'):
            del self.parser.clients
            self.parser.working = False

    def test_map(self):
        when(self.parser.output).write('getmaplist false').thenReturn(('0 CTR_Bridge\n1 CTR_Canyon\n2 CTR_Derelict\n3 CTR_IceBreaker\n4 CTR_Liberty\n5 CTR_Rooftop\n6 Thrust_Bridge\n7 Thrust_Canyon\n8 Thrust_Chasm\n9 Thrust_IceBreaker\n10 Thrust_Liberty\n11 Thrust_Oilrig\n12 Thrust_Rooftop\n').encode('UTF-8'))
        admin = FakeClient(console=self.parser, name='admin', guid='guid_admin', groupBits=128)
        admin.connects('guid_admin')
        with patch.object(self.parser.output, 'write', wraps=self.parser.output.write) as (write_mock):
            admin.says('!map chasm')
        write_mock.assert_has_calls([call('addmap Thrust_Chasm 1'), call('nextmap')])