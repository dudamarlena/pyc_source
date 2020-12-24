# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ISEN\AppData\Local\Temp\pip-install-whg15vss\serial\serial\meta.py
# Compiled at: 2019-09-23 04:34:10
# Size of source mod 2**32: 27529 bytes
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
from utilities.compatibility import backport
backport()
from future.utils import native_str
import numbers, operator, re, collections
from collections import OrderedDict
from copy import copy, deepcopy
from itertools import chain
from numbers import Number
try:
    from typing import Optional, Dict, Sequence, Tuple, Mapping, Union, Any, List
except ImportError:
    Optional = Sequence = Dict = Tuple = Mapping = Union = Any = List = None

import serial
from serial.utilities import qualified_name, properties_values, collections_abc
from serial.abc.model import Model
from serial.abc.properties import Property
_DOT_SYNTAX_RE = re.compile('^\\d+(\\.\\d+)*$')

class Meta(object):

    def __copy__(self):
        new_instance = self.__class__()
        for a in dir(self):
            if a[0] != '_':
                v = getattr(self, a)
                isinstance(v, collections.Callable) or setattr(new_instance, a, v)

        return new_instance

    def __deepcopy__(self, memo=None):
        new_instance = self.__class__()
        for a, v in properties_values(self):
            setattr(new_instance, a, deepcopy(v, memo=memo))

        return new_instance

    def __bool__(self):
        return True

    def __repr__(self):
        return '\n'.join([
         '%s(' % qualified_name(type(self))] + ['    %s=%s,' % (p, repr(v)) for p, v in properties_values(self)] + [
         ')'])


class Version(Meta):

    def __init__(self, version_number=None, specification=None, equals=None, not_equals=None, less_than=None, less_than_or_equal_to=None, greater_than=None, greater_than_or_equal_to=None):
        if isinstance(version_number, str):
            if specification is None:
                if equals is None:
                    if not_equals is None:
                        if less_than is None:
                            if less_than_or_equal_to is None:
                                if greater_than is None:
                                    if greater_than_or_equal_to is None:
                                        specification = None
                                        for s in version_number.split('&'):
                                            if '==' in s:
                                                s, equals = s.split('==')
                                            else:
                                                if '<=' in s:
                                                    s, less_than_or_equal_to = s.split('<=')
                                                else:
                                                    if '>=' in s:
                                                        s, greater_than_or_equal_to = s.split('>=')
                                                    else:
                                                        if '<' in s:
                                                            s, less_than = s.split('<')
                                                        else:
                                                            if '>' in s:
                                                                s, greater_than = s.split('>')
                                                            else:
                                                                if '!=' in s:
                                                                    s, not_equals = s.split('!=')
                                                                else:
                                                                    if '=' in s:
                                                                        s, equals = s.split('=')
                                            if specification:
                                                if s != specification:
                                                    raise ValueError('Multiple specifications cannot be associated with an instance of `serial.meta.Version`: ' + repr(version_number))
                                                elif s:
                                                    specification = s

                                        self.specification = specification
        self.equals = equals
        self.not_equals = not_equals
        self.less_than = less_than
        self.less_than_or_equal_to = less_than_or_equal_to
        self.greater_than = greater_than
        self.greater_than_or_equal_to = greater_than_or_equal_to

    def __eq__(self, other):
        compare_properties_functions = (
         (
          'equals', operator.eq),
         (
          'not_equals', operator.ne),
         (
          'less_than', operator.lt),
         (
          'less_than_or_equal_to', operator.le),
         (
          'greater_than', operator.gt),
         (
          'greater_than_or_equal_to', operator.ge))
        if not isinstance(other, str) or _DOT_SYNTAX_RE.match(other) or isinstance(other, (collections_abc.Sequence, int)):
            if isinstance(other, (native_str, bytes, numbers.Number)):
                other = str(other)
            elif isinstance(other, str):
                other = other.rstrip('.0')
                if other == '':
                    other_components = (0, )
                else:
                    other_components = tuple((int(other_component) for other_component in other.split('.')))
            else:
                other_components = tuple(other)
            for compare_property, compare_function in compare_properties_functions:
                compare_value = getattr(self, compare_property)
                if compare_value is not None:
                    compare_values = tuple((int(n) for n in compare_value.split('.')))
                    other_values = copy(other_components)
                    ld = len(other_values) - len(compare_values)
                    if ld < 0:
                        other_values = tuple(chain(other_values, [0] * -ld))
                    else:
                        if ld > 0:
                            compare_values = tuple(chain(compare_values, [0] * ld))
                        return compare_function(other_values, compare_values) or False

        else:
            for compare_property, compare_function in compare_properties_functions:
                compare_value = getattr(self, compare_property)
                if compare_value is not None:
                    return compare_function(other, compare_value) or False

        return True

    def __str__(self):
        representation = []
        for property, operator in (('equals', '=='), ('not_equals', '!='), ('greater_than', '>'),
                                   ('greater_than_or_equal_to', '>='), ('less_than', '<'),
                                   ('less_than_or_equal_to', '<=')):
            v = getattr(self, property)
            if v is not None:
                representation.append(self.specification + operator + v)

        return '&'.join(representation)


