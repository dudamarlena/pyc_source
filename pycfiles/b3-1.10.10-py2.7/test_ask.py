# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\afk\test_ask.py
# Compiled at: 2016-03-08 18:42:10
from textwrap import dedent
from time import sleep
from tests.plugins.afk import *
from mock import call, Mock

@pytest.yield_fixture
def plugin(console):
    p = None
    with logging_disabled():
        p = plugin_maker_ini(console, dedent('\n            [settings]\n            consecutive_deaths_threshold: 3\n            inactivity_threshold: 30s\n            last_chance_delay: 23\n            kick_reason: AFK for too long on this server\n            are_you_afk: Are you AFK?\n            suspicion_announcement: {name} is AFK, kicking in {last_chance_delay}s\n        '))
        plugin.inactivity_threshold_second = 0
        p.MIN_INGAME_PLAYERS = 0
        p.kick_client = Mock()
        p.console.say = Mock()
        p.onLoadConfig()
        p.onStartup()
    yield p
    p.disable()
    return


def test_ask(plugin, joe):
    joe.message = Mock()
    plugin.ask_client(joe)
    assert [
     call('Are you AFK?')] == joe.message.mock_calls
    assert joe in plugin.kick_timers
    assert [call('Joe is AFK, kicking in 23s')] == plugin.console.say.mock_calls


def test_no_response(plugin, joe):
    plugin.last_chance_delay = 0.005
    joe.message = Mock()
    joe.connects(1)
    plugin.ask_client(joe)
    assert [
     call('Are you AFK?')] == joe.message.mock_calls
    assert [call('Joe is AFK, kicking in 0.005s')] == plugin.console.say.mock_calls
    sleep(0.01)
    assert [
     call(joe)] == plugin.kick_client.mock_calls


def test_response(plugin, joe):
    plugin.last_chance_delay = 0.005
    joe.message = Mock()
    joe.connects(1)
    plugin.ask_client(joe)
    assert [
     call('Are you AFK?')] == joe.message.mock_calls
    assert [call('Joe is AFK, kicking in 0.005s')] == plugin.console.say.mock_calls
    joe.says('hi')
    assert joe not in plugin.kick_timers
    sleep(0.01)
    assert [] == plugin.kick_client.mock_calls
    assert joe not in plugin.kick_timers


def test_make_kill(plugin, joe):
    plugin.last_chance_delay = 0.005
    joe.message = Mock()
    joe.connects(1)
    plugin.ask_client(joe)
    assert [
     call('Are you AFK?')] == joe.message.mock_calls
    assert [call('Joe is AFK, kicking in 0.005s')] == plugin.console.say.mock_calls
    joe.kills(joe)
    assert joe not in plugin.kick_timers
    sleep(0.01)
    assert [] == plugin.kick_client.mock_calls


def test_ask_twice(plugin, joe):
    joe.message = Mock()
    plugin.ask_client(joe)
    assert [
     call('Are you AFK?')] == joe.message.mock_calls
    assert joe in plugin.kick_timers
    assert [call('Joe is AFK, kicking in 23s')] == plugin.console.say.mock_calls
    plugin.ask_client(joe)
    assert [call('Are you AFK?')] == joe.message.mock_calls
    assert joe in plugin.kick_timers
    assert [call('Joe is AFK, kicking in 23s')] == plugin.console.say.mock_calls