# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\core\parsers\test_arma3.py
# Compiled at: 2016-03-08 18:42:10
import logging, unittest2 as unittest
from mock import Mock, patch
from mockito import when
from b3.clients import Client
from b3.parsers.arma3 import Arma3Parser
from b3.config import XmlConfigParser
from tests import logging_disabled
ANY = object()

class Arma3TestCase(unittest.TestCase):
    """
    Test case that is suitable for testing Arma3 parser specific features
    """

    @classmethod
    def setUpClass(cls):
        from b3.parsers.battleye.abstractParser import AbstractParser
        from b3.fake import FakeConsole
        AbstractParser.__bases__ = (FakeConsole,)
        logging.getLogger('output').setLevel(logging.DEBUG)

    def tearDown(self):
        if hasattr(self, 'parser'):
            self.parser.working = False


class EventParsingTestCase(Arma3TestCase):

    def setUp(self):
        """ran before each test"""
        self.conf = XmlConfigParser()
        self.conf.loadFromString('\n                <configuration>\n                </configuration>\n            ')
        with logging_disabled():
            self.parser = Arma3Parser(self.conf)
        self.parser.output = Mock()
        self.evt_queue = []

        def queue_event(evt):
            self.evt_queue.append(evt)

        self.queueEvent_patcher = patch.object(self.parser, 'queueEvent', wraps=queue_event)
        self.queueEvent_mock = self.queueEvent_patcher.start()
        self.write_patcher = patch.object(self.parser, 'write')
        self.write_mock = self.write_patcher.start()
        with logging_disabled():
            self.parser.startup()

    def tearDown(self):
        """ran after each test to clean up"""
        Arma3TestCase.tearDown(self)
        self.queueEvent_patcher.stop()
        self.write_patcher.stop()
        if hasattr(self, 'parser'):
            self.parser.working = False

    def clear_events(self):
        """
        clear the event queue, so when assert_has_event is called, it will look only at the newly caught events.
        """
        self.evt_queue = []

    def assert_has_event(self, event_type, data=ANY, client=ANY, target=ANY):
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
                if client is not ANY:
                    self.assertEqual(expected_event.client, actual_event.client, 'expecting client %s, but got %s' % (expected_event.client, actual_event.client))
                if target is not ANY:
                    self.assertEqual(expected_event.target, actual_event.target, 'expecting target %s, but got %s' % (expected_event.target, actual_event.target))
                if data is not ANY:
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
                except AssertionError:
                    pass

            self.fail('expecting event %s. Got instead: %s' % (expected_event, map(str, self.evt_queue)))


class Test_game_events_parsing(EventParsingTestCase):

    def setUp(self):
        EventParsingTestCase.setUp(self)

    def test_player_connecting_with_unverified_guid_at_first(self):
        self.clear_events()
        self.parser.routeBattleyeEvent('Player #8 Max (111.222.200.50:2304) connected')
        self.parser.routeBattleyeEvent('Player #8 Max - GUID: 73c5e50a7860475f0000000000000000 (unverified)')
        self.parser.routeBattleyeEvent('Verified GUID (73c5e50a7860475f0000000000000000) of player #8 Max')
        self.assertEqual(2, len(self.evt_queue))
        event1, event2 = self.evt_queue
        self.assertEqual(self.parser.getEventID('EVT_CLIENT_CONNECT'), event1.type)
        self.assertEqual('Max', event1.client.name)
        self.assertEqual('8', event1.client.cid)
        self.assertEqual('73c5e50a7860475f0000000000000000', event1.client.guid)
        self.assertEqual('111.222.200.50', event1.client.ip)
        self.assertEqual(self.parser.getEventID('EVT_CLIENT_AUTH'), event2.type)
        self.assertEqual('Max', event2.client.name)
        self.assertEqual('8', event2.client.cid)
        self.assertEqual('73c5e50a7860475f0000000000000000', event2.client.guid)
        self.assertEqual('111.222.200.50', event2.client.ip)
        client_from_db = self.parser.storage.getClient(Client(guid='73c5e50a7860475f0000000000000000'))
        self.assertIsNotNone(client_from_db)
        self.assertEqual('Max', client_from_db.name)
        self.assertEqual('73c5e50a7860475f0000000000000000', client_from_db.guid)
        self.assertEqual('111.222.200.50', client_from_db.ip)

    def test_player_connecting_with_unverified_guid_at_first_and_sync(self):
        self.clear_events()
        self.parser.routeBattleyeEvent('Player #8 Max (111.222.200.50:2304) connected')
        self.parser.routeBattleyeEvent('Player #8 Max - GUID: 73c5e50a7860475f0000000000000000 (unverified)')
        when(self.parser.output).write('players').thenReturn('Players on server:\n[#] [IP Address]:[Port] [Ping] [GUID] [Name]\n--------------------------------------------------\n8   111.222.200.50:2304   -1   73c5e50a7860475f0000000000000000(?)  Max (Lobby)\n(14 players in total)')
        self.parser.sync()
        self.parser.routeBattleyeEvent('Verified GUID (73c5e50a7860475f0000000000000000) of player #8 Max')
        self.assert_has_event('EVT_CLIENT_CONNECT')
        self.assert_has_event('EVT_CLIENT_AUTH')
        client_from_db = self.parser.storage.getClient(Client(guid='73c5e50a7860475f0000000000000000'))
        self.assertIsNotNone(client_from_db)
        self.assertEqual('Max', client_from_db.name)
        self.assertEqual('73c5e50a7860475f0000000000000000', client_from_db.guid)
        self.assertEqual('111.222.200.50', client_from_db.ip)


