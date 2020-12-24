# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\afk\test_game_break.py
# Compiled at: 2016-03-08 18:42:10
from textwrap import dedent
from tests.plugins.afk import *
from mock import Mock

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


def test_game_break(plugin, joe):
    joe.connects(1)
    plugin.ask_client(joe)
    assert joe in plugin.kick_timers
    plugin.on_game_break(None)
    assert joe not in plugin.kick_timers
    return