class Object(Meta):

    def __init__(self, properties=None):
        self._properties = None
        self.properties = properties

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, properties_):
        self._properties = Properties(properties_)


class Dictionary(Meta):

    def __init__(self, value_types=None):
        self._value_types = None
        self.value_types = value_types

    @property
    def value_types(self):
        return self._value_types

    @value_types.setter
    def value_types(self, value_types):
        if value_types is not None:
            if isinstance(value_types, (type, Property)):
                value_types = (
                 value_types,)
            else:
                if native_str is not str:
                    if isinstance(value_types, collections.Callable):
                        _types = value_types

                        def value_types(d):
                            ts = _types(d)
                            if ts is not None:
                                if str in ts:
                                    if native_str not in ts:
                                        ts = tuple(chain(*(((t, native_str) if t is str else (t,)) for t in ts)))
                            return ts

                    else:
                        if str in value_types:
                            if native_str is not str:
                                if native_str not in value_types:
                                    value_types = chain(*(((t, native_str) if t is str else (t,)) for t in value_types))
                value_types = isinstance(value_types, collections_abc.Callable) or tuple(value_types)
        self._value_types = value_types


class Array(Meta):

    def __init__(self, item_types=None):
        self._item_types = None
        self.item_types = item_types

    @property
    def item_types(self):
        return self._item_types

    @item_types.setter
    def item_types(self, item_types):
        if item_types is not None:
            if isinstance(item_types, (type, Property)):
                item_types = (
                 item_types,)
            else:
                if native_str is not str:
                    if isinstance(item_types, collections.Callable):
                        _types = item_types

                        def item_types(d):
                            ts = _types(d)
                            if ts is not None:
                                if str in ts:
                                    if native_str not in ts:
                                        ts = tuple(chain(*(((t, native_str) if t is str else (t,)) for t in ts)))
                            return ts

                    else:
                        if str in item_types:
                            if native_str is not str:
                                if native_str not in item_types:
                                    item_types = chain(*(((t, native_str) if t is str else (t,)) for t in item_types))
                item_types = callable(item_types) or tuple(item_types)
        self._item_types = item_types


class Properties(OrderedDict):

    def __init__(self, items=None):
        if items is None:
            super().__init__()
        else:
            if isinstance(items, OrderedDict):
                items = items.items()
            else:
                if isinstance(items, dict):
                    items = sorted(items.items())
            super().__init__(items)

    def __setitem__(self, key, value):
        if not isinstance(value, Property):
            raise ValueError(value)
        super().__setitem__(key, value)

    def __copy__(self):
        return self.__class__(self)

    def __deepcopy__(self, memo=None):
        return self.__class__(tuple(((k, deepcopy(v, memo=memo)) for k, v in self.items())))

    def __repr__(self):
        representation = [
         qualified_name(type(self)) + '(']
        items = tuple(self.items())
        if len(items) > 0:
            representation[0] += '['
            for k, v in items:
                rv = qualified_name(v) if isinstance(v, type) else repr(v)
                rvls = rv.split('\n')
                if len(rvls) > 1:
                    rvs = [
                     rvls[0]]
                    for rvl in rvls[1:]:
                        rvs.append('        ' + rvl)

                    rv = '\n'.join(rvs)
                    representation += [
                     '    (',
                     '        %s,' % repr(k),
                     '        %s' % rv,
                     '    ),']
                else:
                    representation.append('    (%s, %s),' % (repr(k), rv))

            representation[-1] = representation[(-1)][:-1]
            representation.append(']')
        representation[(-1)] += ')'
        if len(representation) > 2:
            return '\n'.join(representation)
        return ''.join(representation)


