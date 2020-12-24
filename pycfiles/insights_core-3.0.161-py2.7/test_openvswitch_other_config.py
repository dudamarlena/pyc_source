# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_openvswitch_other_config.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.openvswitch_other_config import OpenvSwitchOtherConfig
from insights.tests import context_wrap
other_config_1 = ('\n{dpdk-init="true", dpdk-lcore-mask="30000003000", dpdk-socket-mem="4096,4096", pmd-cpu-mask="30000003000"}\n').strip()
other_config_2 = ('\n{dpdk-init="true", dpdk-lcore-mask="c00000c00", dpdk-socket-mem="4096,4096", pmd-cpu-mask="c00000c00"}\n').strip()
other_config_3 = ('\n{}\n').strip()
other_config_4 = ('\n{pmd-cpu-mask="3000000000030030030"}\n').strip()
other_config_5 = ('\novs-vsctl: unix:/var/run/openvswitch/db.sock: database connection failed (Permission denied)\n').strip()

def test_openvswitch_():
    result = OpenvSwitchOtherConfig(context_wrap(other_config_1))
    assert 'pmd-cpu-mask' in result
    assert result.get('dpdk-init') == 'true'
    assert result.get('dpdk-socket-mem') == '4096,4096'
    assert result.get('pmd-cpu-mask') == '30000003000'
    assert result.get('dpdk-lcore-mask') == '30000003000'
    assert result['dpdk-lcore-mask'] == '30000003000'
    result = OpenvSwitchOtherConfig(context_wrap(other_config_2))
    assert result.get('dpdk-init') == 'true'
    assert result.get('dpdk-socket-mem') == '4096,4096'
    assert result.get('pmd-cpu-mask') == 'c00000c00'
    result = OpenvSwitchOtherConfig(context_wrap(other_config_3))
    assert result.get('dpdk-init') is None
    result = OpenvSwitchOtherConfig(context_wrap(other_config_4))
    assert result.get('dpdk-init') is None
    assert result.get('pmd-cpu-mask') == '3000000000030030030'
    result = OpenvSwitchOtherConfig(context_wrap(other_config_5))
    assert result.get('dpdk-init') is None
    return