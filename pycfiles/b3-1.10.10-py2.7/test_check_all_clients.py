# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\afk\test_check_all_clients.py
# Compiled at: 2016-03-08 18:42:10
from time import time
from textwrap import dedent
from tests.plugins.afk import *
from mock import call, Mock
from b3.fake import FakeClient

def a_long_time_ago():
    return time() - 40


def fakeclient_repr(self):
    return self.name


FakeClient.__repr__ = fakeclient_repr

@pytest.yield_fixture
def plugin(console):
    p = plugin_maker_ini(console, dedent('\n        [settings]\n        inactivity_threshold: 30s\n    '))
    p.last_global_check_time = a_long_time_ago()
    p.check_client = Mock()
    p.onLoadConfig()
    p.onStartup()
    yield p
    p.disable()


def test_someone_saying_afk_triggers_check(plugin, bot, joe, jack):
    bot.connects(1)
    joe.connects(2)
    jack.connects(3)
    bot.last_activity_time = a_long_time_ago()
    joe.last_activity_time = a_long_time_ago()
    jack.last_activity_time = a_long_time_ago()
    jack.says('Joe is afk!!!')
    assert [
     call(joe), call(jack)] == plugin.check_client.mock_calls


def test_do_not_check_all_players_too_often(plugin, joe):
    now = time()
    joe.connects(2)
    plugin.check_all_clients(now=now)
    assert [
     call(joe)] == plugin.check_client.mock_calls
    plugin.check_all_clients(now=now + 10)
    assert [
     call(joe)] == plugin.check_client.mock_calls
    plugin.check_all_clients(now=now + 16)
    assert [
     call(joe), call(joe)] == plugin.check_client.mock_calls