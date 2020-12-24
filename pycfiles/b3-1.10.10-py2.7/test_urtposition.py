# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\afk\test_urtposition.py
# Compiled at: 2016-03-08 18:42:10
from types import MethodType
from textwrap import dedent
from tests.plugins.afk import *
from mock import call, Mock

def evt_client_move(self, client):
    self.console.queueEvent(self.console.getEvent('EVT_CLIENT_MOVE', client=client))


def evt_client_standing(self, client):
    self.console.queueEvent(self.console.getEvent('EVT_CLIENT_STANDING', client=client))


@pytest.yield_fixture
def plugin(console):
    console.createEvent('EVT_CLIENT_MOVE', 'Event client move')
    console.createEvent('EVT_CLIENT_STANDING', 'Event client standing')
    p = plugin_maker_ini(console, dedent('\n        [settings]\n        consecutive_deaths_threshold: 3\n        inactivity_threshold: 30s\n        kick_reason: AFK for too long on this server\n        are_you_afk: Are you AFK?\n    '))
    p.evt_client_move = MethodType(evt_client_move, p, AfkPlugin)
    p.evt_client_standing = MethodType(evt_client_standing, p, AfkPlugin)
    p.MIN_INGAME_PLAYERS = 0
    p.onLoadConfig()
    p.onStartup()
    yield p
    p.disable()


def test_evt_client_standing(plugin, joe):
    """
    EVT_CLIENT_STANDING is received
    """
    plugin.check_client = Mock()
    joe.connects(1)
    plugin.evt_client_standing(joe)
    assert [
     call(joe)] == plugin.check_client.mock_calls


def test_evt_client_move(plugin, joe):
    """
    EVT_CLIENT_MOVE is considered as player activity
    """
    past_activity_time = 123654
    joe.connects(1)
    joe.last_activity_time = past_activity_time
    plugin.evt_client_move(joe)
    assert joe.last_activity_time > past_activity_time