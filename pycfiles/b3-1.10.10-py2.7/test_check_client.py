# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\afk\test_check_client.py
# Compiled at: 2016-03-08 18:42:10
from textwrap import dedent
from time import time
from tests.plugins.afk import *
from mock import call, Mock
from b3.events import Event

@pytest.yield_fixture
def plugin(console):
    p = plugin_maker_ini(console, dedent('\n        [settings]\n        consecutive_deaths_threshold: 3\n        inactivity_threshold: 30s\n        kick_reason: AFK for too long on this server\n        are_you_afk: Are you AFK?\n    '))
    p.ask_client = Mock()
    p.onLoadConfig()
    p.onStartup()
    yield p
    p.disable()


def test_active_recently(plugin, joe):
    """
    check a player who was active 20s ago
    """
    now = time()
    joe.connects(1)
    plugin.on_client_activity(Event('', None, client=joe), now=now - 20)
    plugin.check_client(joe)
    assert not plugin.ask_client.called
    return


def test_not_active_recently(plugin, joe):
    """
    check a player who was active 50s ago
    """
    now = time()
    joe.connects(1)
    plugin.on_client_activity(Event('', None, client=joe), now=now - 50)
    plugin.check_client(joe)
    assert [
     call(joe)] == plugin.ask_client.mock_calls
    return


def test_not_active_recently_but_superadmin(plugin, superadmin):
    """
    check an immune player who was active 50s ago
    """
    now = time()
    superadmin.connects(1)
    plugin.on_client_activity(Event('', None, client=superadmin), now=now - 50)
    plugin.check_client(superadmin)
    assert not plugin.ask_client.called
    return


def test_not_active_recently_but_bot(plugin, bot):
    """
    check a bot who was active 50s ago
    """
    now = time()
    bot.connects(1)
    bot.bot = True
    plugin.on_client_activity(Event('', None, client=bot), now=now - 50)
    plugin.check_client(bot)
    assert not plugin.ask_client.called
    return