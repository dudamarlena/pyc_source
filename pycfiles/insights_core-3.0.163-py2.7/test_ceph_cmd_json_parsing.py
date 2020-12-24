# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ceph_cmd_json_parsing.py
# Compiled at: 2019-11-14 13:57:46
import doctest, pytest
from insights.parsers import ceph_cmd_json_parsing, ParseException, SkipException
from insights.parsers.ceph_cmd_json_parsing import CephOsdDump, CephOsdDf, CephS, CephECProfileGet, CephCfgInfo, CephHealthDetail, CephDfDetail, CephOsdTree, CephReport
from insights.tests import context_wrap
CEPH_OSD_DUMP_INFO = ('\n{\n    "epoch": 210,\n    "fsid": "2734f9b5-2013-48c1-8e96-d31423444717",\n    "created": "2016-11-12 16:08:46.307206",\n    "modified": "2017-03-07 08:55:53.301911",\n    "flags": "sortbitwise",\n    "cluster_snapshot": "",\n    "pool_max": 12,\n    "max_osd": 8,\n    "pools": [\n        {\n            "pool": 0,\n            "pool_name": "rbd",\n            "flags": 1,\n            "flags_names": "hashpspool",\n            "type": 1,\n            "size": 3,\n            "min_size": 2,\n            "crush_ruleset": 0,\n            "object_hash": 2,\n            "pg_num": 256\n        }\n    ]\n}\n').strip()
CEPH_OSD_DF_INFO = ('\n{\n    "nodes": [\n        {\n            "id": 0,\n            "name": "osd.0",\n            "type": "osd",\n            "type_id": 0,\n            "crush_weight": 1.091095,\n            "depth": 2,\n            "reweight": 1.000000,\n            "kb": 1171539620,\n            "kb_used": 4048208,\n            "kb_avail": 1167491412,\n            "utilization": 0.345546,\n            "var": 1.189094,\n            "pgs": 945\n        }\n    ],\n    "stray": [],\n    "summary": {\n        "total_kb": 8200777340,\n        "total_kb_used": 23831128,\n        "total_kb_avail": 8176946212,\n        "average_utilization": 0.290596,\n        "min_var": 0.803396,\n        "max_var": 1.189094,\n        "dev": 0.035843\n    }\n}\n').strip()
CEPH_S_INFO = ('\n{\n    "health": {\n\n    },\n    "pgmap": {\n        "pgs_by_state": [\n            {\n                "state_name": "active+clean",\n                "count": 1800\n            }\n        ],\n        "version": 314179,\n        "num_pgs": 1800,\n        "data_bytes": 7943926574,\n        "bytes_used": 24405610496,\n        "bytes_avail": 8373190385664,\n        "bytes_total": 8397595996160\n    },\n    "fsmap": {\n        "epoch": 1,\n        "by_rank": []\n    }\n}\n').strip()
CEPH_DF_DETAIL_INFO = ('\n{\n    "stats": {\n        "total_bytes": 17113243648,\n        "total_used_bytes": 203120640,\n        "total_avail_bytes": 16910123008,\n        "total_objects": 0\n    },\n    "pools": [\n        {\n            "name": "rbd",\n            "id": 0,\n            "stats": {\n                "kb_used": 0,\n                "bytes_used": 0,\n                "max_avail": 999252180,\n                "objects": 0,\n                "dirty": 0,\n                "rd": 0,\n                "rd_bytes": 0,\n                "wr": 0,\n                "wr_bytes": 0,\n                "raw_bytes_used": 0\n            }\n        },\n        {\n            "name": "ecpool",\n            "id": 2,\n            "stats": {\n                "kb_used": 0,\n                "bytes_used": 0,\n                "max_avail": 1998504360,\n                "objects": 0,\n                "dirty": 0,\n                "rd": 0,\n                "rd_bytes": 0,\n                "wr": 0,\n                "wr_bytes": 0,\n                "raw_bytes_used": 0\n            }\n        }\n    ]\n}\n').strip()
CEPH_HEALTH_DETAIL_INFO = ('\n{\n    "health": {\n    },\n    "timechecks": {\n        "epoch": 4,\n        "round": 0,\n        "round_status": "finished"\n    },\n    "summary": [],\n    "overall_status": "HEALTH_OK",\n    "detail": []\n}\n').strip()
CEPH_OSD_EC_PROFILE_GET = ('\n{\n    "k": "2",\n    "m": "1",\n    "plugin": "jerasure",\n    "technique": "reed_sol_van"\n}\n').strip()
CEPHINFO = ('\n{\n    "name": "osd.1",\n    "cluster": "ceph",\n    "debug_none": "0\\/5",\n    "heartbeat_interval": "5",\n    "heartbeat_file": "",\n    "heartbeat_inject_failure": "0",\n    "perf": "true",\n    "max_open_files": "131072",\n    "ms_type": "simple",\n    "ms_tcp_nodelay": "true",\n    "ms_tcp_rcvbuf": "0",\n    "ms_tcp_prefetch_max_size": "4096",\n    "ms_initial_backoff": "0.2",\n    "ms_max_backoff": "15",\n    "ms_crc_data": "true",\n    "ms_crc_header": "true",\n    "ms_die_on_bad_msg": "false",\n    "ms_die_on_unhandled_msg": "false",\n    "ms_die_on_old_message": "false",\n    "ms_die_on_skipped_message": "false",\n    "ms_dispatch_throttle_bytes": "104857600",\n    "ms_bind_ipv6": "false",\n    "ms_bind_port_min": "6800",\n    "ms_bind_port_max": "7300",\n    "ms_bind_retry_count": "3",\n    "ms_bind_retry_delay": "5"\n}\n').strip()
CEPH_OSD_TREE = ('\n{\n    "nodes": [\n        {\n            "id": -1,\n            "name": "default",\n            "type": "root",\n            "type_id": 10,\n            "children": [\n                -5,\n                -4,\n                -3,\n                -2\n            ]\n        },\n        {\n            "id": -2,\n            "name": "dhcp-192-56",\n            "type": "host",\n            "type_id": 1,\n            "children": []\n        },\n        {\n            "id": -3,\n            "name": "dhcp-192-104",\n            "type": "host",\n            "type_id": 1,\n            "children": []\n        },\n        {\n            "id": -4,\n            "name": "dhcp-192-67",\n            "type": "host",\n            "type_id": 1,\n            "children": []\n        },\n        {\n            "id": -5,\n            "name": "localhost",\n            "type": "host",\n            "type_id": 1,\n            "children": [\n                1,\n                3,\n                5,\n                2,\n                4,\n                0\n            ]\n        },\n        {\n            "id": 0,\n            "name": "osd.0",\n            "type": "osd",\n            "type_id": 0,\n            "crush_weight": 0.002991,\n            "depth": 2,\n            "exists": 1,\n            "status": "up",\n            "reweight": 1.000000,\n            "primary_affinity": 1.000000\n        },\n        {\n            "id": 4,\n            "name": "osd.4",\n            "type": "osd",\n            "type_id": 0,\n            "crush_weight": 0.002991,\n            "depth": 2,\n            "exists": 1,\n            "status": "down",\n            "reweight": 1.000000,\n            "primary_affinity": 1.000000\n        },\n        {\n            "id": 2,\n            "name": "osd.2",\n            "type": "osd",\n            "type_id": 0,\n            "crush_weight": 0.002991,\n            "depth": 2,\n            "exists": 1,\n            "status": "up",\n            "reweight": 1.000000,\n            "primary_affinity": 1.000000\n        },\n        {\n            "id": 5,\n            "name": "osd.5",\n            "type": "osd",\n            "type_id": 0,\n            "crush_weight": 0.002991,\n            "depth": 2,\n            "exists": 1,\n            "status": "up",\n            "reweight": 1.000000,\n            "primary_affinity": 1.000000\n        },\n        {\n            "id": 3,\n            "name": "osd.3",\n            "type": "osd",\n            "type_id": 0,\n            "crush_weight": 0.002991,\n            "depth": 2,\n            "exists": 1,\n            "status": "up",\n            "reweight": 1.000000,\n            "primary_affinity": 1.000000\n        },\n        {\n            "id": 1,\n            "name": "osd.1",\n            "type": "osd",\n            "type_id": 0,\n            "crush_weight": 0.002991,\n            "depth": 2,\n            "exists": 1,\n            "status": "up",\n            "reweight": 1.000000,\n            "primary_affinity": 1.000000\n        }\n    ],\n    "stray": []\n}\n').strip()
CEPH_REPORT = ('\nreport 1188805303\n{\n    "cluster_fingerprint": "0d5f8f7a-0241-4a2e-8401-9dcf37a1039b",\n    "version": "12.2.8-52.el7cp",\n    "commit": "3af3ca15b68572a357593c261f95038d02f46201",\n    "timestamp": "2019-06-05 23:33:08.514032",\n    "tag": "",\n    "health": {\n        "checks": {\n            "POOL_APP_NOT_ENABLED": {\n                "severity": "HEALTH_WARN",\n                "summary": {\n                    "message": "application not enabled on 1 pool(s)"\n                },\n                "detail": [\n                    {\n                        "message": "application not enabled on pool \'pool-a\'"\n                    },\n                    {\n                        "message": "use \'ceph osd pool application enable <pool-name> <app-name>\', where <app-name> is \'cephfs\', \'rbd\', \'rgw\', or freeform for custom applications."\n                    }\n                ]\n            },\n            "MON_DOWN": {\n                "severity": "HEALTH_WARN",\n                "summary": {\n                    "message": "1/3 mons down, quorum ceph2,ceph_1"\n                },\n                "detail": [\n                    {\n                        "message": "mon.ceph3 (rank 0) addr 10.72.37.76:6789/0 is down (out of quorum)"\n                    }\n                ]\n            }\n        },\n        "status": "HEALTH_WARN",\n        "summary": [\n            {\n                "severity": "HEALTH_WARN",\n                "summary": "\'ceph health\' JSON format has changed in luminous. If you see this your monitoring system is scraping the wrong fields. Disable this with \'mon health preluminous compat warning = false\'"\n            }\n        ],\n        "overall_status": "HEALTH_WARN",\n        "detail": [\n            "\'ceph health\' JSON format has changed in luminous. If you see this your monitoring system is scraping the wrong fields. Disable this with \'mon health preluminous compat warning = false\'"\n        ]\n    },\n    "monmap_first_committed": 1,\n    "monmap_last_committed": 1,\n    "quorum": [\n        1,\n        2\n    ],\n    "osdmap_first_committed": 1,\n    "osdmap_last_committed": 92\n}\n').strip()
CEPH_REPORT_INVALID_JSON = ('\nreport 1188805303\n    "cluster_fingerprint": "0d5f8f7a-0241-4a2e-8401-9dcf37a1039b",\n    "version": "12.2.8-52.el7cp",\n    "commit": "3af3ca15b68572a357593c261f95038d02f46201",\n    "timestamp": "2019-06-05 23:33:08.514032",\n    "tag": "",\n    "health": {\n        "checks": {\n            "POOL_APP_NOT_ENABLED": {\n                "severity": "HEALTH_WARN",\n                "summary": {\n                    "message": "application not enabled on 1 pool(s)"\n                },\n                "detail": [\n                    {\n                        "message": "application not enabled on pool \'pool-a\'"\n                    },\n                    {\n                        "message": "use \'ceph osd pool application enable <pool-name> <app-name>\', where <app-name> is \'cephfs\', \'rbd\', \'rgw\', or freeform for custom applications."\n                    }\n                ]\n            },\n            "MON_DOWN": {\n                "severity": "HEALTH_WARN",\n                "summary": {\n                    "message": "1/3 mons down, quorum ceph2,ceph_1"\n                },\n                "detail": [\n                    {\n                        "message": "mon.ceph3 (rank 0) addr 10.72.37.76:6789/0 is down (out of quorum)"\n                    }\n                ]\n            }\n        },\n        "status": "HEALTH_WARN",\n        "summary": [\n            {\n                "severity": "HEALTH_WARN",\n                "summary": "\'ceph health\' JSON format has changed in luminous. If you see this your monitoring system is scraping the wrong fields. Disable this with \'mon health preluminous compat warning = false\'"\n            }\n        ],\n        "overall_status": "HEALTH_WARN",\n        "detail": [\n            "\'ceph health\' JSON format has changed in luminous. If you see this your monitoring system is scraping the wrong fields. Disable this with \'mon health preluminous compat warning = false\'"\n        ]\n    },\n    "monmap_first_committed": 1,\n    "monmap_last_committed": 1,\n    "quorum": [\n        1,\n        2\n    ],\n    "osdmap_first_committed": 1,\n    "osdmap_last_committed": 92\n}\n').strip()
CEPH_REPORT_INVALID = ('\n1188805303\n{\n    "cluster_fingerprint": "0d5f8f7a-0241-4a2e-8401-9dcf37a1039b",\n    "version": "12.2.8-52.el7cp",\n    "commit": "3af3ca15b68572a357593c261f95038d02f46201",\n    "timestamp": "2019-06-05 23:33:08.514032",\n    "tag": "",\n    "health": {\n        "checks": {\n            "POOL_APP_NOT_ENABLED": {\n                "severity": "HEALTH_WARN",\n                "summary": {\n                    "message": "application not enabled on 1 pool(s)"\n                },\n                "detail": [\n                    {\n                        "message": "application not enabled on pool \'pool-a\'"\n                    },\n                    {\n                        "message": "use \'ceph osd pool application enable <pool-name> <app-name>\', where <app-name> is \'cephfs\', \'rbd\', \'rgw\', or freeform for custom applications."\n                    }\n                ]\n            },\n            "MON_DOWN": {\n                "severity": "HEALTH_WARN",\n                "summary": {\n                    "message": "1/3 mons down, quorum ceph2,ceph_1"\n                },\n                "detail": [\n                    {\n                        "message": "mon.ceph3 (rank 0) addr 10.72.37.76:6789/0 is down (out of quorum)"\n                    }\n                ]\n            }\n        },\n        "status": "HEALTH_WARN",\n        "summary": [\n            {\n                "severity": "HEALTH_WARN",\n                "summary": "\'ceph health\' JSON format has changed in luminous. If you see this your monitoring system is scraping the wrong fields. Disable this with \'mon health preluminous compat warning = false\'"\n            }\n        ],\n        "overall_status": "HEALTH_WARN",\n        "detail": [\n            "\'ceph health\' JSON format has changed in luminous. If you see this your monitoring system is scraping the wrong fields. Disable this with \'mon health preluminous compat warning = false\'"\n        ]\n    },\n    "monmap_first_committed": 1,\n    "monmap_last_committed": 1,\n    "quorum": [\n        1,\n        2\n    ],\n    "osdmap_first_committed": 1,\n    "osdmap_last_committed": 92\n}\n').strip()
CEPH_REPORT_EMPTY = ('').strip()

