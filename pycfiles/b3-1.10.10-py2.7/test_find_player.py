# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\customcommands\test_find_player.py
# Compiled at: 2016-03-08 18:42:10
from mock import patch, call
from b3.config import CfgConfigParser
from b3.plugins.customcommands import CustomcommandsPlugin
from tests import logging_disabled
from tests.plugins.customcommands import CustomcommandsTestCase
with logging_disabled():
    from b3.fake import FakeClient

class Test_find_player(CustomcommandsTestCase):

    def setUp(self):
        with logging_disabled():
            CustomcommandsTestCase.setUp(self)
            self.conf = CfgConfigParser()
            self.p = CustomcommandsPlugin(self.console, self.conf)
            self.guest = FakeClient(console=self.console, name='Guest', guid='GuestGUID', pbid='GuestPBID', group_bits=0)
            self.player1 = FakeClient(console=self.console, name='player1', guid='player1GUID', pbid='player1PBID', group_bits=1)
            self.player1.connects(cid='CID1')
            self.player2 = FakeClient(console=self.console, name='player2', guid='player2GUID', pbid='player2PBID', group_bits=1)
            self.player2.connects(cid='CID2')
            self.guest.connects(cid='guestCID')

    def init(self, conf_content):
        with logging_disabled():
            self.conf.loadFromString(conf_content)
            self.p.onLoadConfig()
            self.p.onStartup()

    def test_ARG_FIND_PLAYER_NAME_no_parameter(self):
        self.init('\n[guest commands]\nf00 = f00 #<ARG:FIND_PLAYER:NAME>#\n        ')
        with patch.object(self.console, 'write') as (write_mock):
            self.guest.says('!f00')
        self.assertListEqual(['Error: missing parameter'], self.guest.message_history)
        self.assertListEqual([], write_mock.mock_calls)

    def test_ARG_FIND_PLAYER_NAME_no_match(self):
        self.init('\n[guest commands]\nf00 = f00 #<ARG:FIND_PLAYER:NAME>#\n        ')
        with patch.object(self.console, 'write') as (write_mock):
            self.guest.says('!f00 bar')
        self.assertListEqual(['No players found matching bar'], self.guest.message_history)
        self.assertListEqual([], write_mock.mock_calls)

    def test_ARG_FIND_PLAYER_NAME_with_multiple_matches(self):
        self.init('\n[guest commands]\nf00 = f00 #<ARG:FIND_PLAYER:NAME>#\n        ')
        with patch.object(self.console, 'write') as (write_mock):
            self.guest.says('!f00 player')
        self.assertListEqual(['Players matching player player1 [CID1], player2 [CID2]'], self.guest.message_history)
        self.assertListEqual([], write_mock.mock_calls)