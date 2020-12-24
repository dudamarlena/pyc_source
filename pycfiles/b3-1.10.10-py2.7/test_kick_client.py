# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\afk\test_kick_client.py
# Compiled at: 2016-03-08 18:42:10
from textwrap import dedent
from time import time
from tests.plugins.afk import *
from mock import call, Mock
from b3 import TEAM_SPEC, TEAM_RED

@pytest.yield_fixture
def plugin(console):
    with logging_disabled():
        p = plugin_maker_ini(console, dedent('\n            [settings]\n        '))
        p.inactivity_threshold_second = 0.05
        p.onLoadConfig()
        p.onStartup()
    yield p
    p.disable()


def too_long_ago():
    return time() - 10


def very_recently():
    return time() - 0.001


def test_nominal(plugin, joe):
    joe.kick = Mock()
    plugin.min_ingame_humans = 0
    joe.connects(1)
    joe.last_activity_time = too_long_ago()
    plugin.kick_client(joe)
    assert [
     call(reason='AFK for too long on this server')] == joe.kick.mock_calls


def test_too_few_players_remaining(plugin, joe, jack):
    joe.kick = Mock()
    plugin.min_ingame_humans = 1
    joe.connects(1)
    jack.connects(2)
    jack.team = TEAM_SPEC
    joe.last_activity_time = too_long_ago()
    plugin.kick_client(joe)
    assert [] == joe.kick.mock_calls
    jack.team = TEAM_RED
    joe.last_activity_time = too_long_ago()
    plugin.kick_client(joe)
    assert [
     call(reason='AFK for too long on this server')] == joe.kick.mock_calls


def test_activity_at_the_last_second(plugin, joe):
    joe.kick = Mock()
    plugin.min_ingame_humans = 0
    joe.connects(1)
    joe.last_activity_time = very_recently()
    plugin.kick_client(joe)
    assert [] == joe.kick.mock_calls
    joe.last_activity_time = too_long_ago()
    plugin.kick_client(joe)
    assert [
     call(reason='AFK for too long on this server')] == joe.kick.mock_calls


def test_player_moved_to_spec(plugin, joe, jack):
    joe.kick = Mock()
    plugin.min_ingame_humans = 0
    joe.connects(1)
    jack.connects(2)
    joe.team = TEAM_SPEC
    joe.last_activity_time = too_long_ago()
    plugin.kick_client(joe)
    assert [] == joe.kick.mock_calls
    joe.team = TEAM_RED
    joe.last_activity_time = too_long_ago()
    plugin.kick_client(joe)
    assert [
     call(reason='AFK for too long on this server')] == joe.kick.mock_calls