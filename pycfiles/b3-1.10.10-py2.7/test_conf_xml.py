# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\makeroom\test_conf_xml.py
# Compiled at: 2016-03-08 18:42:10
from tests.plugins.makeroom import *

def test_empty_conf(console):
    plugin = plugin_maker_xml(console, '<configuration/>')
    assert 2 == plugin._non_member_level
    assert 5.0 == plugin._delay
    assert None is plugin._automation_enabled
    assert None is plugin._total_slots
    assert None is plugin._min_free_slots
    return


def test_non_member_level(console):
    plugin = plugin_maker_xml(console, '<configuration>\n            <settings name="global_settings">\n                <set name="non_member_level">20</set>\n            </settings>\n        </configuration>')
    assert 20 == plugin._non_member_level


def test_non_member_level_with_group_names(console):
    plugin = plugin_maker_xml(console, '<configuration>\n            <settings name="global_settings">\n                <set name="non_member_level">mod</set>\n            </settings>\n        </configuration>')
    assert 20 == plugin._non_member_level


def test_delay(console):
    plugin = plugin_maker_xml(console, '<configuration>\n            <settings name="global_settings">\n                <set name="delay">20</set>\n            </settings>\n        </configuration>')
    assert 20 == plugin._delay


def test_automation_missing_enabled(console):
    plugin = plugin_maker_xml(console, '<configuration>\n            <settings name="automation">\n                <set name="total_slots">5</set>\n                <set name="min_free_slots">1</set>\n            </settings>\n        </configuration>')
    assert None is plugin._automation_enabled
    return


def test_automation_off(console):
    plugin = plugin_maker_xml(console, '<configuration>\n            <settings name="automation">\n                <set name="enabled">no</set>\n                <set name="total_slots">5</set>\n                <set name="min_free_slots">1</set>\n            </settings>\n        </configuration>')
    assert False is plugin._automation_enabled


def test_automation_on(console):
    plugin = plugin_maker_xml(console, '<configuration>\n            <settings name="automation">\n                <set name="enabled">yes</set>\n                <set name="total_slots">5</set>\n                <set name="min_free_slots">1</set>\n            </settings>\n        </configuration>')
    assert True is plugin._automation_enabled


def test_automation_total_slots(console):
    plugin = plugin_maker_xml(console, '<configuration>\n            <settings name="automation">\n                <set name="enabled">yes</set>\n                <set name="total_slots">6</set>\n                <set name="min_free_slots">1</set>\n            </settings>\n        </configuration>')
    assert 6 == plugin._total_slots


def test_automation_min_free_slots(console):
    plugin = plugin_maker_xml(console, '<configuration>\n            <settings name="automation">\n                <set name="enabled">yes</set>\n                <set name="total_slots">6</set>\n                <set name="min_free_slots">3</set>\n            </settings>\n        </configuration>')
    assert 3 == plugin._min_free_slots


def test_automation_total_slots_cannot_be_less_than_2(console):
    plugin = plugin_maker_xml(console, '<configuration>\n            <settings name="automation">\n                <set name="enabled">yes</set>\n                <set name="total_slots">1</set>\n                <set name="min_free_slots">1</set>\n            </settings>\n        </configuration>')
    assert None is plugin._automation_enabled
    return