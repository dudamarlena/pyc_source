# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\urtserversidedemo\test_startserverdemo.py
# Compiled at: 2016-03-08 18:42:10
from mockito import when, verify
from tests.plugins.urtserversidedemo import PluginTestCase
from b3.fake import FakeClient

class Test_startserverdemo(PluginTestCase):
    CONF = '[commands]\nstartserverdemo = 20\n'

    def setUp(self):
        PluginTestCase.setUp(self)
        self.p.onStartup()
        self.moderator = FakeClient(self.console, name='Moderator', exactName='Moderator', guid='654654654654654654', groupBits=8)
        self.moderator.connects('0')
        self.moderator.clearMessageHistory()

    def test_no_parameter(self):
        self.moderator.says('!startserverdemo')
        self.assertListEqual(["specify a player name or 'all'"], self.moderator.message_history)

    def test_non_existing_player(self):
        self.moderator.says('!startserverdemo foo')
        self.assertListEqual(['No players found matching foo'], self.moderator.message_history)

    def test_all(self):
        self.p._recording_all_players = False
        when(self.console).write('startserverdemo all').thenReturn('startserverdemo: recording laCourge to serverdemos/2012_04_22_20-16-38_laCourge_642817.dm_68')
        self.moderator.says('!startserverdemo all')
        self.assertTrue(self.p._recording_all_players)
        self.assertListEqual(['startserverdemo: recording laCourge to serverdemos/2012_04_22_20-16-38_laCourge_642817.dm_68'], self.moderator.message_history)

    def test_existing_player(self):
        joe = FakeClient(self.console, name='Joe', guid='01230123012301230123', groupBits=1)
        joe.connects('1')
        self.assertEqual(joe, self.console.clients['1'])
        when(self.console).write('startserverdemo 1').thenReturn('startserverdemo: recording Joe to serverdemos/2012_04_22_20-16-38_Joe_642817.dm_68')
        self.moderator.says('!startserverdemo joe')
        self.assertListEqual(['startserverdemo: recording Joe to serverdemos/2012_04_22_20-16-38_Joe_642817.dm_68'], self.moderator.message_history)