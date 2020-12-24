# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\urtserversidedemo\test_stopserverdemo.py
# Compiled at: 2016-03-08 18:42:10
from mockito import when
from tests.plugins.urtserversidedemo import PluginTestCase
from b3.fake import FakeClient

class Test_stopserverdemo(PluginTestCase):
    CONF = '[commands]\nstopserverdemo = 20\n'

    def setUp(self):
        PluginTestCase.setUp(self)
        self.p.onStartup()
        self.moderator = FakeClient(self.console, name='Moderator', exactName='Moderator', guid='654654654654654654', groupBits=8)
        self.moderator.connects('0')
        self.moderator.clearMessageHistory()

    def test_no_parameter(self):
        self.moderator.says('!stopserverdemo')
        self.assertListEqual(["specify a player name or 'all'"], self.moderator.message_history)

    def test_non_existing_player(self):
        self.moderator.says('!stopserverdemo foo')
        self.assertListEqual(['No players found matching foo'], self.moderator.message_history)

    def test_all(self):
        self.p._recording_all_players = True
        when(self.console).write('stopserverdemo all').thenReturn('stopserverdemo: stopped recording laCourge')
        self.moderator.says('!stopserverdemo all')
        self.assertFalse(self.p._recording_all_players)
        self.assertListEqual(['stopserverdemo: stopped recording laCourge'], self.moderator.message_history)

    def test_existing_player(self):
        joe = FakeClient(self.console, name='Joe', guid='01230123012301230123', groupBits=1)
        joe.connects('1')
        self.assertEqual(joe, self.console.clients['1'])
        when(self.console).write('stopserverdemo 1').thenReturn('stopserverdemo: stopped recording Joe')
        self.moderator.says('!stopserverdemo joe')