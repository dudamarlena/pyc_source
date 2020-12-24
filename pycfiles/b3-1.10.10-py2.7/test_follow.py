# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\urtserversidedemo\test_follow.py
# Compiled at: 2016-03-08 18:42:10
from mock import Mock
from mockito import when
from time import sleep
from b3.fake import FakeClient
from tests.plugins.urtserversidedemo import PluginTestCase
from b3.events import eventManager, Event
EVT_FOLLOW_CONNECTED = eventManager.createEvent('EVT_FOLLOW_CONNECTED', 'EVT_FOLLOW_CONNECTED')

class FollowPlugin:
    """
    dummy FollowPlugin
    """

    def __init__(self, console):
        self.working = True


class Test_with_follow(PluginTestCase):
    CONF = '[commands]\nstartserverdemo = 20\n\n[follow]\ndemo_duration: 2\n'

    def setUp(self):
        PluginTestCase.setUp(self)
        self.follow = FollowPlugin(self.p.console)
        when(self.console).getPlugin('follow').thenReturn(self.follow)
        self.p.onLoadConfig()
        self.p.onStartup()

    def tearDown(self):
        PluginTestCase.tearDown(self)

    def test_register_events(self):
        self.assertIn(EVT_FOLLOW_CONNECTED, self.p.events)

    def test_event_EVT_FOLLOW_CONNECTED(self):
        self.p._follow_demo_duration = 1.0 / 60 / 8
        self.p.start_recording_player = Mock()
        self.p.stop_recording_player = Mock()
        joe = FakeClient(console=self.console, name='Joe', guid='JOE_GUID')
        joe.connects('2')
        self.console.queueEvent(Event(EVT_FOLLOW_CONNECTED, data=None, client=joe))
        self.p.start_recording_player.assert_called_with(joe, None)
        sleep(0.2)
        self.p.stop_recording_player.assert_called_with(joe)
        return