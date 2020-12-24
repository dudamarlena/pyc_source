# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/okera/tests/test_configs.py
# Compiled at: 2020-02-27 14:06:57
# Size of source mod 2**32: 9561 bytes
import unittest
from okera import context, _thrift_api
from okera._thrift_api import TConfigType, TRecordServiceException

def list_configs(conn, config_type):
    """List configurations of the specified type.

    config_type : TConfigType
        The type of configurations to return.

    Returns
    -------
    map(str, str)
        List of configs as a map of key values.
    """
    table_name = None
    if config_type == TConfigType.AUTOTAGGER_REGEX:
        table_name = 'okera_system.tagging_rules'
    else:
        if config_type == TConfigType.SYSTEM_CONFIG:
            table_name = 'okera_system.configs'
        else:
            raise ValueError('Invalid config type.')
    return conn.scan_as_json(table_name)


def list_of_map_to_map(l, key_field):
    result = {}
    for v in l:
        key = v[key_field]
        result[key] = v

    return result


def upsert_config(conn, config_type, key, value):
    """Upsert a configuration.

    config_type : TConfigType
        The type of configurations to return.
    key : str
        The key for this configuration. This must be unique with config_type.
    value : str
        The value for this config.

    Returns
    -------
    bool
        Returns true if the config was updated or false if it was inserted.
    list(str), optional
        List of warnings that were generated as part of this request.
    """
    request = _thrift_api.TConfigUpsertParams()
    request.config_type = config_type
    request.key = key
    if isinstance(value, str):
        request.params = {'value': value}
    else:
        request.params = value
    result = conn.service.client.UpsertConfig(request)
    return (
     True, result.warnings)


def delete_config(conn, config_type, key):
    """Upsert a configuration.

    config_type : TConfigType
        The type of configurations to return.
    key : str
        The key for this configuration. This must be unique with config_type.

    Returns
    -------
    bool
        Returns true if the config was deleted.
    list(str), optional
        List of warnings that were generated as part of this request.
    """
    request = _thrift_api.TConfigDeleteParams()
    request.config_type = config_type
    request.key = key
    result = conn.service.client.DeleteConfig(request)
    return (
     True, result.warnings)


TEST_CONFIG_KEY1 = 'test_configs_key1'
TEST_CONFIG_KEY2 = 'test_configs_key2'