def read(model):
    if isinstance(model, Model):
        return model._meta or read(type(model))
        if isinstance(model, type):
            if issubclass(model, Model):
                return model._meta
    else:
        try:
            repr_model = repr(model)
        except:
            repr_model = object.__repr__(model)

    raise TypeError('%s requires a parameter which is an instance or sub-class of `%s`, not%s' % (
     serial.utilities.calling_function_qualified_name(),
     qualified_name(Model),
     ':\n' + repr_model if '\n' in repr_model else ' `%s`' % repr_model))


def writable(model):
    if isinstance(model, Model):
        if model._meta is None:
            model._meta = deepcopy(writable(type(model)))
    elif isinstance(model, type):
        if issubclass(model, Model):
            if model._meta is None:
                model._meta = Object() if issubclass(model, serial.model.Object) else Array() if issubclass(model, serial.model.Array) else Dictionary() if issubclass(model, serial.model.Dictionary) else None
        else:
            for b in model.__bases__:
                if hasattr(b, '_meta') and model._meta is b._meta:
                    model._meta = deepcopy(model._meta)
                    break

    else:
        repr_model = repr(model)
        raise TypeError('%s requires a parameter which is an instance or sub-class of `%s`, not%s' % (
         serial.utilities.calling_function_qualified_name(),
         qualified_name(Model),
         ':\n' + repr_model if '\n' in repr_model else ' `%s`' % repr_model))
    return model._meta


def write(model, meta):
    if isinstance(model, Model):
        model_type = type(model)
    else:
        if isinstance(model, type):
            if issubclass(model, Model):
                model_type = model
            else:
                repr_model = repr(model)
                raise TypeError('%s requires a value for the parameter `model` which is an instance or sub-class of `%s`, not%s' % (
                 serial.utilities.calling_function_qualified_name(),
                 qualified_name(Model),
                 ':\n' + repr_model if '\n' in repr_model else ' `%s`' % repr_model))
        else:
            metadata_type = Object if issubclass(model_type, serial.model.Object) else Array if issubclass(model_type, serial.model.Array) else Dictionary if issubclass(model_type, serial.model.Dictionary) else None
            assert isinstance(meta, metadata_type), 'Metadata assigned to `%s` must be of type `%s`' % (
             qualified_name(model_type),
             qualified_name(metadata_type))
        model._meta = meta


_UNIDENTIFIED = None

def xpath(model, xpath_=_UNIDENTIFIED):
    """
    Return the xpath at which the element represented by this object was found, relative to the root document. If
    the parameter `xpath_` is provided--set the value
    """
    if not isinstance(model, Model):
        raise TypeError('`model` must be an instance of `%s`, not %s.' % (qualified_name(Model), repr(model)))
    elif xpath_ is not _UNIDENTIFIED:
        if not isinstance(xpath_, str):
            if isinstance(xpath_, native_str):
                xpath_ = str(xpath_)
            else:
                raise TypeError('`xpath_` must be a `str`, not %s.' % repr(xpath_))
        model._xpath = xpath_
        if isinstance(model, serial.model.Dictionary):
            for k, v in model.items():
                if isinstance(v, Model):
                    xpath(v, '%s/%s' % (xpath_, k))

    elif isinstance(model, serial.model.Object):
        for pn, p in read(model).properties.items():
            k = p.name or pn
            v = getattr(model, pn)
            if isinstance(v, Model):
                xpath(v, '%s/%s' % (xpath_, k))

    else:
        if isinstance(model, serial.model.Array):
            for i in range(len(model)):
                v = model[i]
                if isinstance(v, Model):
                    xpath(v, '%s[%s]' % (xpath_, str(i)))

    return model._xpath


