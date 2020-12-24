# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ISEN\AppData\Local\Temp\pip-install-whg15vss\serial\serial\properties.py
# Compiled at: 2019-09-23 04:34:10
# Size of source mod 2**32: 29488 bytes
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
from utilities.compatibility import backport
backport()
from future.utils import native_str
import numbers
from base64 import b64decode, b64encode
from copy import deepcopy
from datetime import date, datetime
try:
    from typing import Union, Optional, Sequence, Mapping, Set, Sequence, Callable, Dict, Any, Hashable, Collection, Tuple
except ImportError:
    Union = Optional = Sequence = Mapping = Set = Sequence = Callable = Dict = Any = Hashable = Collection = Tuple = Iterable = None

import iso8601
from .utilities import collections, collections_abc, qualified_name, properties_values, parameters_defaults, calling_function_qualified_name
from serial import abc, errors, meta
import serial
NoneType = type(None)
NULL = None

class Null(object):
    __doc__ = '\n    Instances of this class represent an *explicit* null value, rather than the absence of a\n    property/attribute/element, as would be inferred from a value of `None`.\n    '

    def __init__(self):
        if NULL is not None:
            raise errors.DefinitionExistsError('%s may only be defined once.' % repr(self))

    def __bool__(self):
        return False

    def __eq__(self, other):
        return id(other) == id(self)

    def __hash__(self):
        return 0

    def __str__(self):
        return 'null'

    def _marshal(self):
        pass

    def __repr__(self):
        if self.__module__ in ('__main__', 'builtins', '__builtin__'):
            return 'NULL'
        return '%s.NULL' % self.__module__

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self


NULL = Null()

def _validate_type_or_property(type_or_property):
    if not isinstance(type_or_property, (type, Property)):
        raise TypeError(type_or_property)
    if not type_or_property is Null:
        if isinstance(type_or_property, type) and not issubclass(type_or_property, (
         abc.model.Model,
         str,
         native_str,
         bytes,
         numbers.Number,
         date,
         datetime,
         Null,
         collections_abc.Iterable,
         dict,
         collections.OrderedDict,
         bool)) or isinstance(type_or_property, Property):
            raise TypeError(type_or_property)
    return type_or_property


class Types(list):
    __doc__ = '\n    Instances of this class are lists which will only take values which are valid types for describing a property\n    definition.\n    '

    def __init__(self, property_, items=None):
        if not isinstance(property_, Property):
            raise TypeError('The parameter `property` must be a `type`, or an instance of `%s`.' % qualified_name(Property))
        else:
            self.property_ = property_
            if isinstance(items, (type, Property)):
                items = (
                 items,)
            if items is None:
                super().__init__()
            else:
                super().__init__(items)

    def __setitem__(self, index, value):
        super().__setitem__(index, _validate_type_or_property(value))
        if value is str:
            if native_str is not str:
                if native_str not in self:
                    super().append(native_str)

    def append(self, value):
        super().append(_validate_type_or_property(value))
        if value is str:
            if native_str is not str:
                if native_str not in self:
                    super().append(native_str)

    def __delitem__(self, index):
        value = self[index]
        super().__delitem__(index)
        if value is str:
            if native_str in self:
                self.remove(native_str)

    def pop(self, index=-1):
        value = super().pop(index)
        if value is str:
            if native_str in self:
                self.remove(native_str)
        return value

    def __copy__(self):
        return self.__class__(self.property_, self)

    def __deepcopy__(self, memo=None):
        return self.__class__(self.property_, tuple((deepcopy(v, memo=memo) for v in self)))

    def __repr__(self):
        representation = [
         qualified_name(type(self)) + '(']
        if self:
            representation[0] += '['
            for v in self:
                rv = qualified_name(v) if isinstance(v, type) else repr(v)
                rvls = rv.split('\n')
                if len(rvls) > 1:
                    rvs = [rvls[0]]
                    for rvl in rvls[1:]:
                        rvs.append('    ' + rvl)

                    rv = '\n'.join(rvs)
                    representation += [
                     '    %s' % rv]
                else:
                    representation.append('    %s,' % rv)

            representation[-1] = representation[(-1)][:-1]
            representation.append(']')
        representation[(-1)] += ')'
        if len(representation) > 2:
            return '\n'.join(representation)
        return ''.join(representation)


