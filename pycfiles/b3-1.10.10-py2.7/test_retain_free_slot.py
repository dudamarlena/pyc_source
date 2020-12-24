# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\makeroom\test_retain_free_slot.py
# Compiled at: 2016-03-08 18:42:10
from textwrap import dedent
import time
from tests.plugins.makeroom import *
from mock import Mock
import pytest
fake_time = int(time.time())

def get_fake_time():
    global fake_time
    return fake_time


@pytest.fixture
def plugin(console, monkeypatch):
    p = plugin_maker_ini(console, dedent('\n        [global_settings]\n        joe_level: reg\n        delay: 0\n        retain_free_duration: 10\n        [commands]\n        makeroom-mr: 20\n    '))
    monkeypatch.setattr(time, 'time', get_fake_time)
    return p


def test_kick_non_member_during_retain_free_duration(plugin, superadmin, joe, jack):
    global fake_time
    assert plugin._retain_free_duration == 10
    joe.kick = Mock()
    jack.kick = Mock()
    fake_time += 0
    superadmin.connects(0)
    joe.connects(1)
    superadmin.says('!makeroom')
    assert joe.kick.call_count == 1
    fake_time += 1
    jack.connects(2)
    assert jack.kick.call_count == 1


def test_dont_kick_non_member_after_retain_free_duration(plugin, superadmin, joe, jack):
    global fake_time
    assert plugin._retain_free_duration == 10
    joe.kick = Mock()
    jack.kick = Mock()
    fake_time += 0
    superadmin.connects(0)
    joe.connects(1)
    superadmin.says('!makeroom')
    assert joe.kick.call_count == 1
    fake_time += 11
    jack.connects(2)
    assert jack.kick.call_count == 0


def test_non_members_can_connect_during_retain_free_duration_if_a_member_joined(plugin, superadmin, moderator, joe, jack):
    global fake_time
    assert plugin._retain_free_duration == 10
    joe.kick = Mock()
    jack.kick = Mock()
    fake_time += 0
    superadmin.connects(0)
    joe.connects(1)
    superadmin.says('!makeroom')
    assert joe.kick.call_count == 1
    fake_time += 1
    moderator.connects(3)
    fake_time += 1
    jack.connects(4)
    assert jack.kick.call_count == 0


def test_dont_kick_joes_during_retain_free_duration_of_zero(plugin, superadmin, joe, jack):
    global fake_time
    plugin._retain_free_duration = 0
    joe = joe
    joe.kick = Mock()
    jack = jack
    jack.kick = Mock()
    fake_time += 0
    superadmin.connects(0)
    joe.connects(1)
    superadmin.says('!makeroom')
    assert joe.kick.call_count == 1
    fake_time += 1
    jack.connects(2)
    assert jack.kick.call_count == 0