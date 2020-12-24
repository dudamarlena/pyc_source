# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ovs_vsctl_list_bridge.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import SkipException
from insights.parsers import ovs_vsctl_list_bridge
from insights.parsers.ovs_vsctl_list_bridge import OVSvsctlListBridge
from insights.tests import context_wrap
import doctest, pytest
OVS_VSCTL_LIST_BRIDGES_ALL = ('\n_uuid               : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx\nauto_attach         : []\ncontroller          : [xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx]\ndatapath_id         : "0000a61fd19ea54f"\ndatapath_type       : "enp0s9"\ndatapath_version    : "<unknown>"\nexternal_ids        : {a="0"}\nfail_mode           : secure\nflood_vlans         : [1000]\nflow_tables         : {1=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}\nipfix               : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx\nmcast_snooping_enable: false\nmirrors             : [xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx]\nname                : br-int\nnetflow             : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx\nother_config        : {disable-in-band="true", mac-table-size="2048"}\nports               : [xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx, 0000000-0000-0000-0000-0000000000000, 1111111-1111-1111-1111-1111111111111]\nprotocols           : ["OpenFlow11", "OpenFlow11", "OpenFlow12", "OpenFlow13"]\nrstp_enable         : true\nrstp_status         : {rstp_bridge_id="8.000.a61fd19ea54f",     rstp_bridge_port_id="0000", rstp_designated_id="8.000.a61fd19ea54f", rstp_designated_port_id="0000", rstp_root_id="8.000.a61fd19ea54f", rstp_root_path_cost="0"}\nsflow               : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx\nstatus              : {"0"="1"}\nstp_enable          : true\n\n_uuid               : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx\nauto_attach         : []\ncontroller          : []\ndatapath_id         : "0000d29e6a8acc4c"\ndatapath_type       : ""\ndatapath_version    : "<unknown>"\nexternal_ids        : {}\nfail_mode           : []\nflood_vlans         : []\nflow_tables         : {}\nipfix               : []\nmcast_snooping_enable: false\nmirrors             : []\nname                : br-tun\nnetflow             : []\nother_config        : {}\nports               : [xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx]\nprotocols           : []\nrstp_enable         : false\nrstp_status         : {}\nsflow               : []\nstatus              : {}\nstp_enable          : false\n').strip()
OVS_VSCTL_LIST_BRIDGES_FILTERED1 = ('\nname                : br-int\nother_config        : {disable-in-band="true", mac-table-size="2048"}\nname                : br-tun\nother_config        : {}\n').strip()
OVS_VSCTL_LIST_BRIDGES_FILTERED2 = ('\n_uuid               : xxxxxxxx-xxxx-xxxx-xxxxx-xxxxxxxxxxxx\nname                : br-int\nnetflow             : []\nother_config        : {disable-in-band="true", mac-table-size="2048"}\nstp_enable          : false\n_uuid               : aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa\nname                : br-tun\nnetflow             : []\nother_config        : {mac-table-size="4096"}\nstp_enable          : true\n').strip()
EXCEPTION1 = ('\n').strip()

def test_ovs_vsctl_list_bridge_documentation():
    env = {'bridge_lists': OVSvsctlListBridge(context_wrap(OVS_VSCTL_LIST_BRIDGES_FILTERED1))}
    failed, total = doctest.testmod(ovs_vsctl_list_bridge, globs=env)
    assert failed == 0


def test_ovs_vsctl_list_bridge_all():
    data = OVSvsctlListBridge(context_wrap(OVS_VSCTL_LIST_BRIDGES_ALL))
    assert data[0]['name'] == 'br-int'
    assert data[0]['external_ids'] == {'a': '0'}
    assert data[0]['flow_tables'] == {'1': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'}
    assert data[0].get('flood_vlans') == ['1000']
    assert data[0]['protocols'][(-1)] == 'OpenFlow13'
    assert data[0]['other_config']['mac-table-size'] == '2048'
    assert data[0]['rstp_status']['rstp_root_path_cost'] == '0'
    assert data[1]['name'] == 'br-tun'
    assert data[1]['mirrors'] == []
    assert data[1]['datapath_type'] == ''
    assert data[1]['status'] == {}
    assert data[1].get('stp_enable') == 'false'


def test_ovs_vsctl_list_bridge():
    data = OVSvsctlListBridge(context_wrap(OVS_VSCTL_LIST_BRIDGES_FILTERED2))
    assert data[0].get('name') == 'br-int'
    assert data[0]['other_config']['mac-table-size'] == '2048'
    assert data[1]['name'] == 'br-tun'


def test_ovs_vsctl_list_bridge_exception1():
    with pytest.raises(SkipException) as (e):
        OVSvsctlListBridge(context_wrap(EXCEPTION1))
    assert 'Empty file' in str(e)