class ConfigsTest(unittest.TestCase):

    def test_basic(self):
        with context().connect() as (conn):
            configs = list_of_map_to_map(list_configs(conn, TConfigType.SYSTEM_CONFIG), 'key')
            self.assertTrue('audit.directory' in configs)
            self.assertEqual('/opt/audit_logs', configs['audit.directory']['value'])
            upsert_config(conn, TConfigType.SYSTEM_CONFIG, [TEST_CONFIG_KEY1], 'val1')
            configs = list_of_map_to_map(list_configs(conn, TConfigType.SYSTEM_CONFIG), 'key')
            self.assertEqual('val1', configs[TEST_CONFIG_KEY1]['value'])
            upsert_config(conn, TConfigType.SYSTEM_CONFIG, [TEST_CONFIG_KEY1], 'val2')
            configs = list_of_map_to_map(list_configs(conn, TConfigType.SYSTEM_CONFIG), 'key')
            self.assertEqual('val2', configs[TEST_CONFIG_KEY1]['value'])
            upsert_config(conn, TConfigType.SYSTEM_CONFIG, [TEST_CONFIG_KEY1], '')
            configs = list_of_map_to_map(list_configs(conn, TConfigType.SYSTEM_CONFIG), 'key')
            self.assertEqual('', configs[TEST_CONFIG_KEY1]['value'])
            upsert_config(conn, TConfigType.SYSTEM_CONFIG, [TEST_CONFIG_KEY2], 'new_val1')
            configs = list_of_map_to_map(list_configs(conn, TConfigType.SYSTEM_CONFIG), 'key')
            self.assertEqual('', configs[TEST_CONFIG_KEY1]['value'])
            self.assertEqual('new_val1', configs[TEST_CONFIG_KEY2]['value'])
            delete_config(conn, TConfigType.SYSTEM_CONFIG, [TEST_CONFIG_KEY2])
            configs = list_of_map_to_map(list_configs(conn, TConfigType.SYSTEM_CONFIG), 'key')
            self.assertEqual('', configs[TEST_CONFIG_KEY1]['value'])
            self.assertTrue(TEST_CONFIG_KEY2 not in configs)
            delete_config(conn, TConfigType.SYSTEM_CONFIG, [TEST_CONFIG_KEY1])
            configs = list_of_map_to_map(list_configs(conn, TConfigType.SYSTEM_CONFIG), 'key')
            self.assertTrue(TEST_CONFIG_KEY1 not in configs)
            self.assertTrue(TEST_CONFIG_KEY2 not in configs)

    def test_upsert_regex_autotagger(self):
        with context().connect() as (conn):
            for c in list_configs(conn, TConfigType.AUTOTAGGER_REGEX):
                if c['namespace'] == 'test_ns' and c['tag'] == 'rule1':
                    delete_config(conn, TConfigType.AUTOTAGGER_REGEX, str(c['id']))

            params = {}
            params['name'] = 'great_rule'
            params['namespace'] = 'test_ns'
            params['description'] = 'a great regex'
            params['min_rows'] = '1'
            params['max_rows'] = '10'
            params['match_rate'] = '.4'
            params['match_column_name'] = 'true'
            params['match_column_comment'] = 'true'
            params['tag'] = 'rule1'
            params['expression'] = '*'
            upsert_config(conn, TConfigType.AUTOTAGGER_REGEX, None, params)
            rule = None
            for c in list_configs(conn, TConfigType.AUTOTAGGER_REGEX):
                if c['namespace'] == 'test_ns' and c['tag'] == 'rule1':
                    rule = c
                    break

            self.assertTrue(rule is not None)
            self.assertEqual('test_ns', rule['namespace'])
            self.assertEqual('*', rule['expression'])
            self.assertEqual('a great regex', rule['description'])
            self.assertTrue(rule['match_column_name'])
            self.assertTrue(rule['match_column_comment'])
            self.assertEqual('great_rule', rule['name'])
            params['expression'] = '.*'
            old_id = rule['id']
            upsert_config(conn, TConfigType.AUTOTAGGER_REGEX, [str(old_id)], params)
            rule = None
            for c in list_configs(conn, TConfigType.AUTOTAGGER_REGEX):
                if c['namespace'] == 'test_ns' and c['tag'] == 'rule1':
                    rule = c
                    break

            self.assertTrue(rule is not None)
            self.assertEqual('test_ns', rule['namespace'])
            self.assertEqual('.*', rule['expression'])
            self.assertEqual('great_rule', rule['name'])
            self.assertEqual(old_id, rule['id'])
            del params['name']
            with self.assertRaises(TRecordServiceException):
                upsert_config(conn, TConfigType.AUTOTAGGER_REGEX, [str(old_id)], params)
            params = {}
            params['name'] = 'greater_rule'
            params['namespace'] = 'test_ns'
            params['description'] = 'another great regex'
            params['min_rows'] = '3'
            params['max_rows'] = '55'
            params['match_rate'] = '.2'
            params['tag'] = 'rule1'
            params['expression'] = 'foo*'
            old_name = params['name']
            upsert_config(conn, TConfigType.AUTOTAGGER_REGEX, None, params)
            rules = []
            for c in list_configs(conn, TConfigType.AUTOTAGGER_REGEX):
                if c['namespace'] == 'test_ns' and c['tag'] == 'rule1':
                    rules.append(c)

            self.assertEqual(2, len(rules))
            self.assertTrue(old_id in (rules[0]['id'], rules[1]['id']))
            params = {}
            params['namespace'] = 'test_ns'
            params['description'] = 'another great regex'
            params['min_rows'] = '3'
            params['max_rows'] = '55'
            params['match_rate'] = '.2'
            params['tag'] = 'rule1'
            params['expression'] = 'foo*'
            with self.assertRaises(TRecordServiceException):
                upsert_config(conn, TConfigType.AUTOTAGGER_REGEX, None, params)
            params['name'] = ''
            with self.assertRaises(TRecordServiceException):
                upsert_config(conn, TConfigType.AUTOTAGGER_REGEX, None, params)
            params['name'] = old_name
            with self.assertRaises(TRecordServiceException):
                upsert_config(conn, TConfigType.AUTOTAGGER_REGEX, None, params)


if __name__ == '__main__':
    unittest.main()