# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ovs_vsctl_show.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.ovs_vsctl_show import OVSvsctlshow
from insights.tests import context_wrap
ovs_vsctl_show_output = ('\ne4d4f521-086d-4479-a88f-d531cd1646b8\n    Bridge br-ex\n        Port br-ex\n            Interface br-ex\n                type: internal\n        Port "qg-dacc6089-be"\n            Interface "qg-dacc6089-be"\n                type: internal\n        Port "eth0"\n            Interface "eth0"\n        Port phy-br-ex\n            Interface phy-br-ex\n                type: patch\n                options: {peer=int-br-ex}\n    Bridge br-int\n        fail_mode: secure\n        Port "tapfcce898c-ca"\n            tag: 1\n            Interface "tapfcce898c-ca"\n                type: internal\n        Port int-br-ex\n            Interface int-br-ex\n                type: patch\n                options: {peer=phy-br-ex}\n        Port "tapdf2d6113-b2"\n            tag: 2\n            Interface "tapdf2d6113-b2"\n                type: internal\n        Port patch-tun\n            Interface patch-tun\n                type: patch\n                options: {peer=patch-int}\n        Port br-int\n            Interface br-int\n                type: internal\n        Port "ha-1f423581-cd"\n            tag: 3\n            Interface "ha-1f423581-cd"\n                type: internal\n        Port "qr-417e232b-dd"\n            tag: 1\n            Interface "qr-417e232b-dd"\n                type: internal\n    Bridge br-tun\n        fail_mode: secure\n        Port "vxlan-aca80118"\n            Interface "vxlan-aca80118"\n                type: vxlan\n                options: {df_default="true", in_key=flow, local_ip="172.168.1.26", out_key=flow, remote_ip="172.168.1.24"}\n        Port "vxlan-aca80119"\n            Interface "vxlan-aca80119"\n                type: vxlan\n                options: {df_default="true", in_key=flow, local_ip="172.168.1.26", out_key=flow, remote_ip="172.168.1.25"}\n        Port "vxlan-aca80117"\n            Interface "vxlan-aca80117"\n                type: vxlan\n                options: {df_default="true", in_key=flow, local_ip="172.168.1.26", out_key=flow, remote_ip="172.168.1.23"}\n        Port patch-int\n            Interface patch-int\n                type: patch\n                options: {peer=patch-tun}\n        Port "vxlan-aca80116"\n            Interface "vxlan-aca80116"\n                type: vxlan\n                options: {df_default="true", in_key=flow, local_ip="172.168.1.26", out_key=flow, remote_ip="172.168.1.22"}\n        Port br-tun\n            Interface br-tun\n                type: internal\n    ovs_version: "2.3.2"\n').strip()
ovs_vsctl_show_missing_lines = '\ne4d4f521-086d-4479-a88f-d531cd1646b8\n    Bridge br-ex\n'

def test_ovs_vsctl_show():
    ovs_ctl_cls = OVSvsctlshow(context_wrap(ovs_vsctl_show_output))
    assert ovs_ctl_cls.get_ovs_version() == '2.3.2'
    assert ovs_ctl_cls.get_bridge('br-int').get('fail_mode') == 'secure'
    br_tun = ovs_ctl_cls.get_bridge('br-tun')
    assert br_tun.get('fail_mode') == 'secure'
    assert len(br_tun.get('ports')) == 6
    ports = br_tun.get('ports')
    assert ports[0].get('interface') == 'vxlan-aca80118'
    assert ports[0].get('type') == 'vxlan'
    options = ports[0].get('options')
    assert options.get('df_default') == 'true'
    assert options.get('local_ip') == '172.168.1.26'
    assert options.get('out_key') == 'flow'
    bad = OVSvsctlshow(context_wrap(ovs_vsctl_show_missing_lines))
    assert not hasattr(bad, 'data')