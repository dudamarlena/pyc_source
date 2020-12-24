# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/errr/programs/python/thunderhead/tests/rules_tests.py
# Compiled at: 2014-09-18 23:21:50
# Size of source mod 2**32: 3985 bytes
import vcr, tests
from thunderhead.builder import rules

class RulesTest(tests.ThunderheadTests):

    @vcr.use_cassette('get_all_rules.yaml', cassette_library_dir=tests.fixtures_path, record_mode='once')
    def test_get_all_rules(self):
        all_rules = rules.get_all_rules(tests.CONNECTION)
        self.assertIsNotNone(all_rules)
        self.assertIsInstance(all_rules, list)
        d1 = {'vcServerId': '1', 
         'valueType': 'Unique ID', 
         'value': 'datacenter-2', 
         'id': '2', 
         'customerId': '3', 
         'objectType': 'Data Center'}
        self.assertDictEqual(all_rules[0], d1)

    @vcr.use_cassette('get_rule_by_id_found.yaml', cassette_library_dir=tests.fixtures_path, record_mode='once')
    def test_get_rule_by_id_found(self):
        rule_id = 2
        rule = rules.get_rule(tests.CONNECTION, rule_id)
        self.assertIsNotNone(rule)
        d1 = {'vcServerId': '1', 
         'valueType': 'Unique ID', 
         'value': 'datacenter-2', 
         'id': '2', 
         'customerId': '3', 
         'objectType': 'Data Center'}
        self.assertDictEqual(rule, d1)

    @vcr.use_cassette('get_rule_by_id_not_found.yaml', cassette_library_dir=tests.fixtures_path, record_mode='once')
    def test_get_rule_by_id_not_found(self):
        rule_id = 10000
        with self.assertRaises(rules.RuleNotFoundException):
            rules.get_rule(tests.CONNECTION, rule_id)

    @vcr.use_cassette('delete_rule_by_id_not_found.yaml', cassette_library_dir=tests.fixtures_path, record_mode='once')
    def test_delete_rule_by_id_not_found(self):
        rule_id = 1
        deleted = rules.delete_rule(tests.CONNECTION, rule_id)
        self.assertTrue(deleted)

    @vcr.use_cassette('delete_rule_by_id.yaml', cassette_library_dir=tests.fixtures_path, record_mode='once')
    def test_delete_rule_by_id(self):
        rule_id = 2
        deleted = rules.delete_rule(tests.CONNECTION, rule_id)
        self.assertTrue(deleted)

    @vcr.use_cassette('create_new_rule_fail_no_customer.yaml', cassette_library_dir=tests.fixtures_path, record_mode='once')
    def test_create_new_rule_fail_no_customer(self):
        rule_info = {'vcServerHost': '172.16.214.129', 
         'customerName': '1018700', 
         'objectType': 'Data Center', 
         'valueType': 'Unique ID', 
         'value': 'datacenter-104'}
        with self.assertRaises(rules.RuleCreationException):
            rules.create_rule(tests.CONNECTION, rule_info)

    @vcr.use_cassette('create_new_rule.yaml', cassette_library_dir=tests.fixtures_path, record_mode='once')
    def test_create_new_rule(self):
        rule_info = {'vcServerHost': '172.16.214.129', 
         'customerName': '1018700', 
         'objectType': 'Data Center', 
         'valueType': 'Unique ID', 
         'value': 'datacenter-104'}
        rule = rules.create_rule(tests.CONNECTION, rule_info)
        self.assertIsNotNone(rule)