def test_ceph_doc_examples():
    env = {'ceph_osd_dump': CephOsdDump(context_wrap(CEPH_OSD_DUMP_INFO)), 
       'ceph_osd_df': CephOsdDf(context_wrap(CEPH_OSD_DF_INFO)), 
       'ceph_s': CephS(context_wrap(CEPH_S_INFO)), 
       'ceph_df_detail': CephDfDetail(context_wrap(CEPH_DF_DETAIL_INFO)), 
       'ceph_health_detail': CephHealthDetail(context_wrap(CEPH_HEALTH_DETAIL_INFO)), 
       'ceph_osd_ec_profile_get': CephECProfileGet(context_wrap(CEPH_OSD_EC_PROFILE_GET)), 
       'ceph_cfg_info': CephCfgInfo(context_wrap(CEPHINFO)), 
       'ceph_osd_tree': CephOsdTree(context_wrap(CEPH_OSD_TREE)), 
       'ceph_report_content': CephReport(context_wrap(CEPH_REPORT))}
    failed, total = doctest.testmod(ceph_cmd_json_parsing, globs=env)
    assert failed == 0


class TestCephOsdDump:

    def test_ceph_osd_dump(self):
        result = CephOsdDump(context_wrap(CEPH_OSD_DUMP_INFO))
        assert result.data == {'pool_max': 12, 
           'max_osd': 8, 'created': '2016-11-12 16:08:46.307206', 
           'modified': '2017-03-07 08:55:53.301911', 
           'epoch': 210, 
           'flags': 'sortbitwise', 'cluster_snapshot': '', 
           'fsid': '2734f9b5-2013-48c1-8e96-d31423444717', 
           'pools': [
                   {'pool_name': 'rbd', 
                      'flags_names': 'hashpspool', 'min_size': 2, 
                      'object_hash': 2, 'flags': 1, 'pg_num': 256, 
                      'crush_ruleset': 0, 'type': 1, 'pool': 0, 
                      'size': 3}]}
        assert result['pools'][0]['min_size'] == 2


