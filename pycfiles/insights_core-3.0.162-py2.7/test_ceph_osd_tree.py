# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_ceph_osd_tree.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.ceph_osd_tree_text import CephOsdTreeText
from insights.parsers.ceph_insights import CephInsights
from insights.parsers.ceph_cmd_json_parsing import CephOsdTree as CephOsdTreeParser
from insights.combiners import ceph_osd_tree
from insights.combiners.ceph_osd_tree import CephOsdTree
from insights.tests import context_wrap
import doctest
CEPH_INSIGHTS = ('\n{\n  "osd_tree": {\n    "nodes": [\n      {\n        "children": [\n          -3\n        ],\n        "type_id": 10,\n        "type": "root",\n        "id": -1,\n        "name": "default"\n      },\n      {\n        "name": "daq",\n        "type_id": 1,\n        "id": -3,\n        "pool_weights": {},\n        "type": "host",\n        "children": [\n          2,\n          1,\n          0\n        ]\n      },\n      {\n        "status": "up",\n        "name": "osd.0",\n        "exists": 1,\n        "type_id": 0,\n        "reweight": 1.0,\n        "crush_weight": 0.009796142578125,\n        "pool_weights": {},\n        "primary_affinity": 1.0,\n        "depth": 2,\n        "device_class": "ssd",\n        "type": "osd",\n        "id": 0\n      },\n      {\n        "status": "up",\n        "name": "osd.1",\n        "exists": 1,\n        "type_id": 0,\n        "reweight": 1.0,\n        "crush_weight": 0.009796142578125,\n        "pool_weights": {},\n        "primary_affinity": 1.0,\n        "depth": 2,\n        "device_class": "ssd",\n        "type": "osd",\n        "id": 1\n      },\n      {\n        "status": "up",\n        "name": "osd.2",\n        "exists": 1,\n        "type_id": 0,\n        "reweight": 1.0,\n        "crush_weight": 0.009796142578125,\n        "pool_weights": {},\n        "primary_affinity": 1.0,\n        "depth": 2,\n        "device_class": "ssd",\n        "type": "osd",\n        "id": 2\n      }\n    ],\n    "stray": []\n  },\n  "osd_metadata": {\n    "1": {\n      "bluefs_db_size": "67108864",\n      "bluestore_bdev_size": "10737418240",\n      "bluestore_bdev_driver": "KernelDevice"\n    }\n  },\n  "version": {\n    "release": 14,\n    "major": 0,\n    "full": "ceph version 14.0.0-3517-g5322f99370 (5322f99370d629f6927b9c948522a003fc5da5bb) nautilus (dev)",\n    "minor": 0\n  }\n}\n').strip()
CEPH_OSD_TREE_TEXT = ('\nID CLASS WEIGHT  TYPE NAME       STATUS REWEIGHT PRI-AFF\n-1       0.08752 root default\n-9       0.02917     host ceph1\n 2   hdd 0.01459         osd.2       up  1.00000 1.00000\n 5   hdd 0.01459         osd.5       up  1.00000 1.00000\n-5       0.02917     host ceph2\n 1   hdd 0.01459         osd.1       up  1.00000 1.00000\n 4   hdd 0.01459         osd.4       up  1.00000 1.00000\n-3       0.02917     host ceph3\n 0   hdd 0.01459         osd.0       up  1.00000 1.00000\n 3   hdd 0.01459         osd.3       up  1.00000 1.00000\n-7             0     host ceph_1\n').strip()
CEPH_OSD_TREE = ('\n{\n    "nodes": [\n        {\n            "id": -1,\n            "name": "default",\n            "type": "root",\n            "type_id": 10,\n            "children": [\n                -7,\n                -3,\n                -5,\n                -9\n            ]\n        },\n        {\n            "id": -9,\n            "name": "ceph1",\n            "type": "host",\n            "type_id": 1,\n            "pool_weights": {},\n            "children": [\n                5,\n                2\n            ]\n        },\n        {\n            "id": 2,\n            "device_class": "hdd",\n            "name": "osd.2",\n            "type": "osd",\n            "type_id": 0,\n            "crush_weight": 0.014587,\n            "depth": 2,\n            "pool_weights": {},\n            "exists": 1,\n            "status": "up",\n            "reweight": 1.000000,\n            "primary_affinity": 1.000000\n        },\n        {\n            "id": 5,\n            "device_class": "hdd",\n            "name": "osd.5",\n            "type": "osd",\n            "type_id": 0,\n            "crush_weight": 0.014587,\n            "depth": 2,\n            "pool_weights": {},\n            "exists": 1,\n            "status": "up",\n            "reweight": 1.000000,\n            "primary_affinity": 1.000000\n        },\n        {\n            "id": -5,\n            "name": "ceph2",\n            "type": "host",\n            "type_id": 1,\n            "pool_weights": {},\n            "children": [\n                4,\n                1\n            ]\n        },\n        {\n            "id": 1,\n            "device_class": "hdd",\n            "name": "osd.1",\n            "type": "osd",\n            "type_id": 0,\n            "crush_weight": 0.014587,\n            "depth": 2,\n            "pool_weights": {},\n            "exists": 1,\n            "status": "up",\n            "reweight": 1.000000,\n            "primary_affinity": 1.000000\n        },\n        {\n            "id": 4,\n            "device_class": "hdd",\n            "name": "osd.4",\n            "type": "osd",\n            "type_id": 0,\n            "crush_weight": 0.014587,\n            "depth": 2,\n            "pool_weights": {},\n            "exists": 1,\n            "status": "up",\n            "reweight": 1.000000,\n            "primary_affinity": 1.000000\n        },\n        {\n            "id": -3,\n            "name": "ceph3",\n            "type": "host",\n            "type_id": 1,\n            "pool_weights": {},\n            "children": [\n                3,\n                0\n            ]\n        },\n        {\n            "id": 0,\n            "device_class": "hdd",\n            "name": "osd.0",\n            "type": "osd",\n            "type_id": 0,\n            "crush_weight": 0.014587,\n            "depth": 2,\n            "pool_weights": {},\n            "exists": 1,\n            "status": "up",\n            "reweight": 1.000000,\n            "primary_affinity": 1.000000\n        },\n        {\n            "id": 3,\n            "device_class": "hdd",\n            "name": "osd.3",\n            "type": "osd",\n            "type_id": 0,\n            "crush_weight": 0.014587,\n            "depth": 2,\n            "pool_weights": {},\n            "exists": 1,\n            "status": "up",\n            "reweight": 1.000000,\n            "primary_affinity": 1.000000\n        },\n        {\n            "id": -7,\n            "name": "ceph_1",\n            "type": "host",\n            "type_id": 1,\n            "pool_weights": {},\n            "children": []\n        }\n    ],\n    "stray": []\n}\n').strip()

