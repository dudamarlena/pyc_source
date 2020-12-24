# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_policycache.py
# Compiled at: 2019-05-23 11:08:11
import unittest
from policytool import policycache
from policytool.policycache import PolicyCache

class TestPolicyCacheClassMethods(unittest.TestCase):

    def test__extract_resources_for_one_table_object(self):
        indata = {'serviceResources': [{'id': 109410, 'resourceElements': {'table': {'isExcludes': False, 'values': ['table_name'], 'isRecursive': False}, 'database': {'isExcludes': False, 'values': ['db_name'], 'isRecursive': False}}}]}
        result = PolicyCache._extract_resources(indata, 'table')
        self.assertEqual(result, {('db_name', 'table_name'): 109410})

    def test__extract_resources_for_no_table_object(self):
        indata = {'serviceResources': [{'id': 109410, 'resourceElements': {'database': {'isExcludes': False, 'values': ['db_name'], 'isRecursive': False}}}]}
        result = PolicyCache._extract_resources(indata, 'table')
        self.assertEqual(result, {})


class TestPolicyCache(unittest.TestCase):

    def test__tags_for_resource(self):
        indata = {'serviceResources': [
                              {'isEnabled': True, 'id': 109410, 
                                 'resourceElements': {'database': {'isExcludes': False, 'values': ['db_name'], 'isRecursive': False}}}], 
           'tags': {'81921': {'type': 'mytag'}, 
                    '42': {'type': 'life'}}, 
           'resourceToTagIds': {'109410': [
                                         81921,
                                         42]}}
        policy_cache = PolicyCache(indata)
        tags = policy_cache._tags_for_resource('109410')
        self.assertEqual(tags, ['mytag', 'life'])