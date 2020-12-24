# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\afk\test_misc.py
# Compiled at: 2016-03-08 18:42:10
from textwrap import dedent
from tests.plugins.afk import *
from b3 import TEAM_SPEC

@pytest.yield_fixture
def plugin(console):
    p = plugin_maker_ini(console, dedent('\n        [settings]\n    '))
    p.onLoadConfig()
    p.onStartup()
    yield p
    p.disable()


def test_count_ingame_humans(plugin, joe, jack, bot):
    assert 0 == plugin.count_ingame_humans()
    joe.connects(1)
    assert 1 == plugin.count_ingame_humans()
    bot.connects(2)
    assert 1 == plugin.count_ingame_humans()
    jack.connects(3)
    assert 2 == plugin.count_ingame_humans()
    joe.team = TEAM_SPEC
    assert 1 == plugin.count_ingame_humans()


def test_client_disconnection_clears_kick_timer(plugin, joe):
    plugin.last_chance_delay = 10
    joe.connects(1)
    joe.says('hi')
    assert hasattr(joe, 'last_activity_time')
    plugin.ask_client(joe)
    assert 1 == len(plugin.kick_timers)
    assert joe in plugin.kick_timers
    joe.disconnects()
    assert 0 == len(plugin.kick_timers)
    assert joe not in plugin.kick_timers
    assert not hasattr(joe, 'last_activity_time')