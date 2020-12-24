# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\afk\test_trigger_check_client.py
# Compiled at: 2016-03-08 18:42:10
from textwrap import dedent
from tests.plugins.afk import *
from mock import call, Mock
from b3 import TEAM_SPEC
from b3.events import Event

@pytest.yield_fixture
def plugin(console):
    p = plugin_maker_ini(console, dedent('\n        [settings]\n        consecutive_deaths_threshold: 3\n        inactivity_threshold: 30s\n        kick_reason: AFK for too long on this server\n        are_you_afk: Are you AFK?\n    '))
    p.MIN_INGAME_PLAYERS = 0
    p.onLoadConfig()
    p.onStartup()
    yield p
    p.disable()


def test_3_consecutive_deaths_with_no_activity(plugin, joe, jack):
    """
    player is killed 3 times in a row but shown some activity
    """
    plugin.check_client = Mock()
    joe.connects(1)
    jack.connects(2)
    plugin.on_client_activity(Event('', None, client=jack))
    joe.kills(jack)
    joe.kills(jack)
    assert not plugin.check_client.called
    joe.kills(jack)
    assert [
     call(jack)] == plugin.check_client.mock_calls
    return


def test_3_consecutive_deaths_with_some_activity(plugin, joe, jack):
    """
    player is killed 3 times in a row but shown some activity
    """
    plugin.check_client = Mock()
    joe.connects(1)
    jack.connects(2)
    plugin.on_client_activity(Event('', None, client=jack))
    joe.kills(jack)
    joe.kills(jack)
    plugin.on_client_activity(Event('', None, client=jack))
    assert not plugin.check_client.called
    joe.kills(jack)
    assert not plugin.check_client.called
    return


def testd_3_consecutive_deaths_with_no_activity_but_not_enough_players(plugin, joe, jack, bot):
    """
    player is killed 3 times in a row but shown some activity but he's the last player on the server
    """
    plugin.MIN_INGAME_PLAYERS = 1
    plugin.check_client = Mock()
    joe.connects(1)
    jack.connects(2)
    jack.team = TEAM_SPEC
    bot.connects(2)
    plugin.on_client_activity(Event('', None, client=joe))
    bot.kills(joe)
    bot.kills(joe)
    assert not plugin.check_client.called
    bot.kills(joe)
    assert not plugin.check_client.called
    return