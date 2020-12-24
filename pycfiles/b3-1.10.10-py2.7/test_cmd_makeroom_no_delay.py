# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\makeroom\test_cmd_makeroom_no_delay.py
# Compiled at: 2016-03-08 18:42:10
import time, pytest
from textwrap import dedent
from tests.plugins.makeroom import *
from mock import Mock
t = int(time.time())

@pytest.fixture
def plugin(console):
    p = plugin_maker_ini(console, dedent('\n        [global_settings]\n        non_member_level: 2\n        delay: 0\n        [commands]\n        makeroom-mr: 20\n    '))
    return p


def test_no_player_to_kick(plugin, superadmin):
    superadmin.connects(0)
    superadmin.says('!makeroom')
    assert [
     'No non-member found to kick !'] == superadmin.message_history


def test_no_non_member_to_kick(plugin, superadmin, moderator):
    superadmin.connects(0)
    moderator.connects(1)
    superadmin.says('!makeroom')
    assert [
     'No non-member found to kick !'] == superadmin.message_history


def test_one_player_to_kick(plugin, superadmin, joe):
    superadmin.connects(0)
    joe.connects(1)
    joe.kick = Mock()
    superadmin.says('!makeroom')
    assert 1 == joe.kick.call_count
    assert ['Joe was kicked to free a slot'] == superadmin.message_history


def test_kick_last_connected_player(plugin, superadmin, joe, jack):
    superadmin.connects(0)
    joe.connects(1)
    joe.timeAdd = t
    joe.kick = Mock()
    jack.connects(2)
    jack.timeAdd = t + 1
    jack.kick = Mock()
    superadmin.says('!makeroom')
    assert 0 == joe.kick.call_count
    assert 1 == jack.kick.call_count
    assert ['Jack was kicked to free a slot'] == superadmin.message_history


def test_kick_player_of_lowest_B3_group(plugin, superadmin, joe, moderator):
    superadmin.connects(0)
    joe.connects(1)
    joe.timeAdd = t
    joe.kick = Mock()
    moderator.connects(2)
    moderator.timeAdd = t + 1
    moderator.kick = Mock()
    superadmin.says('!makeroom')
    assert 1 == joe.kick.call_count
    assert 0 == moderator.kick.call_count
    assert ['Joe was kicked to free a slot'] == superadmin.message_history


def test_makeroom_called_during_retain_free_slot_duration(plugin, superadmin, joe):
    plugin._retain_free_duration = 5
    superadmin.connects(0)
    joe.connects(1)
    superadmin.says('!makeroom')
    time.sleep(0.3)
    superadmin.says('!makeroom')
    assert [
     'Joe was kicked to free a slot. A member has 5s to join the server',
     'There is already a makeroom request in progress. Try again later in 4s'] == superadmin.message_history