class Property(object):
    __doc__ = '\n    This is the base class for defining a property.\n\n    Properties\n\n        - value_types ([type|Property]): One or more expected value_types or `Property` instances. Values are checked,\n          sequentially, against each type or `Property` instance, and the first appropriate match is used.\n\n        - required (bool|collections.Callable): If `True`--dumping the json_object will throw an error if this value\n          is `None`.\n\n        - versions ([str]|{str:Property}): The property should be one of the following:\n\n            - A set/tuple/list of version numbers to which this property applies.\n            - A mapping of version numbers to an instance of `Property` applicable to that version.\n\n          Version numbers prefixed by "<" indicate any version less than the one specified, so "<3.0" indicates that\n          this property is available in versions prior to 3.0. The inverse is true for version numbers prefixed by ">".\n          ">=" and "<=" have similar meanings, but are inclusive.\n\n          Versioning can be applied to an json_object by calling `serial.meta.set_version` in the `__init__` method of\n          an `serial.model.Object` sub-class. For an example, see `oapi.model.OpenAPI.__init__`.\n\n        - name (str): The name of the property when loaded from or dumped into a JSON/YAML/XML json_object. Specifying a\n          `name` facilitates mapping of PEP8 compliant property to JSON or YAML attribute names, or XML element names,\n          which are either camelCased, are python keywords, or otherwise not appropriate for usage in python code.\n\n    '

    def __init__(self, types=None, name=None, required=False, versions=None):
        self._types = None
        self.types = types
        self.name = name
        self.required = required
        self._versions = None
        self.versions = versions

    @property
    def types(self):
        return self._types

    @types.setter
    def types(self, types_or_properties):
        if types_or_properties is not None:
            if callable(types_or_properties):
                if native_str is not str:
                    _types_or_properties = types_or_properties

                    def types_or_properties(d):
                        return Types(self, _types_or_properties(d))

            else:
                types_or_properties = Types(self, types_or_properties)
        self._types = types_or_properties

    @property
    def versions(self):
        return self._versions

    @versions.setter
    def versions(self, versions):
        if versions is not None:
            if isinstance(versions, (str, Number, meta.Version)):
                versions = (
                 versions,)
            if isinstance(versions, collections_abc.Iterable):
                versions = tuple(((v if isinstance(v, meta.Version) else meta.Version(v)) for v in versions))
            else:
                repr_versions = repr(versions)
                raise TypeError('`%s` requires a sequence of version strings or ' % calling_function_qualified_name() + '`%s` instances, not' % qualified_name(meta.Version) + (':\n' + repr_versions if '\n' in repr_versions else ' `%s`.' % repr_versions))
        self._versions = versions

    def unmarshal(self, data):
        if isinstance(data, collections_abc.Iterable):
            if not isinstance(data, (
             str, bytes, bytearray, native_str)):
                if not isinstance(data, abc.model.Model):
                    if isinstance(data, (dict, collections.OrderedDict)):
                        for k, v in data.items():
                            if v is None:
                                data[k] = NULL

                    else:
                        data = tuple(((NULL if i is None else i) for i in data))
        return serial.marshal.unmarshal(data, types=(self.types))

    def marshal(self, data):
        return serial.marshal.marshal(data, types=(self.types))

    def __repr__(self):
        representation = [
         qualified_name(type(self)) + '(']
        pd = parameters_defaults(self.__init__)
        for p, v in properties_values(self):
            if p not in pd or pd[p] == v:
                continue
            if v is not None and v is not NULL:
                if isinstance(v, collections_abc.Sequence):
                    rvs = isinstance(v, (str, bytes)) or [
                     '(']
                    for i in v:
                        ri = qualified_name(i) if isinstance(i, type) else "'%s'" % str(i) if isinstance(i, meta.Version) else repr(i)
                        rils = ri.split('\n')
                        if len(rils) > 1:
                            ris = [
                             rils[0]]
                            for ril in rils[1:]:
                                ris.append('        ' + ril)

                            ri = '\n'.join(ris)
                        rvs.append('        %s,' % ri)

                    if len(v) > 1:
                        rvs[-1] = rvs[(-1)][:-1]
                    rvs.append('    )')
                    rv = '\n'.join(rvs)
                else:
                    rv = qualified_name(v) if isinstance(v, type) else "'%s'" % str(v) if isinstance(v, meta.Version) else repr(v)
                    rvls = rv.split('\n')
                    if len(rvls) > 2:
                        rvs = [
                         rvls[0]]
                        for rvl in rvls[1:]:
                            rvs.append('    ' + rvl)

                        rv = '\n'.join(rvs)
                    representation.append('    %s=%s,' % (p, rv))

        representation.append(')')
        if len(representation) > 2:
            return '\n'.join(representation)
        return ''.join(representation)

    def __copy__(self):
        new_instance = self.__class__()
        for a in dir(self):
            if a[0] != '_' and a != 'data':
                v = getattr(self, a)
                callable(v) or setattr(new_instance, a, v)

        return new_instance

    def __deepcopy__(self, memo):
        new_instance = self.__class__()
        for a, v in properties_values(self):
            setattr(new_instance, a, deepcopy(v, memo))

        return new_instance