class TestCephOsdDf:

    def test_ceph_osd_df(self):
        result = CephOsdDf(context_wrap(CEPH_OSD_DF_INFO))
        assert result.data == {'nodes': [
                   {'id': 0, 
                      'name': 'osd.0', 
                      'type': 'osd', 
                      'type_id': 0, 
                      'crush_weight': 1.091095, 
                      'depth': 2, 
                      'reweight': 1.0, 
                      'kb': 1171539620, 
                      'kb_used': 4048208, 
                      'kb_avail': 1167491412, 
                      'utilization': 0.345546, 
                      'var': 1.189094, 
                      'pgs': 945}], 
           'stray': [], 'summary': {'total_kb': 8200777340, 
                       'total_kb_used': 23831128, 
                       'total_kb_avail': 8176946212, 
                       'average_utilization': 0.290596, 
                       'min_var': 0.803396, 
                       'max_var': 1.189094, 
                       'dev': 0.035843}}
        assert result['nodes'][0]['pgs'] == 945


class TestCephS:

    def test_ceph_s(self):
        result = CephS(context_wrap(CEPH_S_INFO))
        assert result.data == {'health': {}, 'pgmap': {'pgs_by_state': [
                                    {'state_name': 'active+clean', 
                                       'count': 1800}], 
                     'version': 314179, 
                     'num_pgs': 1800, 
                     'data_bytes': 7943926574, 
                     'bytes_used': 24405610496, 
                     'bytes_avail': 8373190385664, 
                     'bytes_total': 8397595996160}, 
           'fsmap': {'epoch': 1, 
                     'by_rank': []}}
        assert result['pgmap']['pgs_by_state'][0]['state_name'] == 'active+clean'