def test_ceph_osd_tree_parser():
    cot = CephOsdTreeParser(context_wrap(CEPH_OSD_TREE))
    ci = CephInsights(context_wrap(CEPH_INSIGHTS))
    ret = CephOsdTree(cot, ci, None)
    assert ret['nodes'][0] == {'id': -1, 'name': 'default', 'type': 'root', 'type_id': 10, 'children': [-7, -3, -5, -9]}
    return


def test_ceph_osd_tree_parser_2():
    cot = CephOsdTreeParser(context_wrap(CEPH_OSD_TREE))
    ci = CephInsights(context_wrap(CEPH_INSIGHTS))
    cott = CephOsdTreeText(context_wrap(CEPH_OSD_TREE_TEXT))
    ret = CephOsdTree(cot, ci, cott)
    assert ret['nodes'][0] == {'id': -1, 'name': 'default', 'type': 'root', 'type_id': 10, 'children': [-7, -3, -5, -9]}


def test_ceph_insights():
    ci = CephInsights(context_wrap(CEPH_INSIGHTS))
    cott = CephOsdTreeText(context_wrap(CEPH_OSD_TREE_TEXT))
    ret = CephOsdTree(None, ci, cott)
    assert ret['nodes'][0] == {'children': [-3], 'type_id': 10, 'type': 'root', 'id': -1, 'name': 'default'}
    return


def test_ceph_osd_tree_text():
    cott = CephOsdTreeText(context_wrap(CEPH_OSD_TREE_TEXT))
    ret = CephOsdTree(None, None, cott)
    assert ret['nodes'][0] == {'id': '-1', 'device_class': '', 'crush_weight': '0.08752', 'name': 'default', 'status': '', 
       'reweight': '', 'primary_affinity': '', 'type': 'root', 'children': [
                  -7, -3, -5, -9]}
    return


def test_ceph_osd_tree_doc_examples():
    env = {'cot': CephOsdTree(None, None, CephOsdTreeText(context_wrap(CEPH_OSD_TREE_TEXT)))}
    failed, total = doctest.testmod(ceph_osd_tree, globs=env)
    assert failed == 0
    return