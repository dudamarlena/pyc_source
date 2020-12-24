# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/core/rule.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 6617 bytes
import json, re
from ScoutSuite.core.fs import read_ip_ranges
from ScoutSuite.core.console import print_exception
from ScoutSuite.utils import format_service_name
ip_ranges_from_args = 'ip-ranges-from-args'
re_account_id = re.compile('_ACCOUNT_ID_')
re_ip_ranges_from_file = re.compile('_IP_RANGES_FROM_FILE_\\((.*?)(,.*?)\\)')
re_ip_ranges_from_local_file = re.compile('_IP_RANGES_FROM_LOCAL_FILE_\\((.*?)(,.*?)\\)')
re_strip_dots = re.compile('(_STRIPDOTS_\\((.*?)\\))')
testcases = [
 {'name':'account_id', 
  'regex':re_account_id},
 {'name':'ip_ranges_from_file', 
  'regex':re_ip_ranges_from_file},
 {'name':'ip_ranges_from_local_file', 
  'regex':re_ip_ranges_from_local_file}]

class Rule(object):

    def to_string(self):
        return str(vars(self))

    def __init__(self, data_path, filename, rule_type, rule):
        self.data_path = data_path
        self.filename = filename
        self.rule_type = rule_type
        self.enabled = bool(self.get_attribute('enabled', rule, False))
        self.level = self.get_attribute('level', rule, '')
        self.args = self.get_attribute('args', rule, [])
        self.conditions = self.get_attribute('conditions', rule, [])
        self.key_suffix = self.get_attribute('key_suffix', rule, None)

    @staticmethod
    def get_attribute(name, rule, default_value):
        if name in list(rule.keys()):
            return rule[name]
        return default_value

    def set_definition(self, rule_definitions, attributes=None, ip_ranges=None, params=None):
        """
        Update every attribute of the rule by setting the argument values as necessary

        :param rule_definitions:            TODO
        :param attributes:                  TODO
        :param ip_ranges:                   TODO
        :param params:                      TODO
        :return:
        """
        attributes = [] if attributes is None else attributes
        ip_ranges = [] if ip_ranges is None else ip_ranges
        params = {} if params is None else params
        try:
            string_definition = rule_definitions[self.filename].string_definition
            definition = json.loads(string_definition)
            definition['conditions'] += self.conditions
            loaded_conditions = []
            for condition in definition['conditions']:
                if condition[0].startswith('_INCLUDE_('):
                    include = re.findall('_INCLUDE_\\((.*?)\\)', condition[0])[0]
                    rules_path = '%s/%s' % (self.data_path, include)
                    with open(rules_path, 'rt') as (f):
                        new_conditions = f.read()
                        for i, value in enumerate(condition[1]):
                            new_conditions = re.sub(condition[1][i], condition[2][i], new_conditions)

                        new_conditions = json.loads(new_conditions)['conditions']
                    loaded_conditions.append(new_conditions)
                else:
                    loaded_conditions.append(condition)

            definition['conditions'] = loaded_conditions
            string_definition = json.dumps(definition)
            parameters = re.findall('(_ARG_([a-zA-Z0-9]+)_)', string_definition)
            for param in parameters:
                index = int(param[1])
                if len(self.args) <= index:
                    string_definition = string_definition.replace(param[0], '')
                elif type(self.args[index]) == list:
                    value = '[ %s ]' % ', '.join(('"%s"' % v for v in self.args[index]))
                    string_definition = string_definition.replace('"%s"' % param[0], value)
                else:
                    string_definition = string_definition.replace(param[0], self.args[index])

            stripdots = re_strip_dots.findall(string_definition)
            for value in stripdots:
                string_definition = string_definition.replace(value[0], value[1].replace('.', ''))

            definition = json.loads(string_definition)
            for condition in definition['conditions']:
                if not type(condition) != list:
                    if len(condition) == 1 or type(condition[2]) == list:
                        continue
                    for testcase in testcases:
                        result = testcase['regex'].match(condition[2])
                        if result:
                            if testcase['name'] == 'ip_ranges_from_file' or testcase['name'] == 'ip_ranges_from_local_file':
                                filename = result.groups()[0]
                                conditions = result.groups()[1] if len(result.groups()) > 1 else []
                                if filename == ip_ranges_from_args:
                                    prefixes = []
                                    for filename in ip_ranges:
                                        prefixes += read_ip_ranges(filename, local_file=True, ip_only=True, conditions=conditions)

                                    condition[2] = prefixes
                                    break
                                else:
                                    local_file = True if testcase['name'] == 'ip_ranges_from_local_file' else False
                                    condition[2] = read_ip_ranges(filename, local_file=local_file, ip_only=True, conditions=conditions)
                                    break
                        if result:
                            condition[2] = params[testcase['name']]
                            break

            if len(attributes) == 0:
                attributes = [attr for attr in definition]
            for attr in attributes:
                if attr in definition:
                    setattr(self, attr, definition[attr])

            if hasattr(self, 'path'):
                self.service = format_service_name(self.path.split('.')[0])
            if not hasattr(self, 'key'):
                setattr(self, 'key', self.filename)
            setattr(self, 'key', self.key.replace('.json', ''))
            if self.key_suffix:
                setattr(self, 'key', '%s-%s' % (self.key, self.key_suffix))
        except Exception as e:
            try:
                print_exception('Failed to set definition %s: %s' % (self.filename, e))
            finally:
                e = None
                del e