# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_getsebool.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.parsers import getsebool, SkipException
from insights.tests import context_wrap
GETSEBOOL = ('\nvarnishd_connect_any --> off\nvirt_read_qemu_ga_data --> off\nvirt_rw_qemu_ga_data --> off\nvirt_sandbox_use_all_caps --> on\nvirt_sandbox_use_audit --> on\nvirt_sandbox_use_fusefs --> off\nvirt_sandbox_use_mknod --> off\nvirt_sandbox_use_netlink --> off\nvirt_sandbox_use_sys_admin --> off\nvirt_transition_userdomain --> off\nvirt_use_comm --> off\nvirt_use_execmem --> off\nvirt_use_fusefs --> off\nvirt_use_glusterd --> off\nvirt_use_nfs --> on\nvirt_use_rawip --> off\nvirt_use_samba --> off\nvirt_use_sanlock --> off\nvirt_use_usb --> on\nvirt_use_xserver --> off\n').strip()
SELINUX_DISABLED = '/usr/sbin/getsebool:  SELinux is disabled'

def test_getsebool():
    result = getsebool.Getsebool(context_wrap(GETSEBOOL))
    assert result['varnishd_connect_any'] == 'off'
    assert result['virt_use_nfs'] == 'on'
    assert 'virt_use_xserver' in result
    assert 'not_exist_key' not in result


def test_getsebool_disabled():
    with pytest.raises(SkipException) as (excinfo):
        getsebool.Getsebool(context_wrap(SELINUX_DISABLED))
    assert 'SELinux is disabled' in str(excinfo.value)