class test_sync(EventParsingTestCase):

    def test_new_client_with_unverified_guid(self):
        self.assertDictContainsSubset({'clients': 1}, self.parser.storage.getCounts())
        self.assertNotIn('8', self.parser.clients)
        when(self.parser.output).write('players').thenReturn('Players on server:\n[#] [IP Address]:[Port] [Ping] [GUID] [Name]\n--------------------------------------------------\n8   111.222.200.50:2304   -1   73c5e50a7860475f49db400000000000(?)  Max (Lobby)\n(1 players in total)\n')
        rv = self.parser.sync()
        self.assertDictContainsSubset({'clients': 1}, self.parser.storage.getCounts())
        self.assertIn('8', rv)
        client = rv['8']
        self.assertEqual('Max', client.name)
        self.assertEqual('8', client.cid)
        self.assertEqual('111.222.200.50', client.ip)
        self.assertEqual('', client.guid)
        self.assertFalse(client.authed)
        self.assertIn('8', self.parser.clients)
        client = self.parser.clients['8']
        self.assertEqual('Max', client.name)
        self.assertEqual('111.222.200.50', client.ip)
        self.assertEqual('', client.guid)
        self.assertFalse(client.authed)

    def test_connected_client_with_unverified_guid(self):
        self.parser.routeBattleyeEvent('Player #8 Max (111.222.200.50:2304) connected')
        self.parser.routeBattleyeEvent('Player #8 Max - GUID: 73c5e50a7860475f0000000000000000 (unverified)')
        self.assertDictContainsSubset({'clients': 1}, self.parser.storage.getCounts())
        self.assertIn('8', self.parser.clients)
        self.clear_events()
        when(self.parser.output).write('players').thenReturn('Players on server:\n[#] [IP Address]:[Port] [Ping] [GUID] [Name]\n--------------------------------------------------\n8   111.222.200.50:2304   -1   73c5e50a7860475f49db400000000000(?)  Max (Lobby)\n(1 players in total)\n')
        rv = self.parser.sync()
        self.assertDictContainsSubset({'clients': 1}, self.parser.storage.getCounts())
        self.assertIn('8', rv)
        client = rv['8']
        self.assertEqual('Max', client.name)
        self.assertEqual('8', client.cid)
        self.assertEqual('111.222.200.50', client.ip)
        self.assertEqual('', client.guid)
        self.assertFalse(client.authed)
        self.assertIn('8', self.parser.clients)
        client = self.parser.clients['8']
        self.assertEqual('Max', client.name)
        self.assertEqual('111.222.200.50', client.ip)
        self.assertEqual('', client.guid)
        self.assertFalse(client.authed)

    def test_connected_client_with_verified_guid(self):
        self.parser.routeBattleyeEvent('Player #8 Max (111.222.200.50:2304) connected')
        self.parser.routeBattleyeEvent('Player #8 Max - GUID: 73c5e50a7860475f0000000000000000 (unverified)')
        self.parser.routeBattleyeEvent('Verified GUID (73c5e50a7860475f0000000000000000) of player #8 Max')
        self.assertDictContainsSubset({'clients': 2}, self.parser.storage.getCounts())
        self.assertIn('8', self.parser.clients)
        client_from_db = self.parser.storage.getClient(Client(guid='73c5e50a7860475f0000000000000000'))
        self.assertIsNotNone(client_from_db)
        self.assertEqual('Max', client_from_db.name)
        self.assertEqual('73c5e50a7860475f0000000000000000', client_from_db.guid)
        self.assertEqual('111.222.200.50', client_from_db.ip)
        self.clear_events()
        when(self.parser.output).write('players').thenReturn('Players on server:\n[#] [IP Address]:[Port] [Ping] [GUID] [Name]\n--------------------------------------------------\n8   111.222.200.50:2304   62   73c5e50a7860475f0000000000000000(OK) Max (Lobby)\n(1 players in total)\n')
        rv = self.parser.sync()
        self.assertDictContainsSubset({'clients': 2}, self.parser.storage.getCounts())
        self.assertIn('8', rv)
        client = rv['8']
        self.assertEqual('Max', client.name)
        self.assertEqual('8', client.cid)
        self.assertEqual('111.222.200.50', client.ip)
        self.assertEqual('73c5e50a7860475f0000000000000000', client.guid)
        self.assertTrue(client.authed)
        self.assertIn('8', self.parser.clients)
        client = self.parser.clients['8']
        self.assertEqual('Max', client.name)
        self.assertEqual('111.222.200.50', client.ip)
        self.assertEqual('73c5e50a7860475f0000000000000000', client.guid)
        self.assertTrue(client.authed)
        client_from_db = self.parser.storage.getClient(Client(guid='73c5e50a7860475f0000000000000000'))
        self.assertIsNotNone(client_from_db)
        self.assertEqual('Max', client_from_db.name)
        self.assertEqual('73c5e50a7860475f0000000000000000', client_from_db.guid)
        self.assertEqual('111.222.200.50', client_from_db.ip)