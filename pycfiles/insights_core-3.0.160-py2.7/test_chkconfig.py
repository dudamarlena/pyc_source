# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_chkconfig.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from ...tests import context_wrap
from ..chkconfig import ChkConfig
SERVICES = ('\nauditd         \t0:off\t1:off\t2:on\t3:on\t4:on\t5:on\t6:off\ncrond          \t0:off\t1:off\t2:on\t3:on\t4:on\t5:on\t6:off\niptables       \t0:off\t1:off\t2:on\t3:on\t4:on\t5:on\t6:off\nkdump          \t0:off\t1:off\t2:off\t3:on\t4:on\t5:on\t6:off\nrestorecond    \t0:off\t1:off\t2:off\t3:off\t4:off\t5:off\t6:off\nxinetd          0:off   1:off   2:on    3:on    4:on    5:on    6:off\n        rexec:          off\n        rlogin:         off\n        rsh:            on\n        tcpmux-server:  off\n        telnet:         on\n').strip()
RHEL_73_SERVICES = "\nNote: This output shows SysV services only and does not include native\n      systemd services. SysV configuration data might be overridden by native\n      systemd configuration.\n\n      If you want to list systemd services use 'systemctl list-unit-files'.\n      To see services enabled on particular target use\n      'systemctl list-dependencies [target]'.\n\nnetconsole     \t0:off\t1:off\t2:off\t3:off\t4:off\t5:off\t6:off\nnetwork        \t0:off\t1:off\t2:on\t3:on\t4:on\t5:on\t6:off\nrhnsd          \t0:off\t1:off\t2:on\t3:on\t4:on\t5:on\t6:off\n\nxinetd based services:\n        chargen-dgram:  off\n        chargen-stream: off\n        daytime-dgram:  off\n        daytime-stream: off\n        discard-dgram:  off\n        discard-stream: off\n        echo-dgram:     off\n        echo-stream:    off\n        rsync:          on\n        tcpmux-server:  off\n        time-dgram:     off\n        time-stream:    off\n"

def test_chkconfig():
    context = context_wrap(SERVICES)
    chkconfig = ChkConfig(context)
    assert len(chkconfig.services) == 11
    assert len(chkconfig.parsed_lines) == 11
    assert chkconfig.is_on('crond')
    assert chkconfig.is_on('kdump')
    assert chkconfig.is_on('telnet')
    assert not chkconfig.is_on('restorecond')
    assert not chkconfig.is_on('rlogin')


def test_levels_on():
    chkconfig = ChkConfig(context_wrap(SERVICES))
    assert chkconfig.levels_on('crond') == set(['2', '3', '4', '5'])
    assert chkconfig.levels_on('telnet') == set(['2', '3', '4', '5'])
    assert chkconfig.levels_on('rlogin') == set([])
    with pytest.raises(KeyError):
        assert chkconfig.levels_on('bad_name')


def test_levels_off():
    chkconfig = ChkConfig(context_wrap(SERVICES))
    assert chkconfig.levels_off('crond') == set(['0', '1', '6'])
    assert chkconfig.levels_off('telnet') == set(['0', '1', '6'])
    assert chkconfig.levels_off('rlogin') == set(['0', '1', '2', '3',
     '4', '5', '6'])
    with pytest.raises(KeyError):
        assert chkconfig.levels_off('bad_name')


def test_rhel_73():
    chkconfig = ChkConfig(context_wrap(RHEL_73_SERVICES))
    assert sorted(chkconfig.level_states.keys()) == sorted([
     'netconsole', 'network', 'rhnsd', 'chargen-dgram', 'chargen-stream',
     'daytime-dgram', 'daytime-stream', 'discard-dgram', 'discard-stream',
     'echo-dgram', 'echo-stream', 'rsync', 'tcpmux-server', 'time-dgram',
     'time-stream'])
    assert chkconfig.levels_off('netconsole') == set(['0', '1', '2', '3', '4', '5', '6'])
    assert chkconfig.levels_on('network') == set(['2', '3', '4', '5'])
    assert chkconfig.levels_on('rsync') == set(['0', '1', '2', '3', '4', '5', '6'])