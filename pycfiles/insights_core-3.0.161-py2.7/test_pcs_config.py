# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_pcs_config.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.pcs_config import PCSConfig
from insights.parsers import pcs_config
from insights.tests import context_wrap
import doctest
NORMAL_PCS_CONFIG = ('\nCluster Name: cluster-1\nCorosync Nodes:\n node-1 node-2\nPacemaker Nodes:\n node-1 node-2\n\nResources:\n Clone: clone-1\n  Meta Attrs: interleave=true ordered=true\n  Resource: res-1 (class=ocf provider=pacemaker type=controld)\n   Operations: start interval=0s timeout=90 (dlm-start-interval-0s)\n               stop interval=0s timeout=100 (dlm-stop-interval-0s)\n               monitor interval=30s on-fail=fence (dlm-monitor-interval-30s)\n Clone: clone-2\n  Meta Attrs: interleave=true ordered=true\n  Resource: res-2 (class=ocf provider=pacemaker type=controld)\n   Operations: start interval=0s timeout=90 (dlm-start-interval-0s)\n               stop interval=0s timeout=100 (dlm-stop-interval-0s)\n               monitor interval=30s on-fail=fence (dlm-monitor-interval-30s)\n Group: grp-1\n  Resource: res-1 (class=ocf provider=heartbeat type=IPaddr2)\n   Attributes: ip=10.0.0.1 cidr_netmask=32\n   Operations: monitor interval=120s (ip_monitor-interval-120s)\n               start interval=0s timeout=20s (ip_-start-interval-0s)\n               stop interval=0s timeout=20s (ip_-stop-interval-0s)\n  Resource: res-2 (class=ocf provider=heartbeat type=Filesystem)\n   Attributes: device=/dev/lv_exzpr directory= fstype=xfs run_fsck=yes fast_stop=yes\n   Operations: start interval=0s timeout=60 (fs_exzpr-start-interval-0s)\n               stop interval=0s timeout=60 (fs_exzpr-stop-interval-0s)\n               monitor interval=30s timeout=60 (fs_exzpr-monitor-interval-30s)\n\nStonith Devices:\nFencing Levels:\n\nLocation Constraints:\n  Resource: fence-1\n    Disabled on: res-mgt (score:-INFINITY) (id:location-fence-1--INFINITY)\n  Resource: res-1\n    Enabled on: res-mcast (score:INFINITY) (role: Started) (id:cli-prefer-res)\nOrdering Constraints:\n  start clone-1 then start clone-x (kind:Mandatory) (id:clone-mandatory)\n  start clone-2 then start clone-y (kind:Mandatory) (id:clone-mandatory)\nColocation Constraints:\n  clone-1 with clone-x (score:INFINITY) (id:clone-INFINITY)\n  clone-2 with clone-x (score:INFINITY) (id:clone-INFINITY)\n\nResources Defaults:\n resource-stickiness: 100\n migration-threshold: 3\nOperations Defaults:\n No defaults set\n\nCluster Properties:\n cluster-infrastructure: corosync\n cluster-name: cluster-1\n dc-version: 1.1.13-10.el7_2.4-44eb2dd\n have-watchdog: false\n no-quorum-policy: ignore\n stonith-enable: true\n stonith-enabled: false\n').strip()

def test_pcs_config_basic():
    pcs = PCSConfig(context_wrap(NORMAL_PCS_CONFIG))
    assert pcs.get('Cluster Name') == 'cluster-1'
    assert pcs.get('Corosync Nodes') == ['node-1', 'node-2']
    assert pcs.get('Pacemaker Nodes') == ['node-1', 'node-2']
    assert pcs.get('Unknown Key') is None
    return


def test_pcs_config_normal():
    pcs = PCSConfig(context_wrap(NORMAL_PCS_CONFIG))
    assert 'cluster-infrastructure: corosync' in pcs.get('Cluster Properties')
    assert 'stonith-enabled: false' in pcs.get('Cluster Properties')
    assert pcs.get('Resources Defaults') == ['resource-stickiness: 100', 'migration-threshold: 3']
    assert 'cluster-infrastructure' in pcs.cluster_properties
    assert 'have-watchdog' in pcs.cluster_properties
    assert pcs.cluster_properties.get('have-watchdog') == 'false'


def test_pcs_config_documentation():
    env = {'pcs_config': PCSConfig(context_wrap(NORMAL_PCS_CONFIG))}
    failed, total = doctest.testmod(pcs_config, globs=env)
    assert failed == 0