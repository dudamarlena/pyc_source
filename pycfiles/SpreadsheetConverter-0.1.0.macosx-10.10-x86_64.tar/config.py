# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yugo/.virtualenvs/ssc/lib/python2.7/site-packages/spreadsheetconverter/config.py
# Compiled at: 2016-03-17 09:43:59
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
import codecs
from collections import defaultdict
import six, yaml
from .loader import get_loader
from .handler import get_handler
from .handler.inspector import get_inspectors
from .exceptions import TargetFieldDoesNotExistError
from .utils import search_path

class Config(object):

    def __init__(self, rules, target_fields=None):
        self.rules = rules
        self.target_fields = target_fields
        if target_fields:
            fields = [ field for field in self.rules[b'fields'] if field[b'column'] in target_fields ]
        else:
            fields = self.rules[b'fields']
        self._fields = {field[b'name']:field for field in fields}
        self._fields_column = {field[b'column']:field for field in fields}
        self._loader = None
        self._handler = None
        self._formatter = {}
        self._converter = {}
        self._validator = defaultdict(dict)
        self._inspectors = None
        self._column_name_index_map = {}
        self.name = self.rules[b'target']
        return

    @property
    def loader(self):
        if self._loader:
            return self._loader
        self._loader = get_loader(self.rules[b'target'])
        return self._loader

    @property
    def handler(self):
        if self._handler:
            return self._handler
        self._handler = get_handler(self.rules[b'handler'], self)
        return self._handler

    @property
    def inspectors(self):
        if self._inspectors:
            return self._inspectors
        self._inspectors = get_inspectors(self.rules[b'handler'], self.target_fields)
        return self._inspectors

    @property
    def header_row_index(self):
        u"""
        カラム名のはいっている行
        :rtype: int
        """
        return self.rules.get(b'row', 1) - 1

    @property
    def data_start_row_index(self):
        u"""
        データのはいっている開始行
        :rtype: int
        """
        return self.header_row_index + 1

    @property
    def limit(self):
        u"""
        変換の最大数
        :rtype: int
        """
        if b'limit' in self.rules:
            return self.rules[b'limit']
        else:
            return

    def get_converter(self, item):
        if item not in self._fields:
            return None
        else:
            if item in self._converter:
                return self._converter[item]
            converter = self.loader.get_value_converter(self._fields[item], config=self)
            self._converter[item] = converter
            return converter

    def get_converter_by_column(self, item):
        return self.get_converter(self._fields_column[item][b'name'])

    def get_formatter(self, item):
        if item in self._formatter:
            return self._formatter[item]
        formatter = self.handler.get_value_formatter(self._fields_column[item])
        self._formatter[item] = formatter
        return formatter

    def get_validators(self, item):
        if item in self._validator:
            return self._validator[item]
        validators = self.loader.get_validators(self._fields_column[item])
        self._validator[item] = validators
        return validators

    def get_sheet(self):
        return self.loader.sheet

    def save(self, data):
        for entity in data:
            for key, value in entity.items():
                formatter = self.get_formatter(key)
                if not formatter:
                    continue
                entity[key] = formatter.format(value)

        self.inspect(data)
        self.handler.save(data)

    def convert(self, sheet):
        _data = []
        count = 0
        for i, row in enumerate(sheet.rows):
            if i == self.header_row_index:
                self.load_header_row(row)
                self.check_header_row()
                continue
            if i < self.data_start_row_index:
                continue
            try:
                _data.append(self.convert_column(row))
            except ValueError as e:
                print((b'Error row: [{}] {}').format((b':').join([ six.text_type(v) for v in row ]), e.message))
                raise

            count += 1
            if self.limit and count >= self.limit:
                break

        return _data

    def convert_column(self, row):
        result = {}
        for i, value in enumerate(row):
            converter = self.get_converter(self._column_name_index_map[i])
            if not converter:
                continue
            converted = converter.to_python(value)
            result[converter.fieldname] = converted
            validators = self.get_validators(converter.fieldname)
            for validator in validators:
                validator.validate(converted)

        return result

    def load_header_row(self, row):
        for i, name in enumerate(row):
            self._column_name_index_map[i] = name

    def check_header_row(self):
        field_names = set(self._column_name_index_map.values())
        target_field_names = set(self._fields.keys())
        if not target_field_names <= field_names:
            raise TargetFieldDoesNotExistError((b'{}: nothing fields: {}').format(self.name, (b', ').join(target_field_names - field_names)))

    def has_cache(self):
        return False

    def get_cache(self):
        raise NotImplementedError

    def inspect(self, data):
        for row in data:
            for inspector in self.inspectors:
                inspector.inspect(row)


YAML_CACHE = {}

class YamlConfig(Config):

    def __init__(self, yaml_path, target_fields=None):
        abs_yaml_path = search_path(yaml_path, path_env=b'SSC_YAML_SEARCH_PATH', recursive_env=b'SSC_YAML_SEARCH_RECURSIVE')
        f = codecs.open(abs_yaml_path, b'r', b'utf8').read()
        rules = yaml.load(f)
        super(YamlConfig, self).__init__(rules, target_fields=target_fields)
        self.name = yaml_path
        self._converted = None
        return

    @classmethod
    def get_config(cls, yaml_path, target_fields=None, **kwargs):
        cache_key = (b':').join([yaml_path] + (sorted(target_fields) if target_fields else []))
        if cache_key in YAML_CACHE:
            return YAML_CACHE[cache_key]
        config = cls(yaml_path, target_fields=target_fields, **kwargs)
        YAML_CACHE[cache_key] = config
        config._load_relation_config()
        return YAML_CACHE[cache_key]

    def _load_relation_config(self):
        for entity in self.rules[b'fields']:
            if self.target_fields and entity[b'column'] in self.target_fields:
                continue
            if b'relation' not in entity:
                continue
            if isinstance(entity[b'relation'][b'from'], six.string_types):
                related_path = entity[b'relation'][b'from']
                entity[b'relation'][b'from'] = YamlConfig.get_config(related_path, target_fields=[
                 entity[b'relation'][b'column'],
                 entity[b'relation'][b'key']])

    def convert(self, sheet):
        _result = super(YamlConfig, self).convert(sheet)
        self._set_cache(_result)
        return _result

    def has_cache(self):
        return bool(self._converted)

    def get_cache(self):
        return self._converted

    def _set_cache(self, data):
        self._converted = data