abc.properties.Property.register(Property)

class String(Property):
    __doc__ = '\n    See `serial.properties.Property`\n    '

    def __init__(self, name=None, required=False, versions=None):
        super().__init__(types=(
         str,),
          name=name,
          required=required,
          versions=versions)


class Date(Property):
    __doc__ = '\n    See `serial.properties.Property`\n\n    Additional Properties:\n\n        - marshal (collections.Callable): A function, taking one argument (a python `date` json_object), and returning\n          a date string in the desired format. The default is `date.isoformat`--returning an iso8601 compliant date\n          string.\n\n        - unmarshal (collections.Callable): A function, taking one argument (a date string), and returning a python\n          `date` json_object. By default, this is `iso8601.parse_date`.\n    '

    def __init__(self, name=None, required=False, versions=None, date2str=date.isoformat, str2date=iso8601.parse_date):
        super().__init__(types=(
         date,),
          name=name,
          required=required,
          versions=versions)
        self.date2str = date2str
        self.str2date = str2date

    def unmarshal(self, data):
        if data is None:
            return data
        elif isinstance(data, date):
            date_ = data
        else:
            if isinstance(data, str):
                date_ = self.str2date(data)
            else:
                raise TypeError('%s is not a `str`.' % repr(data))
        if isinstance(date_, date):
            return date_
        raise TypeError('"%s" is not a properly formatted date string.' % data)

    def marshal(self, data):
        if data is None:
            return data
            ds = self.date2str(data)
            if not isinstance(ds, str):
                if isinstance(ds, native_str):
                    ds = str(ds)
        else:
            raise TypeError('The date2str function should return a `str`, not a `%s`: %s' % (
             type(ds).__name__,
             repr(ds)))
        return ds


class DateTime(Property):
    __doc__ = '\n    See `serial.properties.Property`\n\n    Additional Properties:\n\n        - marshal (collections.Callable): A function, taking one argument (a python `datetime` json_object), and\n          returning a date-time string in the desired format. The default is `datetime.isoformat`--returning an\n          iso8601 compliant date-time string.\n\n        - unmarshal (collections.Callable): A function, taking one argument (a datetime string), and returning a python\n          `datetime` json_object. By default, this is `iso8601.parse_date`.\n    '

    def __init__(self, name=None, required=False, versions=None, datetime2str=datetime.isoformat, str2datetime=iso8601.parse_date):
        self.datetime2str = datetime2str
        self.str2datetime = str2datetime
        super().__init__(types=(
         datetime,),
          name=name,
          required=required,
          versions=versions)

    def unmarshal(self, data):
        if data is None:
            return data
        elif isinstance(data, datetime):
            datetime_ = data
        else:
            if isinstance(data, str):
                datetime_ = self.str2datetime(data)
            else:
                raise TypeError('%s is not a `str`.' % repr(data))
        if isinstance(datetime_, datetime):
            return datetime_
        raise TypeError('"%s" is not a properly formatted date-time string.' % data)

    def marshal(self, data):
        if data is None:
            return data
            datetime_string = self.datetime2str(data)
            if not isinstance(datetime_string, str):
                if isinstance(datetime_string, native_str):
                    datetime_string = str(datetime_string)
        else:
            repr_datetime_string = repr(datetime_string).strip()
            raise TypeError('The datetime2str function should return a `str`, not:' + ('\n' if '\n' in repr_datetime_string else ' ') + repr_datetime_string)
        return datetime_string


class Bytes(Property):
    __doc__ = '\n    See `serial.properties.Property`\n    '

    def __init__(self, name=None, required=False, versions=None):
        super().__init__(types=(
         bytes, bytearray),
          name=name,
          required=required,
          versions=versions)

    def unmarshal(self, data):
        """
        Un-marshal a base-64 encoded string into bytes
        """
        if data is None:
            return data
        if isinstance(data, str):
            return b64decode(data)
        if isinstance(data, bytes):
            return data
        raise TypeError('`data` must be a base64 encoded `str` or `bytes`--not `%s`' % qualified_name(type(data)))

    def marshal(self, data):
        """
        Marshal bytes into a base-64 encoded string
        """
        if data is None or isinstance(data, str):
            return data
        if isinstance(data, bytes):
            return str(b64encode(data), 'ascii')
        raise TypeError('`data` must be a base64 encoded `str` or `bytes`--not `%s`' % qualified_name(type(data)))


