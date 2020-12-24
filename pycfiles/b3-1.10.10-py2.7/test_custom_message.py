# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\makeroom\test_custom_message.py
# Compiled at: 2016-03-08 18:42:10
from textwrap import dedent
import pytest
from mock import call, Mock
from tests.plugins.makeroom import *

@pytest.fixture
def plugin(console):
    p = plugin_maker_ini(console, dedent('\n        [commands]\n        makeroom: 20\n        [messages]\n        kick_message: kicking $clientname to make room for a member xxxxxxxxxx\n        kick_reason: to free a slot ! mlkjmlkj\n    '))
    p._delay = 0
    p.console.say = Mock()
    return p


def test_custom_message(plugin, moderator, joe):
    moderator.connects('0')
    joe.connects('1')
    joe.kick = Mock()
    moderator.says('!makeroom')
    assert [
     call('kicking Joe to make room for a member xxxxxxxxxx')] == plugin.console.say.mock_calls
    assert [
     call(admin=moderator, reason='to free a slot ! mlkjmlkj', silent=True, keyword='makeroom')] == joe.kick.mock_calls