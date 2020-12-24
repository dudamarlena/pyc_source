# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/query/tests/test_where.py
# Compiled at: 2019-10-28 13:56:59
# Size of source mod 2**32: 3157 bytes
import json
from parsr.query import from_dict, child_query as q
DATA = json.loads('\n{\n  "kind": "ClusterVersion",\n  "apiVersion": "config.openshift.io/v1",\n  "metadata": {\n    "name": "version",\n    "selfLink": "/apis/config.openshift.io/v1/clusterversions/version",\n    "uid": "11111111-2222-3333-4444-555555555555",\n    "resourceVersion": "1",\n    "generation": 1,\n    "creationTimestamp": "2019-08-04T23:16:46Z"\n  },\n  "spec": {\n    "clusterID": "55555555-4444-3333-2222-111111111111",\n    "upstream": "xxxxx://xxx.xxxxxxxxx.xxx/xxx/xxxxxxxxxxxxx/xx/xxxxx",\n    "channel": "stable-4.2"\n  },\n  "status": {\n    "desired": {\n      "version": "4.2.0-0.ci-2019-08-04-183142",\n      "image": "registry.svc.ci.openshift.org/ocp/release@sha256:63b65452005d6e9e45bb92a7505524db0e406c3281d91bdc1a4f5c5cf71b01c5",\n      "force": false\n    },\n    "history": [\n      {\n        "state": "Completed",\n        "startedTime": "2019-08-04T23:17:08Z",\n        "completionTime": "2019-08-04T23:32:14Z",\n        "version": "4.2.0-0.ci-2019-08-04-183142",\n        "image": "registry.svc.ci.openshift.org/ocp/release@sha256:63b65452005d6e9e45bb92a7505524db0e406c3281d91bdc1a4f5c5cf71b01c5",\n        "verified": false\n      }\n    ],\n    "observedGeneration": 1,\n    "versionHash": "############",\n    "conditions": [\n      {\n        "type": "Available",\n        "status": "True",\n        "lastTransitionTime": "2019-08-04T23:32:14Z",\n        "message": "Done applying 4.2.0-0.ci-2019-08-04-183142"\n      },\n      {\n        "type": "Failing",\n        "status": "True",\n        "lastTransitionTime": "2019-08-05T15:04:39Z",\n        "reason": "ClusterOperatorNotAvailable",\n        "message": "Cluster operator console is still updating"\n      },\n      {\n        "type": "Progressing",\n        "status": "False",\n        "lastTransitionTime": "2019-08-04T23:32:14Z",\n        "reason": "ClusterOperatorNotAvailable",\n        "message": "Error while reconciling 4.2.0-0.ci-2019-08-04-183142: the cluster operator console has not yet successfully rolled out"\n      },\n      {\n        "type": "RetrievedUpdates",\n        "status": "False",\n        "lastTransitionTime": "2019-08-04T23:17:08Z",\n        "reason": "RemoteFailed",\n        "message": "Unable to retrieve available updates: currently installed version 4.2.0-0.ci-2019-08-04-183142 not found in the stable-4.2 channel"\n      }\n    ],\n    "availableUpdates": null\n  }\n}\n')
d = from_dict(DATA)

def test_values():
    assert d.status.conditions.status.values == ['True', 'True', 'False', 'False']


def test_where():
    if not len(d.status.conditions.where('type', 'Progressing')) == 1:
        raise AssertionError
    else:
        res = d.status.conditions.where(q('type', 'Progressing') | q('status', 'True'))
        assert len(res) == 3
        assert res.reason.values == ['ClusterOperatorNotAvailable', 'ClusterOperatorNotAvailable']


def test_where_lambda():
    if not bool(d.status.conditions.where(lambda n: n.type.value == 'Progressing')):
        raise AssertionError
    else:
        assert bool(d.status.where(lambda n: len(n.conditions) > 3))
        assert not bool(d.status.where(lambda n: len(n.conditions) > 9))