class Enumerated(Property):
    __doc__ = '\n    See `serial.properties.Property`...\n\n    + Properties:\n\n        - values ([Any]):  A list of possible values. If the parameter `types` is specified--typing is\n          applied prior to validation.\n    '

    def __init__(self, types=None, values=None, name=None, required=False, versions=None):
        self._values = None
        super().__init__(types=types,
          name=name,
          required=required,
          versions=versions)
        self.values = values

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        if not values is None:
            if not callable(values):
                if values is not None:
                    if not isinstance(values, (collections_abc.Sequence, collections_abc.Set)):
                        raise TypeError('`values` must be a finite set or sequence, not `%s`.' % qualified_name(type(values)))
                if values is not None:
                    values = [serial.marshal.unmarshal(v, types=(self.types)) for v in values]
        self._values = values

    def unmarshal(self, data):
        if self.types is not None:
            data = serial.marshal.unmarshal(data, types=(self.types))
        if data is not None:
            if self.values is not None:
                if data not in self.values:
                    raise ValueError('The value provided is not a valid option:\n%s\n\n' % repr(data) + 'Valid options include:\n%s' % ', '.join((repr(t) for t in self.values)))
        return data


class Number(Property):
    __doc__ = '\n    See `serial.properties.Property`\n    '

    def __init__(self, name=None, required=False, versions=None):
        super().__init__(types=(
         numbers.Number,),
          name=name,
          required=required,
          versions=versions)


class Integer(Property):
    __doc__ = '\n    See `serial.properties.Property`\n    '

    def __init__(self, name=None, required=False, versions=None):
        super().__init__(types=(
         int,),
          name=name,
          required=required,
          versions=versions)


class Boolean(Property):
    __doc__ = '\n    See `serial.properties.Property`\n    '

    def __init__(self, name=None, required=False, versions=None):
        super().__init__(types=(
         bool,),
          name=name,
          required=required,
          versions=versions)


class Array(Property):
    __doc__ = '\n    See `serial.properties.Property`...\n\n    + Properties:\n\n        - item_types (type|Property|[type|Property]): The type(s) of values/objects contained in the array. Similar to\n          `serial.properties.Property().value_types`, but applied to items in the array, not the array itself.\n    '

    def __init__(self, item_types=None, name=None, required=False, versions=None):
        self._item_types = None
        self.item_types = item_types
        super().__init__(types=(
         serial.model.Array,),
          name=name,
          required=required,
          versions=versions)

    def unmarshal(self, data):
        return serial.marshal.unmarshal(data, types=(self.types), item_types=(self.item_types))

    def marshal(self, data):
        return serial.marshal.marshal(data, types=(self.types), item_types=(self.item_types))

    @property
    def item_types(self):
        return self._item_types

    @item_types.setter
    def item_types(self, item_types):
        if item_types is not None:
            if callable(item_types):
                if native_str is not str:
                    _item_types = item_types

                    def item_types(d):
                        return Types(self, _item_types(d))

            else:
                item_types = Types(self, item_types)
        self._item_types = item_types


class Dictionary(Property):
    __doc__ = '\n    See `serial.properties.Property`...\n\n    + Properties:\n\n        - value_types (type|Property|[type|Property]): The type(s) of values/objects comprising the mapped\n          values. Similar to `serial.properties.Property.types`, but applies to *values* in the dictionary\n          object, not the dictionary itself.\n    '

    def __init__(self, value_types=None, name=None, required=False, versions=None):
        self._value_types = None
        self.value_types = value_types
        super().__init__(types=(
         serial.model.Dictionary,),
          name=name,
          required=required,
          versions=versions)

    def unmarshal(self, data):
        return serial.marshal.unmarshal(data, types=(self.types), value_types=(self.value_types))

    @property
    def value_types(self):
        return self._value_types

    @value_types.setter
    def value_types(self, value_types_):
        """
        The `types` can be either:

            - A sequence of types and/or `serial.properties.Property` instances.

            - A function which accepts exactly one argument (a dictionary), and which returns a sequence of types and/or
              `serial.properties.Property` instances.

        If more than one type or property definition is provided, un-marshalling is attempted using each `value_type`,
        in sequential order. If a value could be cast into more than one of the `types` without throwing a
        `ValueError`, `TypeError`, or `serial.errors.ValidationError`, the value type occuring *first* in the sequence
        will be used.
        """
        if value_types_ is not None:
            if callable(value_types_):
                if native_str is not str:
                    original_value_types_ = value_types_

                    def value_types_(data):
                        return Types(self, original_value_types_(data))

            else:
                value_types_ = Types(self, value_types_)
        self._value_types = value_types_