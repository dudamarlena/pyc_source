# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_services.py
# Compiled at: 2019-05-16 13:41:33
from ...parsers.chkconfig import ChkConfig
from ...parsers.systemd.unitfiles import UnitFiles
from ..services import Services
from ...tests import context_wrap
CHKCONIFG = ('\nauditd         \t0:off\t1:off\t2:on\t3:on\t4:on\t5:on\t6:off\ncrond          \t0:off\t1:off\t2:on\t3:on\t4:on\t5:on\t6:off\niptables       \t0:off\t1:off\t2:on\t3:on\t4:on\t5:on\t6:off\nkdump          \t0:off\t1:off\t2:off\t3:on\t4:on\t5:on\t6:off\nrestorecond    \t0:off\t1:off\t2:off\t3:off\t4:off\t5:off\t6:off\n').strip()
SYSTEMCTL = ('\nUNIT FILE                                   STATE\nauditd.service                              enabled\ncpupower.service                            disabled\ncrond.service                               enabled\nemergency.service                           static\nfirewalld.service                           enabled\nfstrim.service                              static\nkdump.service                               enabled\n\n7 unit files listed.\n').strip()

def test_chkconfig():
    context = context_wrap(CHKCONIFG)
    chkconfig = ChkConfig(context)
    services = Services(chkconfig, None)
    assert len(services.services) == 5
    assert len(services.parsed_lines) == 5
    assert services.is_on('auditd')
    assert services.is_on('crond')
    assert not services.is_on('restorecond')
    assert not services.is_on('ksm')
    assert services.service_line('auditd') == 'auditd         \t0:off\t1:off\t2:on\t3:on\t4:on\t5:on\t6:off'
    assert services.service_line('ksm') == ''
    assert 'crond' in services
    assert 'ksm' not in services
    return


def test_systemctl():
    context = context_wrap(SYSTEMCTL)
    unitfiles = UnitFiles(context)
    services = Services(None, unitfiles)
    assert len(services.services) == 7
    assert len(services.parsed_lines) == 7
    assert services.is_on('auditd.service')
    assert services.is_on('crond.service')
    assert not services.is_on('cpupower.service')
    assert services.is_on('auditd')
    assert services.is_on('crond')
    assert not services.is_on('cpupower')
    assert not services.is_on('ksm')
    assert not services.is_on('ksm.service')
    assert services.service_line('auditd.service') == 'auditd.service                              enabled'
    assert 'crond' in services
    assert 'ksm' not in services
    return


def test_combined():
    context = context_wrap(CHKCONIFG)
    chkconfig = ChkConfig(context)
    context = context_wrap(SYSTEMCTL)
    unitfiles = UnitFiles(context)
    services = Services(chkconfig, unitfiles)
    assert len(services.services) == 12
    assert len(services.parsed_lines) == 12
    assert services.is_on('auditd')
    assert services.is_on('crond')
    assert not services.is_on('restorecond')
    assert services.is_on('auditd.service')
    assert services.is_on('crond.service')
    assert not services.is_on('cpupower.service')
    assert not services.is_on('cpupower')
    assert 'crond' in services
    assert 'ksm' not in services