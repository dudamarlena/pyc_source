# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ip_netns_exec_namespace_lsof.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import SkipException
from insights.parsers import ip_netns_exec_namespace_lsof
from insights.parsers.ip_netns_exec_namespace_lsof import IpNetnsExecNamespaceLsofI
from insights.tests import context_wrap
import doctest, pytest
IP_NETNS_EXEC_NAMESPACE_LSOF_I = ('\nCOMMAND   PID   USER    FD  TYPE  DEVICE     SIZE/OFF  NODE NAME\nneutron-n 975   root    5u  IPv4  6482691    0t0        TCP *:http (LISTEN)\n').strip()
EXCEPTION1 = ('\n').strip()
EXCEPTION2 = ('\nCOMMAND     PID   USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME\n').strip()

def test_ip_netns_exec_namespace_lsof():
    data = IpNetnsExecNamespaceLsofI(context_wrap(IP_NETNS_EXEC_NAMESPACE_LSOF_I))
    assert len(data.search(node='TCP')) == 1
    assert len(data.search(command='neutron-n')) == 1
    assert len(data.search(user='nobody')) == 0
    assert data.data[0]['command'] == 'neutron-n'
    assert data.data[0].get('node') == 'TCP'
    assert [ ps[2] for ps in data ] == ['root']


def test_ip_netns_exec_namespace_lsof_documentation():
    env = {'ns_lsof': IpNetnsExecNamespaceLsofI(context_wrap(IP_NETNS_EXEC_NAMESPACE_LSOF_I))}
    failed, total = doctest.testmod(ip_netns_exec_namespace_lsof, globs=env)
    assert failed == 0


def test_ip_netns_exec_namespace_lsof_exception1():
    with pytest.raises(SkipException) as (e):
        IpNetnsExecNamespaceLsofI(context_wrap(EXCEPTION1))
    assert 'Empty file' in str(e)


def test_ip_netns_exec_namespace_lsof_exception2():
    with pytest.raises(SkipException) as (e):
        IpNetnsExecNamespaceLsofI(context_wrap(EXCEPTION2))
    assert 'Useless data' in str(e)