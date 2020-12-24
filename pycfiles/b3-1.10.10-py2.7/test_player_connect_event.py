# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\urtserversidedemo\test_player_connect_event.py
# Compiled at: 2016-03-08 18:42:10
from mock import Mock
from b3.events import Event
from tests.plugins.urtserversidedemo import PluginTestCase
from b3.fake import FakeClient
from time import sleep

class Test_player_connect_event(PluginTestCase):
    CONF = '[commands]\nstartserverdemo = 20\nstopserverdemo = 20\n'

    def setUp(self):
        PluginTestCase.setUp(self)
        self.p.onStartup()
        self.joe = FakeClient(self.console, name='Joe', guid='01230123012301230123', groupBits=1)
        self.joe.clearMessageHistory()
        self.p.start_recording_player = Mock(return_value='startserverdemo: recording ')
        self.p.start_recording_player.reset_mock()

    def test_auto_start_demo_of_connecting_players(self):
        self.p._recording_all_players = True
        self.joe.connects('2')
        self.console.queueEvent(Event(self.console.getEventID('EVT_CLIENT_JOIN'), self.joe, self.joe))
        sleep(0.5)
        self.assertTrue(self.p.start_recording_player.called)
        self.p.start_recording_player.assert_called_with(self.joe, None)
        return

    def test_do_not_auto_start_demo_of_connecting_players(self):
        self.p._recording_all_players = False
        self.joe.connects('2')
        sleep(0.5)
        self.assertFalse(self.p.start_recording_player.called)