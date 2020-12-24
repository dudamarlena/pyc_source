# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wargaming/parser.py
# Compiled at: 2018-05-14 16:33:13
from collections import namedtuple
from datetime import datetime
import six
type_tuple = namedtuple('validator', ['validate', 'convert'])
types_map = {'numeric': type_tuple(lambda x: isinstance(x, int), int), 
   'float': type_tuple(lambda x: isinstance(x, float), float), 
   'boolean': type_tuple(lambda x: isinstance(x, bool), bool), 
   'string': type_tuple(lambda x: isinstance(x, six.string_types), str), 
   'timestamp': type_tuple(lambda x: isinstance(x, datetime), lambda x: datetime.fromtimestamp(x)), 
   'list of timestamps': type_tuple(lambda x: all(map(lambda y: isinstance(y, datetime), x)), lambda x: list(map(lambda y: datetime.fromtimestamp(y), x))), 
   'list of strings': type_tuple(lambda x: all(map(lambda y: isinstance(y, six.string_types), x)), lambda x: list(map(str, x)))}

def unflatten_fields(fields, parent=None):
    """Make nested dict with field types from flat list"""
    parent = parent or []
    data = {}
    subsections = {}
    for field in fields:
        field_type = field['type']
        if field_type == 'empty_line':
            continue
        name = field['name']
        if len(name) > len(parent) + 1 and name[:len(parent)] == parent:
            subsections[name[len(parent)]] = parent + [name[len(parent)]]
        elif name == parent + [name[(-1)]]:
            if field_type in types_map:
                field_type = types_map[field_type]
            else:
                field_type = None
            data[name[(-1)]] = field_type

    for name, path in subsections.items():
        data[name] = unflatten_fields(fields, path)

    return data


def _parse_data(fields, data):
    """recursive function which converts data to correct fields type"""
    for name in data:
        if name not in fields:
            continue
        elif data[name] is None:
            continue
        elif isinstance(fields[name], dict):
            if isinstance(data[name], list):
                data[name] = [ _parse_data(fields[name], i) ]
            else:
                data[name] = _parse_data(fields[name], data[name])
        elif fields[name]:
            data[name] = fields[name].validate(data[name]) or fields[name].convert(data[name])

    return data


class Parser(object):

    def __init__(self, fields):
        self.fields = unflatten_fields(fields)

    def parse_response_data(self, data):
        """Parse response from WG API and set correct types of values
        :param data: data section from WG API
        """
        if isinstance(data, list):
            for index, item in enumerate(data):
                data[index] = _parse_data(self.fields, item)

        elif isinstance(data, dict):
            if not (all(isinstance(k, dict) for k in data.values()) and all(isinstance(k, dict) for k in self.fields.values())):
                for k, v in data.items():
                    _parse_data(self.fields, data[k])

            else:
                _parse_data(self.fields, data)
        return data