def pointer(model, pointer_=_UNIDENTIFIED):
    if not isinstance(model, Model):
        raise TypeError('`model` must be an instance of `%s`, not %s.' % (qualified_name(Model), repr(model)))
    elif pointer_ is not _UNIDENTIFIED:
        if not isinstance(pointer_, (str, native_str)):
            raise TypeError('`pointer_` must be a `str`, not %s (of type `%s`).' % (repr(pointer_), type(pointer_).__name__))
        model._pointer = pointer_
        if isinstance(model, serial.model.Dictionary):
            for k, v in model.items():
                if isinstance(v, Model):
                    pointer(v, '%s/%s' % (pointer_, k.replace('~', '~0').replace('/', '~1')))

        else:
            if isinstance(model, serial.model.Object):
                for pn, property in read(model).properties.items():
                    k = property.name or pn
                    v = getattr(model, pn)
                    if isinstance(v, Model):
                        pointer(v, '%s/%s' % (pointer_, k.replace('~', '~0').replace('/', '~1')))

            else:
                if isinstance(model, serial.model.Array):
                    for i in range(len(model)):
                        v = model[i]
                        if isinstance(v, Model):
                            pointer(v, '%s[%s]' % (pointer_, str(i)))

    return model._pointer


def url--- This code section failed: ---

 L. 592         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'model'
                4  LOAD_GLOBAL              serial
                6  LOAD_ATTR                abc
                8  LOAD_ATTR                model
               10  LOAD_ATTR                Model
               12  CALL_FUNCTION_2       2  '2 positional arguments'
               14  POP_JUMP_IF_TRUE     40  'to 40'

 L. 593        16  LOAD_GLOBAL              TypeError

 L. 594        18  LOAD_STR                 '`model` must be an instance of `%s`, not %s.'
               20  LOAD_GLOBAL              qualified_name
               22  LOAD_GLOBAL              Model
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  LOAD_GLOBAL              repr
               28  LOAD_FAST                'model'
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  BUILD_TUPLE_2         2 
               34  BINARY_MODULO    
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            14  '14'

 L. 596        40  LOAD_FAST                'url_'
               42  LOAD_GLOBAL              _UNIDENTIFIED
               44  COMPARE_OP               is-not
               46  POP_JUMP_IF_FALSE   252  'to 252'

 L. 597        48  LOAD_GLOBAL              isinstance
               50  LOAD_FAST                'url_'
               52  LOAD_GLOBAL              str
               54  CALL_FUNCTION_2       2  '2 positional arguments'
               56  POP_JUMP_IF_TRUE     74  'to 74'

 L. 598        58  LOAD_GLOBAL              TypeError

 L. 599        60  LOAD_STR                 '`url_` must be a `str`, not %s.'
               62  LOAD_GLOBAL              repr
               64  LOAD_FAST                'url_'
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  BINARY_MODULO    
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            56  '56'

 L. 601        74  LOAD_FAST                'url_'
               76  LOAD_FAST                'model'
               78  STORE_ATTR               _url

 L. 602        80  LOAD_GLOBAL              isinstance
               82  LOAD_FAST                'model'
               84  LOAD_GLOBAL              serial
               86  LOAD_ATTR                model
               88  LOAD_ATTR                Dictionary
               90  CALL_FUNCTION_2       2  '2 positional arguments'
               92  POP_JUMP_IF_FALSE   134  'to 134'

 L. 603        94  SETUP_LOOP          252  'to 252'
               96  LOAD_FAST                'model'
               98  LOAD_METHOD              values
              100  CALL_METHOD_0         0  '0 positional arguments'
              102  GET_ITER         
            104_0  COME_FROM           116  '116'
              104  FOR_ITER            130  'to 130'
              106  STORE_FAST               'v'

 L. 604       108  LOAD_GLOBAL              isinstance
              110  LOAD_FAST                'v'
              112  LOAD_GLOBAL              Model
              114  CALL_FUNCTION_2       2  '2 positional arguments'
              116  POP_JUMP_IF_FALSE   104  'to 104'

 L. 605       118  LOAD_GLOBAL              url
              120  LOAD_FAST                'v'
              122  LOAD_FAST                'url_'
              124  CALL_FUNCTION_2       2  '2 positional arguments'
              126  POP_TOP          
              128  JUMP_BACK           104  'to 104'
              130  POP_BLOCK        
              132  JUMP_FORWARD        252  'to 252'
            134_0  COME_FROM            92  '92'

 L. 606       134  LOAD_GLOBAL              isinstance
              136  LOAD_FAST                'model'
              138  LOAD_GLOBAL              serial
              140  LOAD_ATTR                model
              142  LOAD_ATTR                Object
              144  CALL_FUNCTION_2       2  '2 positional arguments'
              146  POP_JUMP_IF_FALSE   204  'to 204'

 L. 607       148  SETUP_LOOP          252  'to 252'
              150  LOAD_GLOBAL              read
              152  LOAD_FAST                'model'
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  LOAD_ATTR                properties
              158  LOAD_METHOD              keys
              160  CALL_METHOD_0         0  '0 positional arguments'
              162  GET_ITER         
            164_0  COME_FROM           186  '186'
              164  FOR_ITER            200  'to 200'
              166  STORE_FAST               'pn'

 L. 608       168  LOAD_GLOBAL              getattr
              170  LOAD_FAST                'model'
              172  LOAD_FAST                'pn'
              174  CALL_FUNCTION_2       2  '2 positional arguments'
              176  STORE_FAST               'v'

 L. 609       178  LOAD_GLOBAL              isinstance
              180  LOAD_FAST                'v'
              182  LOAD_GLOBAL              Model
              184  CALL_FUNCTION_2       2  '2 positional arguments'
              186  POP_JUMP_IF_FALSE   164  'to 164'

 L. 610       188  LOAD_GLOBAL              url
              190  LOAD_FAST                'v'
              192  LOAD_FAST                'url_'
              194  CALL_FUNCTION_2       2  '2 positional arguments'
              196  POP_TOP          
              198  JUMP_BACK           164  'to 164'
              200  POP_BLOCK        
              202  JUMP_FORWARD        252  'to 252'
            204_0  COME_FROM           146  '146'

 L. 611       204  LOAD_GLOBAL              isinstance
              206  LOAD_FAST                'model'
              208  LOAD_GLOBAL              serial
              210  LOAD_ATTR                model
              212  LOAD_ATTR                Array
              214  CALL_FUNCTION_2       2  '2 positional arguments'
              216  POP_JUMP_IF_FALSE   252  'to 252'

 L. 612       218  SETUP_LOOP          252  'to 252'
              220  LOAD_FAST                'model'
              222  GET_ITER         
            224_0  COME_FROM           236  '236'
              224  FOR_ITER            250  'to 250'
              226  STORE_FAST               'v'

 L. 613       228  LOAD_GLOBAL              isinstance
              230  LOAD_FAST                'v'
              232  LOAD_GLOBAL              Model
              234  CALL_FUNCTION_2       2  '2 positional arguments'
              236  POP_JUMP_IF_FALSE   224  'to 224'

 L. 614       238  LOAD_GLOBAL              url
              240  LOAD_FAST                'v'
              242  LOAD_FAST                'url_'
              244  CALL_FUNCTION_2       2  '2 positional arguments'
              246  POP_TOP          
              248  JUMP_BACK           224  'to 224'
              250  POP_BLOCK        
            252_0  COME_FROM_LOOP      218  '218'
            252_1  COME_FROM           216  '216'
            252_2  COME_FROM           202  '202'
            252_3  COME_FROM_LOOP      148  '148'
            252_4  COME_FROM           132  '132'
            252_5  COME_FROM_LOOP       94  '94'
            252_6  COME_FROM            46  '46'

 L. 615       252  LOAD_FAST                'model'
              254  LOAD_ATTR                _url
              256  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 252


