# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\makeroom\test_automation.py
# Compiled at: 2016-03-08 18:42:10
import time, pytest
from textwrap import dedent
from tests.plugins.makeroom import *
from mock import call, Mock

@pytest.fixture
def plugin(console):
    p = plugin_maker_ini(console, dedent('\n        [commands]\n        makeroomauto-mrauto: 20\n        [automation]\n        enabled: no\n        total_slots: 3\n        min_free_slots: 1\n    '))
    p._delay = 0
    return p


def test_kick_last_connected_non_member_when_on(plugin, superadmin, joe, moderator):
    plugin._automation_enabled = True
    plugin._total_slots = 3
    plugin._min_free_slots = 1
    joe.kick = Mock()
    moderator.kick = Mock()
    superadmin.connects(0)
    joe.connects(1)
    moderator.connects(2)
    assert [] == moderator.kick.mock_calls
    assert [
     call(admin=None, reason='to free a slot', silent=True, keyword='makeroom')] == joe.kick.mock_calls
    return


def test_kick_non_member_when_on(plugin, superadmin, joe):
    plugin._automation_enabled = True
    plugin._total_slots = 2
    plugin._min_free_slots = 1
    joe.kick = Mock()
    superadmin.connects(0)
    joe.connects(1)
    assert [
     call(reason='to free a slot', silent=True, keyword='makeroom')] == joe.kick.mock_calls


def test_kick_non_member_when_on_with_delay(plugin, superadmin, joe):
    plugin._automation_enabled = True
    plugin._total_slots = 2
    plugin._min_free_slots = 1
    plugin._delay = 0.1
    joe.kick = Mock()
    superadmin.connects(0)
    joe.connects(1)
    time.sleep(0.2)
    assert [call(reason='to free a slot', silent=True, keyword='makeroom')] == joe.kick.mock_calls


def test_no_kick_non_member_when_on_and_enough_free_slots(plugin, superadmin, joe):
    plugin._automation_enabled = True
    plugin._total_slots = 3
    plugin._min_free_slots = 1
    joe.kick = Mock()
    superadmin.connects(0)
    joe.connects(1)
    assert [] == joe.kick.mock_calls


def test_no_kick_member_when_off(plugin, superadmin, joe):
    plugin._automation_enabled = False
    plugin._total_slots = 2
    plugin._min_free_slots = 1
    joe._groupBits = 8
    joe.kick = Mock()
    superadmin.connects(0)
    joe.connects(1)
    assert [] == joe.kick.mock_calls


def test_no_kick_non_member_when_off(plugin, superadmin, joe):
    plugin._automation_enabled = False
    plugin._total_slots = 2
    plugin._min_free_slots = 1
    joe.kick = Mock()
    superadmin.connects(0)
    joe.connects(1)
    assert [] == joe.kick.mock_calls