# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\spamcontrol\test_game_specific.py
# Compiled at: 2016-03-08 18:42:10
import b3, new
from mock import Mock
from mockito import when
from b3.events import Event
from b3.fake import FakeClient
from b3.plugins.spamcontrol import SpamcontrolPlugin
from tests.plugins.spamcontrol import SpamcontrolTestCase

class Test_game_specific_spam(SpamcontrolTestCase):

    def setUp(self):
        SpamcontrolTestCase.setUp(self)
        with open(b3.getAbsolutePath('@b3/conf/plugin_spamcontrol.ini')) as (default_conf):
            self.init_plugin(default_conf.read())
        self.joe = FakeClient(self.console, name='Joe', exactName='Joe', guid='zaerezarezar', groupBits=1)
        self.joe.connects('1')
        EVT_CLIENT_RADIO = self.console.Events.createEvent('EVT_CLIENT_RADIO', 'Event client radio')

        def onRadio(this, event):
            new_event = Event(type=event.type, client=event.client, target=event.target, data=event.data['text'])
            this.onChat(new_event)

        self.p.onRadio = new.instancemethod(onRadio, self.p, SpamcontrolPlugin)
        self.p.registerEvent('EVT_CLIENT_RADIO', self.p.onRadio)

        def radios(me, text):
            me.console.queueEvent(Event(type=EVT_CLIENT_RADIO, client=me, data={'text': text}))

        self.joe.radios = new.instancemethod(radios, self.joe, FakeClient)

    def test_radio_spam(self):
        when(self.p).getTime().thenReturn(0)
        self.joe.warn = Mock()
        self.joe.says('doh 1')
        self.joe.radios('doh 2')
        self.joe.says('doh 3')
        self.joe.radios('doh 4')
        self.joe.says('doh 5')
        self.assertEqual(1, self.joe.warn.call_count)