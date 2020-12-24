# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\makeroom\test_conf_ini.py
# Compiled at: 2016-03-08 18:42:10
import os, pytest
from textwrap import dedent
from tests.plugins.makeroom import *

@pytest.mark.skipif(not os.path.exists(DEFAULT_PLUGIN_CONFIG_FILE), reason='Could not find default plugin config file %r' % DEFAULT_PLUGIN_CONFIG_FILE)
def test_default_conf(console):
    plugin = plugin_maker(console, DEFAULT_PLUGIN_CONFIG_FILE)
    assert 2 == plugin._non_member_level
    assert 2.0 == plugin._delay
    assert 15 == plugin._retain_free_duration
    assert False is plugin._automation_enabled
    assert 32 is plugin._total_slots
    assert 1 is plugin._min_free_slots
    assert plugin.config.get('messages', 'kick_message') == 'kicking $clientname to free a slot'
    assert plugin.config.get('messages', 'kick_reason') == 'to make room for a server member'
    assert plugin.config.get('messages', 'info_message') == 'Making room for clan member, please come back again'
    admin_plugin = console.getPlugin('admin')
    assert 'makeroom' in admin_plugin._commands
    assert admin_plugin._commands['makeroom'].level == (20, 100)
    assert 'mkr' in admin_plugin._commands
    assert admin_plugin._commands['mkr'].level == (20, 100)
    assert 'makeroomauto' in admin_plugin._commands
    assert admin_plugin._commands['makeroomauto'].level == (60, 100)
    assert 'mrauto' in admin_plugin._commands
    assert admin_plugin._commands['mrauto'].level == (60, 100)


def test_empty_conf(console):
    plugin = plugin_maker_ini(console, dedent(''))
    assert 2 == plugin._non_member_level
    assert 5.0 == plugin._delay
    assert None is plugin._automation_enabled
    assert None is plugin._total_slots
    assert None is plugin._min_free_slots
    return


def test_non_member_level(console):
    plugin = plugin_maker_ini(console, dedent('\n        [global_settings]\n        non_member_level: 20\n        '))
    assert 20 == plugin._non_member_level


def test_non_member_level_with_group_names(console):
    plugin = plugin_maker_ini(console, dedent('\n        [global_settings]\n        non_member_level: mod\n        '))
    assert 20 == plugin._non_member_level


def test_delay(console):
    plugin = plugin_maker_ini(console, dedent('\n        [global_settings]\n        delay: 20\n        '))
    assert 20 == plugin._delay


def test_automation_missing_enabled(console):
    plugin = plugin_maker_ini(console, dedent('\n        [automation]\n        total_slots: 5\n        min_free_slots: 1\n        '))
    assert None is plugin._automation_enabled
    return


def test_automation_junk_enabled(console):
    plugin = plugin_maker_ini(console, dedent('\n        [automation]\n        enabled: f00\n        '))
    assert None is plugin._automation_enabled
    return


def test_automation_off(console):
    plugin = plugin_maker_ini(console, dedent('\n        [automation]\n        enabled: no\n        total_slots: 5\n        min_free_slots: 1\n        '))
    assert False is plugin._automation_enabled


def test_automation_on(console):
    plugin = plugin_maker_ini(console, dedent('\n        [automation]\n        enabled: yes\n        total_slots: 5\n        min_free_slots: 1\n        '))
    assert True is plugin._automation_enabled


def test_automation_total_slots(console):
    plugin = plugin_maker_ini(console, dedent('\n        [automation]\n        enabled: yes\n        total_slots: 6\n        min_free_slots: 1\n        '))
    assert 6 == plugin._total_slots


def test_automation_min_free_slots(console):
    plugin = plugin_maker_ini(console, dedent('\n        [automation]\n        enabled: yes\n        total_slots: 6\n        min_free_slots: 3\n        '))
    assert 3 == plugin._min_free_slots


def test_automation_min_free_slots_junk(console):
    plugin = plugin_maker_ini(console, dedent('\n        [automation]\n        enabled: yes\n        total_slots: 6\n        min_free_slots: f00\n        '))
    assert None is plugin._automation_enabled
    return


def test_automation_min_free_slots_negative(console):
    plugin = plugin_maker_ini(console, dedent('\n        [automation]\n        enabled: yes\n        total_slots: 6\n        min_free_slots: -5\n        '))
    assert None is plugin._automation_enabled
    return


def test_automation_min_free_slots_higher_than_total_slots(console):
    plugin = plugin_maker_ini(console, dedent('\n        [automation]\n        enabled: yes\n        total_slots: 6\n        min_free_slots: 7\n        '))
    assert None is plugin._automation_enabled
    return


def test_automation_total_slots_cannot_be_less_than_2(console):
    plugin = plugin_maker_ini(console, dedent('\n        [automation]\n        enabled: yes\n        total_slots: 1\n        min_free_slots: 1\n        '))
    assert None is plugin._automation_enabled
    return


def test_retain_free_duration(console):
    plugin = plugin_maker_ini(console, dedent('\n        [global_settings]\n        retain_free_duration: 20\n        '))
    assert 20 == plugin._retain_free_duration


def test_retain_free_duration_junk(console):
    plugin = plugin_maker_ini(console, dedent('\n        [global_settings]\n        retain_free_duration: f00\n        '))
    assert 0 is plugin._retain_free_duration


def test_retain_free_duration_negative(console):
    plugin = plugin_maker_ini(console, dedent('\n        [global_settings]\n        retain_free_duration: -5\n        '))
    assert 0 is plugin._retain_free_duration


def test_retain_free_duration_zero(console):
    plugin = plugin_maker_ini(console, dedent('\n        [global_settings]\n        retain_free_duration: 0\n        '))
    assert 0 is plugin._retain_free_duration


def test_retain_free_duration_too_high(console):
    plugin = plugin_maker_ini(console, dedent('\n        [global_settings]\n        retain_free_duration: 40\n        '))
    assert 30 == plugin._retain_free_duration