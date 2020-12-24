# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_cluster_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.cluster_conf import ClusterConf
from insights.tests import context_wrap
CLUSTER_CONF_INFO = '\n<cluster name="mycluster" config_version="3">\n   <clusternodes>\n     <clusternode name="node-01.example.com" nodeid="1">\n         <fence>\n            <method name="APC">\n                <device name="apc" port="1"/>\n             </method>\n            <method name="SAN">\n                <device name="sanswitch1" port="12" action="on"/>\n                <device name="sanswitch2" port="12" action="on"/>\n            </method>\n         </fence>\n     </clusternode>\n     <clusternode name="node-02.example.com" nodeid="2">\n         <fence>\n            <method name="APC">\n              <device name="apc" port="2"/>\n            </method>\n            <method name="SAN">\n                <device name="sanswitch1" port="12"/>\n            </method>\n         </fence>\n     </clusternode>\n    </clusternodes>\n    <cman expected_votes="3"/>\n    <fencedevices>\n        <fencedevice agent="fence_imm" ipaddr="192.0.2.1" login="opmgr" name="fence1" passwd="***"/>\n        <fencedevice agent="fence_imm" ipaddr="192.0.2.2" login="opmgr" name="fence2" passwd="***"/>\n    </fencedevices>\n   <rm>\n    <resources>\n       <lvm name="lvm" vg_name="shared_vg" lv_name="ha-lv"/>\n       <fs name="FS" device="/dev/shared_vg/ha-lv" force_fsck="0" force_unmount="1" fsid="64050" fstype="ext4" mountpoint="/mnt" options="" self_fence="0"/>\n    </resources>\n   </rm>\n</cluster>\n'

def test_cluster_conf():
    conf = ClusterConf(context_wrap(CLUSTER_CONF_INFO))
    assert any('clusternode' in line for line in conf.lines)