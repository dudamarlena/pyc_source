# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_network.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.sysconfig import NetworkSysconfig
from insights.tests import context_wrap
NETWORK_SYSCONFIG = ('\nNETWORKING=yes\nHOSTNAME=rhel7-box\nGATEWAY=172.31.0.1\nNM_BOND_VLAN_ENABLED=no\n').strip()

def test_sysconfig_network():
    result = NetworkSysconfig(context_wrap(NETWORK_SYSCONFIG))
    assert result['GATEWAY'] == '172.31.0.1'
    assert result.get('NETWORKING') == 'yes'
    assert result['NM_BOND_VLAN_ENABLED'] == 'no'