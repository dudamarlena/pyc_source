# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_origin_local_volumes_pods.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import ls_origin_local_volumes_pods
from insights.parsers.ls_origin_local_volumes_pods import LsOriginLocalVolumePods
from insights.tests import context_wrap
LS_ORIGIN_LOCAL_VOLUME_PODS = ('\ntotal 0\ndrwxr-x---. 5 root root 71 Oct 18 23:20 5946c1f644096161a1242b3de0ee5875\ndrwxr-x---. 5 root root 71 Oct 18 23:24 6ea3d5cd-d34e-11e8-a142-001a4a160152\ndrwxr-x---. 5 root root 71 Oct 18 23:31 77d6d959-d34f-11e8-a142-001a4a160152\ndrwxr-x---. 5 root root 71 Oct 18 23:24 7ad952a0-d34e-11e8-a142-001a4a160152\ndrwxr-x---. 5 root root 71 Oct 18 23:24 7b63e8aa-d34e-11e8-a142-001a4a160152\n').strip()

def test_ls_origin_local_volumes_pods():
    ls_origin_local_volumes_pods = LsOriginLocalVolumePods(context_wrap(LS_ORIGIN_LOCAL_VOLUME_PODS, path='insights_commands/ls_-l_.var.lib.origin.openshift.local.volumes.pods'))
    assert len(ls_origin_local_volumes_pods.pods) == 5
    assert ls_origin_local_volumes_pods.pods == [
     '5946c1f644096161a1242b3de0ee5875', '6ea3d5cd-d34e-11e8-a142-001a4a160152',
     '77d6d959-d34f-11e8-a142-001a4a160152', '7ad952a0-d34e-11e8-a142-001a4a160152',
     '7b63e8aa-d34e-11e8-a142-001a4a160152']


def test_ls_origin_local_volumes_pods_doc_examples():
    env = {'ls_origin_local_volumes_pods': LsOriginLocalVolumePods(context_wrap(LS_ORIGIN_LOCAL_VOLUME_PODS, path='insights_commands/ls_-l_.var.lib.origin.openshift.local.volumes.pods'))}
    failed, total = doctest.testmod(ls_origin_local_volumes_pods, globs=env)
    assert failed == 0