def format_(model, serialization_format=_UNIDENTIFIED):
    if not isinstance(model, Model):
        raise TypeError('`model` must be an instance of `%s`, not %s.' % (qualified_name(Model), repr(model)))
    elif serialization_format is not _UNIDENTIFIED:
        if not isinstance(serialization_format, str):
            if isinstance(serialization_format, native_str):
                serialization_format = str(serialization_format)
            else:
                raise TypeError('`serialization_format` must be a `str`, not %s.' % repr(serialization_format))
        model._format = serialization_format
        if isinstance(model, serial.model.Dictionary):
            for v in model.values():
                if isinstance(v, Model):
                    format_(v, serialization_format)

    elif isinstance(model, serial.model.Object):
        for pn in read(model).properties.keys():
            v = getattr(model, pn)
            if isinstance(v, Model):
                format_(v, serialization_format)

    else:
        if isinstance(model, serial.model.Array):
            for v in model:
                if isinstance(v, Model):
                    format_(v, serialization_format)

    return model._format


def version(data, specification, version_number):
    """
    Recursively alters model class or instance metadata based on version number metadata associated with an
    object's properties. This allows one data model to represent multiple versions of a specification and dynamically
    change based on the version of a specification represented.

    Arguments:

        - data (serial.abc.model.Model)

        - specification (str):

            The specification to which the `version_number` argument applies.

        - version_number (str|int|[int]):

            A version number represented as text (in the form of integers separated by periods), an integer, or a
            sequence of integers.
    """
    if not isinstance(data, serial.abc.model.Model):
        raise TypeError('The data provided is not an instance of serial.abc.model.Model: ' + repr(data))
    else:

        def version_match(property_):
            if property_.versions is not None:
                version_matched = False
                specification_matched = False
                for applicable_version in property_.versions:
                    if applicable_version.specification == specification:
                        specification_matched = True
                        if applicable_version == version_number:
                            version_matched = True
                            break

                if specification_matched:
                    if not version_matched:
                        return False
            return True

        def version_properties(properties_):
            changed = False
            nps = []
            for property in properties_:
                if isinstance(property, serial.properties.Property):
                    if version_match(property):
                        np = version_property(property)
                        if np is not property:
                            changed = True
                        nps.append(np)
                    else:
                        changed = True
                else:
                    nps.append(property)

            if changed:
                return tuple(nps)
            return

        def version_property(property):
            changed = False
            if isinstance(property, serial.properties.Array) and property.item_types is not None:
                item_types = version_properties(property.item_types)
                if item_types is not None:
                    if not changed:
                        property = deepcopy(property)
                    property.item_types = item_types
                    changed = True
            elif isinstance(property, serial.properties.Dictionary):
                if property.value_types is not None:
                    value_types = version_properties(property.value_types)
                    if value_types is not None:
                        if not changed:
                            property = deepcopy(property)
                        property.value_types = value_types
                        changed = True
            if property.types is not None:
                types = version_properties(property.types)
                if types is not None:
                    if not changed:
                        property = deepcopy(property)
                    property.types = types
            return property

        instance_meta = read(data)
        class_meta = read(type(data))
        if isinstance(data, serial.abc.model.Object):
            for property_name in tuple(instance_meta.properties.keys()):
                property = instance_meta.properties[property_name]
                if version_match(property):
                    np = version_property(property)
                    if np is not property:
                        if instance_meta is class_meta:
                            instance_meta = writable(data)
                        instance_meta.properties[property_name] = np
                    else:
                        if instance_meta is class_meta:
                            instance_meta = writable(data)
                        del instance_meta.properties[property_name]
                        version_ = getattr(data, property_name)
                        if version_ is not None:
                            raise serial.errors.VersionError('%s - the property `%s` is not applicable in %s version %s:\n%s' % (
                             qualified_name(type(data)),
                             property_name,
                             specification,
                             version_number,
                             str(data)))
                        value = getattr(data, property_name)
                        if isinstance(value, serial.abc.model.Model):
                            version(value, specification, version_number)

        else:
            if isinstance(data, serial.abc.model.Dictionary):
                if instance_meta:
                    if instance_meta.value_types:
                        new_value_types = version_properties(instance_meta.value_types)
                        if new_value_types:
                            if instance_meta is class_meta:
                                instance_meta = writable(data)
                            instance_meta.value_types = new_value_types
                for value in data.values():
                    if isinstance(value, serial.abc.model.Model):
                        version(value, specification, version_number)

            else:
                if isinstance(data, serial.abc.model.Array):
                    if instance_meta:
                        if instance_meta.item_types:
                            new_item_types = version_properties(instance_meta.item_types)
                            if new_item_types:
                                if instance_meta is class_meta:
                                    instance_meta = writable(data)
                                instance_meta.item_types = new_item_types
                    for item in data:
                        if isinstance(item, serial.abc.model.Model):
                            version(item, specification, version_number)