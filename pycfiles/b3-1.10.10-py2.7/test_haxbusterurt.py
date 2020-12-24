# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\urtserversidedemo\test_haxbusterurt.py
# Compiled at: 2016-03-08 18:42:10
from mock import Mock
from mockito import when
from time import sleep
from b3.fake import FakeClient
from tests.plugins.urtserversidedemo import PluginTestCase
from b3.events import eventManager, Event
from time import sleep
EVT_BAD_GUID = eventManager.createEvent('EVT_BAD_GUID', 'Bad guid detected')
EVT_1337_PORT = eventManager.createEvent('EVT_1337_PORT', '1337 port detected')

class HaxbusterurtPlugin:
    """
    dummy HaxbusterurtPlugin
    """

    def __init__(self, console):
        self.working = True


class Test_with_haxbusterurt(PluginTestCase):
    CONF = '[commands]\nstartserverdemo = 20\n\n[haxbusterurt]\ndemo_duration: 2\n'

    def setUp(self):
        PluginTestCase.setUp(self)
        self.haxbusterurt = HaxbusterurtPlugin(self.p.console)
        when(self.console).getPlugin('haxbusterurt').thenReturn(self.haxbusterurt)
        self.console.createEvent('EVT_BAD_GUID', 'Bad guid detected')
        self.console.createEvent('EVT_1337_PORT', '1337 port detected')
        self.p.onLoadConfig()
        self.p.onStartup()

    def tearDown(self):
        PluginTestCase.tearDown(self)

    def test_register_events(self):
        self.assertIn(self.console.getEventID('EVT_BAD_GUID'), self.p.events)
        self.assertIn(self.console.getEventID('EVT_1337_PORT'), self.p.events)

    def test_event_EVT_BAD_GUID(self):
        self.p._haxbusterurt_demo_duration = 1.0 / 60 / 8
        self.p.start_recording_player = Mock()
        self.p.stop_recording_player = Mock()
        joe = FakeClient(console=self.console, name='Joe', guid='JOE_GUID')
        joe.connects('2')
        self.console.queueEvent(Event(self.console.getEventID('EVT_BAD_GUID'), data=joe.guid, client=joe))
        sleep(0.5)
        self.p.start_recording_player.assert_called_with(joe, None)
        sleep(0.5)
        self.p.stop_recording_player.assert_called_with(joe)
        return

    def test_event_EVT_1337_PORT(self):
        self.p._haxbusterurt_demo_duration = 1.0 / 60 / 8
        self.p.start_recording_player = Mock()
        self.p.stop_recording_player = Mock()
        joe = FakeClient(console=self.console, name='Joe', guid='JOE_GUID')
        joe.connects('2')
        self.console.queueEvent(Event(self.console.getEventID('EVT_1337_PORT'), data=joe.guid, client=joe))
        sleep(0.5)
        self.p.start_recording_player.assert_called_with(joe, None)
        sleep(0.5)
        self.p.stop_recording_player.assert_called_with(joe)
        return