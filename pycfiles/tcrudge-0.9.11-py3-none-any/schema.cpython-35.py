# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/app/tcrudge/utils/schema.py
# Compiled at: 2017-01-07 15:24:53
# Size of source mod 2**32: 8999 bytes
import copy, json
from collections import defaultdict
from warnings import warn
JS_TYPES = {dict: 'object', 
 list: 'array', 
 str: 'string', 
 type(''): 'string', 
 int: 'integer', 
 float: 'number', 
 bool: 'boolean', 
 type(None): 'null'}
PEEWEE_TYPES = {'SERIAL': [
            {'type': 'integer'},
            {'type': 'string', 'pattern': '^[+-]?[0-9]+$'}], 
 
 'TEXT': 'string', 
 'TIMESTAMP': 'string', 
 'BOOLEAN': 'boolean', 
 'JSONB': 'object', 
 'JSON': 'object', 
 'INTEGER': [
             {'type': 'integer'},
             {'type': 'string', 'pattern': '^[+-]?[0-9]+$'}], 
 
 'REAL': [
          {'type': 'number'},
          {'type': 'string', 'pattern': '^[+-]?([0-9]*[.])?[0-9]+$'}], 
 
 'NUMERIC': [
             {'type': 'number'},
             {'type': 'string', 'pattern': '^[+-]?([0-9]*[.])?[0-9]+$'}]}
JS_TYPES.update(PEEWEE_TYPES)

class Schema(object):
    __doc__ = '\n    Basic schema generator class. Schema objects can be loaded up\n    with existing schemas and objects before being serialized.\n    '

    @classmethod
    def create_default_schema(cls):
        sch = cls()
        sch.add_schema({'type': 'object', 'properties': {}, 
         'additionalProperties': False})
        return sch

    def __init__(self, merge_arrays=True):
        """
        Builds a schema generator object.
        arguments:
        * `merge_arrays` (default `True`): Assume all array items share
          the same schema (as they should). The alternate behavior is to
          merge schemas based on position in the array.
        """
        self._options = {'merge_arrays': merge_arrays}
        self._type = []
        self._required = None
        self._properties = defaultdict(lambda : Schema(**self._options))
        self._items = None
        self._other = {}

    def add_schema(self, schema):
        """
        Merges in an existing schema.
        arguments:
        * `schema` (required - `dict` or `Schema`):
          an existing JSON Schema to merge.
        """
        if isinstance(schema, Schema):
            schema = schema.to_dict()
        for prop, val in schema.items():
            if prop == 'type':
                self._add_type(val)
            elif prop == 'required':
                self._add_required(val)
            elif prop == 'properties':
                self._add_properties(val, 'add_schema')
            else:
                if prop == 'items':
                    self._add_items(val, 'add_schema')
                else:
                    if prop not in self._other:
                        self._other[prop] = val
                    elif self._other[prop] != val:
                        warn('Schema incompatible. Keyword {0!r} has conflicting values ({1!r} vs. {2!r}). Using {1!r}'.format(prop, self._other[prop], val))

        if 'required' not in schema:
            self._add_required([])
        return self

    def add_object(self, obj):
        """
        Modify the schema to accomodate an object.
        arguments:
        * `obj` (required - `dict`):
          a JSON object to use in generate the schema.
        """
        if isinstance(obj, dict):
            self._generate_object(obj)
        else:
            if isinstance(obj, list):
                self._generate_array(obj)
            else:
                self._generate_basic(obj)
        return self

    def to_dict(self, recurse=True):
        """
        Convert the current schema to a `dict`.
        """
        schema = dict(self._other)
        if self._type:
            if isinstance(self._get_type(), dict):
                schema = self._get_type()
            else:
                schema['type'] = self._get_type()
            if 'object' in self._type:
                pass
            properties = copy.deepcopy(self._get_properties(recurse))
            for key_prop, val_prop in self._get_properties(recurse).items():
                if isinstance(val_prop.get('type'), list):
                    res = {'anyOf': []}
                    for it in val_prop['type']:
                        if isinstance(it, dict):
                            res['anyOf'].append(it)
                        else:
                            res['anyOf'].append({'type': it})

                    properties[key_prop] = res

            schema['properties'] = properties
            if self._required:
                schema['required'] = self._get_required()
        elif 'array' in self._type:
            items = self._get_items(recurse)
        if items or isinstance(items, dict):
            schema['items'] = items
        return schema

    def to_json(self, *args, **kwargs):
        """
        Convert the current schema directly to serialized JSON.
        """
        return json.dumps(self.to_dict(), *args, **kwargs)

    def __eq__(self, other):
        """required for comparing array items to ensure there aren't duplicates
        """
        if not isinstance(other, Schema):
            return False
        if self._get_type() != other._get_type():
            return False
        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        return not self.__eq__(other)

    def _get_type(self):
        schema_type = self._type[:]
        if 'integer' in schema_type and 'number' in schema_type:
            schema_type.remove('integer')
        if len(schema_type) == 1:
            schema_type, = schema_type
        return schema_type

    def _get_required(self):
        if self._required:
            return sorted(self._required)
        return []

    def _get_properties(self, recurse=True):
        if not recurse:
            return dict(self._properties)
        properties = {}
        for prop, subschema in self._properties.items():
            properties[prop] = subschema.to_dict()

        return properties

    def _get_items(self, recurse=True):
        if not recurse:
            return self._items
        else:
            if self._options['merge_arrays']:
                return self._items.to_dict()
            return [subschema.to_dict() for subschema in self._items]

    def _add_type(self, val_type):
        if isinstance(val_type, (str, dict)):
            if val_type not in self._type:
                self._type.append(val_type)
        else:
            if isinstance(val_type, list):
                for el in val_type:
                    if el not in self._type:
                        self._type.append(el)

            else:
                self._type = list(set(self._type) | set(val_type))

    def _add_required(self, required):
        if self._required is None:
            self._required = set(required)
        else:
            self._required |= set(required)

    def _add_properties(self, properties, func):
        for prop, val in properties.items():
            getattr(self._properties[prop], func)(val)

    def _add_items(self, items, func):
        if self._options['merge_arrays']:
            self._add_items_merge(items, func)
        else:
            self._add_items_sep(items, func)

    def _add_items_merge(self, items, func):
        if not self._items:
            self._items = Schema(**self._options)
        method = getattr(self._items, func)
        for item in items:
            method(item)

    def _add_items_sep(self, items, func):
        if not self._items:
            self._items = []
        while len(self._items) < len(items):
            self._items.append(Schema(**self._options))

        for subschema, item in zip(self._items, items):
            getattr(subschema, func)(item)

    def _generate_object(self, obj):
        self._add_type('object')
        self._add_properties(obj, 'add_object')

    def _generate_array(self, array):
        self._add_type('array')
        self._add_items(array, 'add_object')

    def _generate_basic(self, val):
        if val in JS_TYPES.keys():
            val_type = JS_TYPES[val]
        else:
            val_type = JS_TYPES[type(val)]
        self._add_type(val_type)