# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tornado_swirl/openapi/types.py
# Compiled at: 2019-12-17 19:27:20
# Size of source mod 2**32: 6266 bytes
"""OpenAPI Types

Use the Type class to determine the OpenAPI data type.

"""

class SchemaMixin(object):
    __doc__ = 'Schema mixin type for schema value'

    @property
    def schema(self):
        """Gets the type schema details"""
        schema = {'type': self.name}
        if self.format:
            schema.update({'format': self.format})
        if self.kwargs:
            schema.update(self.kwargs)
        return schema


class Type(object):
    __doc__ = 'Represents an open api type'

    def __new__(cls, val, *args, **kwargs):
        instance = (Type._determine_type)((str(val).strip()), **kwargs)
        if instance:
            return instance
        return (super(Type, cls).__new__)(cls, *args, **kwargs)

    def __init__(self, val, **kwargs):
        self.name = val
        self.format = None
        self.kwargs = kwargs

    @staticmethod
    def _determine_type(val, **kwargs):
        if not val == '':
            if val is None:
                return NoneType()
            if val.startswith('['):
                if val.endswith(']'):
                    return ArrayType((val[1:-1]), **kwargs)
            if val.startswith('enum['):
                if val.endswith(']'):
                    return EnumType(val[5:-1])
            if val.startswith('oneOf['):
                if val.endswith(']'):
                    return CombineType('oneOf', val[6:-1])
            if val.startswith('anyOf['):
                if val.endswith(']'):
                    return CombineType('anyOf', val[6:-1])
        else:
            if val.startswith('allOf['):
                if val.endswith(']'):
                    return CombineType('allOf', val[6:-1])
            if val.startswith('not[') and val.endswith(']'):
                return CombineType('not', val[4:-1])
        return (Type._get_builtin_type)(val, **kwargs)

    @staticmethod
    def _get_builtin_type(val, **kwargs):
        dtype = val
        dformat = None
        colon = val.find(':')
        if colon > 1:
            dtype = val[:colon]
            dformat = val[colon + 1:]
        if dtype in ('int', 'integer', 'int32'):
            return IntType(dtype, dformat, **kwargs)
        if dtype == 'file':
            return FileType(dformat, **kwargs)
        if dtype in ('long', 'int64'):
            return IntType(dtype, dformat, **kwargs)
        if dtype in ('number', 'float', 'double'):
            return NumberType(dtype, dformat, **kwargs)
        if dtype in ('string', 'str', 'date', 'date-time', 'password', 'byte', 'binary',
                     'email', 'uuid', 'uri', 'hostname', 'ipv4', 'ipv6'):
            return StringType(dtype, dformat, **kwargs)
        if dtype in ('bool', 'boolean'):
            return BoolType()
        if dtype == 'object':
            return ObjectType(**kwargs)
        return ModelType(dtype)

    @property
    def schema(self):
        """Override"""
        pass


class FileType(object):
    __doc__ = 'File type'

    def __init__(self, contents, **kwargs):
        self.name = 'file'
        self.contents = contents
        self.kwargs = kwargs

    @property
    def schema(self):
        """Returns file schema details"""
        return {'type':'string', 
         'format':'binary'}


class ArrayType(object):
    __doc__ = 'Array/List type'

    def __init__(self, contents, **kwargs):
        self.name = 'array'
        self.items_type = Type(contents)
        self.kwargs = kwargs

    @property
    def schema(self):
        """Returns array schema details"""
        return {'type':'array', 
         'items':self.items_type.schema}


class CombineType(object):
    __doc__ = 'Combine type: anyof allof oneof not'

    def __init__(self, name, contents, **kwargs):
        self.name = name
        self.vals = []
        vals = contents.strip().split(',')
        self.vals = [Type(val.strip()) for val in vals]
        self.kwargs = kwargs

    @property
    def schema(self):
        """Returns combine type schema"""
        return {self.name: [x.schema for x in self.vals]}


class NoneType(object):
    __doc__ = 'None type for None/null'

    def __init__(self, **kwargs):
        self.name = 'None'
        self.kwargs = kwargs

    @property
    def schema(self):
        """Schema none"""
        pass


class BoolType(SchemaMixin):
    __doc__ = 'Boolean type'

    def __init__(self, **kwargs):
        self.name = 'boolean'
        self.kwargs = kwargs
        self.format = None


class ObjectType(SchemaMixin):
    __doc__ = 'Object type -- freeform'

    def __init__(self, **kwargs):
        self.name = 'object'
        self.kwargs = kwargs
        self.kwargs.update({'additionalProperties': True})
        self.format = None


class IntType(SchemaMixin):
    __doc__ = 'Integer type'

    def __init__(self, name, dformat, **kwargs):
        self.name = 'integer'
        self.format = None
        if name == 'long':
            self.format = 'int64'
        else:
            if name in ('int32', 'int64'):
                self.format = name
            else:
                if dformat:
                    self.format = dformat
        self.kwargs = kwargs


class NumberType(SchemaMixin):
    __doc__ = 'Number Type'

    def __init__(self, name, dformat, **kwargs):
        self.name = 'number'
        self.format = None
        if name in ('float', 'double'):
            self.format = name
        else:
            if dformat:
                self.format = dformat
        self.kwargs = kwargs


class StringType(SchemaMixin):
    __doc__ = 'String type'

    def __init__(self, name, dformat, **kwargs):
        self.name = 'string'
        self.format = None
        if name in ('date', 'date-time', 'password', 'byte', 'binary', 'email', 'uuid',
                    'uri', 'hostname', 'ipv4', 'ipv6'):
            self.format = name
        else:
            if dformat:
                self.format = dformat
        self.kwargs = kwargs


class EnumType(SchemaMixin):
    __doc__ = 'Enum type'

    def __init__(self, values):
        self.name = 'string'
        self.format = None
        vals = values.strip().split(',')
        vals = [val.strip() for val in vals]
        self.kwargs = {'enum': vals}


class ModelType(object):
    __doc__ = 'Model type'

    def __init__(self, name):
        self.name = name

    @property
    def schema(self):
        """Model schema ref"""
        return {'$ref': '#/components/schemas/' + self.name}