class TestCephECProfileGet:

    def test_ceph_ec_profile_get(self):
        result = CephECProfileGet(context_wrap(CEPH_OSD_EC_PROFILE_GET))
        assert result.data == {'k': '2', 
           'm': '1', 
           'plugin': 'jerasure', 
           'technique': 'reed_sol_van'}
        assert result['k'] == '2'
        assert result['m'] == '1'


class TestCephCfgInfo:

    def test_cephcfginfo(self):
        result = CephCfgInfo(context_wrap(CEPHINFO))
        assert result.data == {'ms_tcp_nodelay': 'true', 
           'ms_max_backoff': '15', 'cluster': 'ceph', 
           'ms_dispatch_throttle_bytes': '104857600', 'debug_none': '0/5', 
           'ms_crc_data': 'true', 'perf': 'true', 'ms_tcp_prefetch_max_size': '4096', 
           'ms_die_on_bad_msg': 'false', 'ms_bind_port_max': '7300', 
           'ms_bind_port_min': '6800', 'ms_die_on_skipped_message': 'false', 
           'heartbeat_file': '', 'heartbeat_interval': '5', 
           'heartbeat_inject_failure': '0', 'ms_crc_header': 'true', 
           'max_open_files': '131072', 'ms_die_on_old_message': 'false', 
           'name': 'osd.1', 'ms_type': 'simple', 
           'ms_initial_backoff': '0.2', 'ms_bind_retry_delay': '5', 
           'ms_bind_ipv6': 'false', 'ms_die_on_unhandled_msg': 'false', 
           'ms_tcp_rcvbuf': '0', 'ms_bind_retry_count': '3'}
        assert result.max_open_files == '131072'


