# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rhv_log_collector_analyzer.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.rhv_log_collector_analyzer import RhvLogCollectorJson
from insights.tests import context_wrap
RHV_ANALYZER_JSON = ('\n{\n    "hostname": "localhost.localdomain.localdomain",\n    "rhv-log-collector-analyzer": [\n        {\n            "bugzilla": "",\n            "description": "Found Cluster(s) using Legacy Migration Policy It is recommended to update the Migration Policy. Please visit: https://access.redhat.com/solutions/3143541",\n            "file": "cluster_query_migration_policy_check_legacy.sql",\n            "hash": "fb908a5befb8bedd2c87d8d7fcd6f305",\n            "id": "67cd9967367beb3e7431a4e5b1970efc4914007af95735de40c2298ea6f18f19",\n            "id_host": "08985ce25cee4dcd8a2e56cebc3574ad",\n            "kb": "https://access.redhat.com/solutions/3143541",\n            "name": "check_legacy_policy",\n            "path": "/usr/share/rhv-log-collector-analyzer/analyzer/produceReport/sqls/cluster_query_migration_policy_check_legacy.sql",\n            "result": [\n                [\n                    {\n                        "Cluster": "fccl",\n                        "Data Center": "fcdc",\n                        "NO.": 1\n                    }\n                ],\n                [\n                    {\n                        "Cluster": "larry",\n                        "Data Center": "Default",\n                        "NO.": 2\n                    }\n                ],\n                [\n                    {\n                        "Cluster": "larry",\n                        "Data Center": "lo-dc",\n                        "NO.": 3\n                    }\n                ],\n                [\n                    {\n                        "Cluster": "larry",\n                        "Data Center": "fcdc",\n                        "NO.": 4\n                    }\n                ],\n                [\n                    {\n                        "Cluster": "larry",\n                        "Data Center": "larry",\n                        "NO.": 5\n                    }\n                ],\n                [\n                    {\n                        "Cluster": "lo-cl",\n                        "Data Center": "lo-dc",\n                        "NO.": 6\n                    }\n                ]\n            ],\n            "time": "0.0137791633606",\n            "type": "WARNING",\n            "when": "2018-06-27 00:19:14"\n        }\n   ]\n}\n').strip()

class TestRhvLogCollectorJson:

    def test_rhv_log_collector_json(self):
        result = RhvLogCollectorJson(context_wrap(RHV_ANALYZER_JSON))
        assert result.data == {'hostname': 'localhost.localdomain.localdomain', 
           'rhv-log-collector-analyzer': [
                                        {'bugzilla': '', 
                                           'description': 'Found Cluster(s) using Legacy Migration Policy It is recommended to update the Migration Policy. Please visit: https://access.redhat.com/solutions/3143541', 
                                           'file': 'cluster_query_migration_policy_check_legacy.sql', 
                                           'hash': 'fb908a5befb8bedd2c87d8d7fcd6f305', 
                                           'id': '67cd9967367beb3e7431a4e5b1970efc4914007af95735de40c2298ea6f18f19', 
                                           'id_host': '08985ce25cee4dcd8a2e56cebc3574ad', 
                                           'kb': 'https://access.redhat.com/solutions/3143541', 
                                           'name': 'check_legacy_policy', 
                                           'path': '/usr/share/rhv-log-collector-analyzer/analyzer/produceReport/sqls/cluster_query_migration_policy_check_legacy.sql', 
                                           'result': [
                                                    [
                                                     {'Cluster': 'fccl', 
                                                        'Data Center': 'fcdc', 
                                                        'NO.': 1}],
                                                    [
                                                     {'Cluster': 'larry', 
                                                        'Data Center': 'Default', 
                                                        'NO.': 2}],
                                                    [
                                                     {'Cluster': 'larry', 
                                                        'Data Center': 'lo-dc', 
                                                        'NO.': 3}],
                                                    [
                                                     {'Cluster': 'larry', 
                                                        'Data Center': 'fcdc', 
                                                        'NO.': 4}],
                                                    [
                                                     {'Cluster': 'larry', 
                                                        'Data Center': 'larry', 
                                                        'NO.': 5}],
                                                    [
                                                     {'Cluster': 'lo-cl', 
                                                        'Data Center': 'lo-dc', 
                                                        'NO.': 6}]], 
                                           'time': '0.0137791633606', 
                                           'type': 'WARNING', 
                                           'when': '2018-06-27 00:19:14'}]}
        assert result['rhv-log-collector-analyzer'][0]['file'] == 'cluster_query_migration_policy_check_legacy.sql'