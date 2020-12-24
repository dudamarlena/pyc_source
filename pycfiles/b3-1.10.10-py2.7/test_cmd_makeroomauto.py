# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\makeroom\test_cmd_makeroomauto.py
# Compiled at: 2016-03-08 18:42:10
from tests.plugins.makeroom import *
import pytest

@pytest.fixture
def plugin(console):
    p = plugin_maker_xml(console, '\n        <configuration>\n            <settings name="commands">\n                <set name="makeroomauto-mrauto">20</set>\n            </settings>\n            <settings name="automation">\n                <set name="enabled">no</set>\n                <set name="total_slots">3</set>\n                <set name="min_free_slots">1</set>\n            </settings>\n        </configuration>\n    ')
    p._delay = 0
    return p


def test_no_arg(plugin, superadmin):
    superadmin.connects(0)
    superadmin.says('!makeroomauto')
    assert ["expecting 'on' or 'off'"] == superadmin.message_history


def test_off(plugin, superadmin):
    superadmin.connects(0)
    plugin._automation_enabled = True
    superadmin.says('!makeroomauto off')
    assert False == plugin._automation_enabled
    assert ['Makeroom automation is OFF'] == superadmin.message_history


def test_on(plugin, superadmin):
    superadmin.connects(0)
    superadmin.says('!makeroomauto on')
    assert True == plugin._automation_enabled
    assert ['Makeroom automation is ON'] == superadmin.message_history


def test_junk(plugin, superadmin):
    superadmin.connects(0)
    superadmin.says('!makeroomauto f00')
    assert ["expecting 'on' or 'off'"] == superadmin.message_history