class TestCephHealthDetail:

    def test_ceph_health_detail(self):
        result = CephHealthDetail(context_wrap(CEPH_HEALTH_DETAIL_INFO))
        assert result.data == {'health': {}, 'timechecks': {'epoch': 4, 
                          'round': 0, 
                          'round_status': 'finished'}, 
           'summary': [], 'overall_status': 'HEALTH_OK', 
           'detail': []}
        assert result['overall_status'] == 'HEALTH_OK'


class TestCephDfDetail:

    def test_ceph_df_detail(self):
        result = CephDfDetail(context_wrap(CEPH_DF_DETAIL_INFO))
        assert result.data == {'stats': {'total_bytes': 17113243648, 
                     'total_used_bytes': 203120640, 
                     'total_avail_bytes': 16910123008, 
                     'total_objects': 0}, 
           'pools': [
                   {'name': 'rbd', 
                      'id': 0, 
                      'stats': {'kb_used': 0, 
                                'bytes_used': 0, 
                                'max_avail': 999252180, 
                                'objects': 0, 
                                'dirty': 0, 
                                'rd': 0, 
                                'rd_bytes': 0, 
                                'wr': 0, 
                                'wr_bytes': 0, 
                                'raw_bytes_used': 0}},
                   {'name': 'ecpool', 
                      'id': 2, 
                      'stats': {'kb_used': 0, 
                                'bytes_used': 0, 
                                'max_avail': 1998504360, 
                                'objects': 0, 
                                'dirty': 0, 
                                'rd': 0, 
                                'rd_bytes': 0, 
                                'wr': 0, 
                                'wr_bytes': 0, 
                                'raw_bytes_used': 0}}]}
        assert result['stats']['total_avail_bytes'] == 16910123008


class TestCephOsdTree:

    def test_ceph_osd_tree(self):
        result = CephOsdTree(context_wrap(CEPH_OSD_TREE))
        assert result.data == {'nodes': [
                   {'id': -1, 
                      'name': 'default', 
                      'type': 'root', 
                      'type_id': 10, 
                      'children': [
                                 -5,
                                 -4,
                                 -3,
                                 -2]},
                   {'id': -2, 
                      'name': 'dhcp-192-56', 
                      'type': 'host', 
                      'type_id': 1, 
                      'children': []},
                   {'id': -3, 
                      'name': 'dhcp-192-104', 
                      'type': 'host', 
                      'type_id': 1, 
                      'children': []},
                   {'id': -4, 
                      'name': 'dhcp-192-67', 
                      'type': 'host', 
                      'type_id': 1, 
                      'children': []},
                   {'id': -5, 
                      'name': 'localhost', 
                      'type': 'host', 
                      'type_id': 1, 
                      'children': [
                                 1,
                                 3,
                                 5,
                                 2,
                                 4,
                                 0]},
                   {'id': 0, 
                      'name': 'osd.0', 
                      'type': 'osd', 
                      'type_id': 0, 
                      'crush_weight': 0.002991, 
                      'depth': 2, 
                      'exists': 1, 
                      'status': 'up', 
                      'reweight': 1.0, 
                      'primary_affinity': 1.0},
                   {'id': 4, 
                      'name': 'osd.4', 
                      'type': 'osd', 
                      'type_id': 0, 
                      'crush_weight': 0.002991, 
                      'depth': 2, 
                      'exists': 1, 
                      'status': 'down', 
                      'reweight': 1.0, 
                      'primary_affinity': 1.0},
                   {'id': 2, 
                      'name': 'osd.2', 
                      'type': 'osd', 
                      'type_id': 0, 
                      'crush_weight': 0.002991, 
                      'depth': 2, 
                      'exists': 1, 
                      'status': 'up', 
                      'reweight': 1.0, 
                      'primary_affinity': 1.0},
                   {'id': 5, 
                      'name': 'osd.5', 
                      'type': 'osd', 
                      'type_id': 0, 
                      'crush_weight': 0.002991, 
                      'depth': 2, 
                      'exists': 1, 
                      'status': 'up', 
                      'reweight': 1.0, 
                      'primary_affinity': 1.0},
                   {'id': 3, 
                      'name': 'osd.3', 
                      'type': 'osd', 
                      'type_id': 0, 
                      'crush_weight': 0.002991, 
                      'depth': 2, 
                      'exists': 1, 
                      'status': 'up', 
                      'reweight': 1.0, 
                      'primary_affinity': 1.0},
                   {'id': 1, 
                      'name': 'osd.1', 
                      'type': 'osd', 
                      'type_id': 0, 
                      'crush_weight': 0.002991, 
                      'depth': 2, 
                      'exists': 1, 
                      'status': 'up', 
                      'reweight': 1.0, 
                      'primary_affinity': 1.0}], 
           'stray': []}
        assert len(result['nodes'][0]['children']) == 4


class TestCephReport:

    def test_ceph_report(self):
        result = CephReport(context_wrap(CEPH_REPORT))
        assert result['version'] == '12.2.8-52.el7cp'

    def test_invalid(self):
        with pytest.raises(ParseException) as (e):
            CephReport(context_wrap(CEPH_REPORT_INVALID))
        assert 'Invalid' in str(e)

    def test_invalid_json(self):
        with pytest.raises(ParseException) as (e):
            CephReport(context_wrap(CEPH_REPORT_INVALID_JSON))
        assert 'Could not parse json.' in str(e)

    def test_invalid_empty(self):
        with pytest.raises(SkipException) as (e):
            CephReport(context_wrap(CEPH_REPORT_EMPTY))
        assert 'Empty output.' in str(e)