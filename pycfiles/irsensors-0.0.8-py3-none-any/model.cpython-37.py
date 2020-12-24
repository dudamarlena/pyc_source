# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ISEN\AppData\Local\Temp\pip-install-whg15vss\serial\serial\model.py
# Compiled at: 2019-09-23 04:34:10
# Size of source mod 2**32: 41874 bytes
"""
This module defines the building blocks of a `serial` based data model.
"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
from utilities.compatibility import backport, BACKWARDS_COMPATIBILITY_IMPORTS
backport()
from future.utils import native_str
import re, sys
from urllib.parse import urljoin
from copy import deepcopy
from io import IOBase
from itertools import chain
from numbers import Number
from .utilities import qualified_name, collections, Generator
from . import properties, meta, errors, hooks, abc
from .marshal import marshal, unmarshal, serialize, detect_format, validate, UNMARSHALLABLE_TYPES
try:
    from typing import Union, Dict, Any, AnyStr, IO, Sequence, Mapping, Callable, Tuple, Optional, Set
except ImportError:
    Union = Dict = Any = AnyStr = IO = Sequence = Mapping = Callable = Tuple = Optional = Set = None

class Object(object):
    _format = None
    _meta = None
    _hooks = None

    def __init__(self, _=None):
        self._meta = None
        self._hooks = None
        self._url = None
        self._xpath = None
        self._pointer = None
        url = None
        if _ is not None:
            if isinstance(_, Object):
                instance_meta = meta.read(_)
                if meta.read(self) is not instance_meta:
                    meta.write(self, deepcopy(instance_meta))
                instance_hooks = hooks.read(_)
                if hooks.read(self) is not instance_hooks:
                    hooks.write(self, deepcopy(instance_hooks))
                for property_name in instance_meta.properties.keys():
                    try:
                        setattr(self, property_name, getattr(_, property_name))
                    except TypeError as error:
                        try:
                            label = '\n - %s.%s: ' % (qualified_name(type(self)), property_name)
                            if error.args:
                                error.args = tuple(chain((
                                 label + error.args[0],), error.args[1:]))
                            else:
                                error.args = (label + serialize(_),)
                            raise error
                        finally:
                            error = None
                            del error

            else:
                if isinstance(_, IOBase):
                    if hasattr(_, 'url'):
                        url = _.url
                else:
                    if hasattr(_, 'name'):
                        url = urljoin('file:', _.name)
                    _, format_ = detect_format(_)
                    if isinstance(_, dict):
                        for property_name, value in _.items():
                            if value is None:
                                value = properties.NULL
                            try:
                                self[property_name] = value
                            except KeyError as error:
                                try:
                                    if error.args:
                                        if len(error.args) == 1:
                                            error.args = (
                                             '%s.%s: %s' % (qualified_name(type(self)), error.args[0], repr(_)),)
                                    raise error
                                finally:
                                    error = None
                                    del error

                    else:
                        if format_ is None:
                            _dir = tuple((property_name for property_name in dir(_) if property_name[0] != '_'))
                            for property_name in meta.writable(self.__class__).properties.keys():
                                if property_name in _dir:
                                    setattr(self, getattr(_, property_name))

                        else:
                            raise TypeError('The `_` parameter must be a string, file-like object, or dictionary, not `%s`' % repr(_))
                if format_ is not None:
                    meta.format_(self, format_)
                if url is not None:
                    meta.url(self, url)
                if meta.pointer(self) is None:
                    meta.pointer(self, '#')
                if meta.xpath(self) is None:
                    meta.xpath(self, '')

    def __hash__(self):
        return id(self)

    def __setattr__(self, property_name, value):
        instance_hooks = None
        unmarshalled_value = value
        if property_name[0] != '_':
            instance_hooks = hooks.read(self)
            if instance_hooks:
                if instance_hooks.before_setattr:
                    property_name, value = instance_hooks.before_setattr(self, property_name, value)
            try:
                property_definition = meta.read(self).properties[property_name]
            except KeyError:
                raise KeyError('`%s` has no attribute "%s".' % (
                 qualified_name(type(self)),
                 property_name))

            if value is not None:
                if isinstance(value, Generator):
                    value = tuple(value)
                try:
                    unmarshalled_value = property_definition.unmarshal(value)
                except (TypeError, ValueError) as error:
                    try:
                        message = '\n - %s.%s: ' % (
                         qualified_name(type(self)),
                         property_name)
                        if error.args and isinstance(error.args[0], str):
                            error.args = tuple(chain((
                             message + error.args[0],), error.args[1:]))
                        else:
                            error.args = (
                             message + repr(value),)
                        raise error
                    finally:
                        error = None
                        del error

        super().__setattr__(property_name, unmarshalled_value)
        if instance_hooks:
            if instance_hooks.after_setattr:
                instance_hooks.after_setattr(self, property_name, value)

    def __setitem__(self, key, value):
        instance_hooks = hooks.read(self)
        if instance_hooks:
            if instance_hooks.before_setitem:
                key, value = instance_hooks.before_setitem(self, key, value)
        instance_meta = meta.read(self)
        if key in instance_meta.properties:
            property_name = key
        else:
            property_name = None
            for potential_property_name, property in instance_meta.properties.items():
                if key == property.name:
                    property_name = potential_property_name
                    break

            if property_name is None:
                raise KeyError('`%s` has no property mapped to the name "%s"' % (
                 qualified_name(type(self)),
                 key))
            else:
                setattr(self, property_name, value)
                if instance_hooks and instance_hooks.after_setitem:
                    instance_hooks.after_setitem(self, key, value)

    def __delattr__(self, key):
        instance_meta = meta.read(self)
        if key in instance_meta.properties:
            setattr(self, key, None)
        else:
            super().__delattr__(key)

    def __getitem__(self, key):
        instance_meta = meta.read(self)
        if key in instance_meta.properties:
            property_name = key
        else:
            property_definition = None
            property_name = None
            for pn, pd in instance_meta.properties.items():
                if key == pd.name:
                    property_name = pn
                    property_definition = pd
                    break

            if property_definition is None:
                raise KeyError('`%s` has no property mapped to the name "%s"' % (
                 qualified_name(type(self)),
                 key))
        return getattr(self, property_name)

    def __copy__(self):
        return self.__class__(self)

    def __deepcopy__(self, memo):
        new_instance = self.__class__()
        instance_meta = meta.read(self)
        class_meta = meta.read(type(self))
        if instance_meta is class_meta:
            meta_ = class_meta
        else:
            meta.write(new_instance, deepcopy(instance_meta, memo))
            meta_ = instance_meta
        instance_hooks = hooks.read(self)
        class_hooks = hooks.read(type(self))
        if instance_hooks is not class_hooks:
            hooks.write(new_instance, deepcopy(instance_hooks, memo))
        if meta_ is not None:
            for property_name in meta_.properties.keys():
                try:
                    value = getattr(self, property_name)
                    if isinstance(value, Generator):
                        value = tuple(value)
                    if value is not None:
                        if not callable(value):
                            value = deepcopy(value, memo)
                        setattr(new_instance, property_name, value)
                except TypeError as error:
                    try:
                        label = '%s.%s: ' % (qualified_name(type(self)), property_name)
                        if error.args:
                            error.args = tuple(chain((
                             label + error.args[0],), error.args[1:]))
                        else:
                            error.args = (label + serialize(self),)
                        raise error
                    finally:
                        error = None
                        del error

        return new_instance

    def _marshal(self):
        object_ = self
        instance_hooks = hooks.read(object_)
        if instance_hooks is not None:
            if instance_hooks.before_marshal is not None:
                object_ = instance_hooks.before_marshal(object_)
        data = collections.OrderedDict()
        instance_meta = meta.read(object_)
        for property_name, property in instance_meta.properties.items():
            value = getattr(object_, property_name)
            if value is not None:
                key = property.name or property_name
                data[key] = property.marshal(value)

        if instance_hooks is not None:
            if instance_hooks.after_marshal is not None:
                data = instance_hooks.after_marshal(data)
        return data

    def __str__(self):
        return serialize(self)

    def __repr__(self):
        representation = [
         '%s(' % qualified_name(type(self))]
        instance_meta = meta.read(self)
        for property_name in instance_meta.properties.keys():
            value = getattr(self, property_name)
            if value is not None:
                repr_value = qualified_name(value) if isinstance(value, type) else repr(value)
                repr_value_lines = repr_value.split('\n')
                if len(repr_value_lines) > 2:
                    rvs = [
                     repr_value_lines[0]]
                    for rvl in repr_value_lines[1:]:
                        rvs.append('    ' + rvl)

                    repr_value = '\n'.join(rvs)
                representation.append('    %s=%s,' % (property_name, repr_value))

        representation.append(')')
        if len(representation) > 2:
            return '\n'.join(representation)
        return ''.join(representation)

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        instance_meta = meta.read(self)
        om = meta.read(other)
        self_properties = set(instance_meta.properties.keys())
        other_properties = set(om.properties.keys())
        if self_properties != other_properties:
            return False
        for property_name in self_properties & other_properties:
            value = getattr(self, property_name)
            ov = getattr(other, property_name)
            if value != ov:
                return False

        return True

    def __ne__(self, other):
        if self == other:
            return False
        return True

    def __iter__(self):
        instance_meta = meta.read(self)
        for property_name, property in instance_meta.properties.items():
            yield property.name or property_name

    def _validate(self, raise_errors=True):
        validation_errors = []
        object_ = self
        instance_hooks = hooks.read(self)
        if instance_hooks is not None:
            if instance_hooks.before_validate is not None:
                object_ = instance_hooks.before_validate(object_)
        instance_meta = meta.read(object_)
        for property_name, property in instance_meta.properties.items():
            value = getattr(object_, property_name)
            if value is None:
                if callable(property.required):
                    required = property.required(object_)
                else:
                    required = property.required
                if required:
                    validation_errors.append('The property `%s` is required for `%s`:\n%s' % (
                     property_name,
                     qualified_name(type(object_)),
                     str(object_)))
                elif value is properties.NULL:
                    types = property.types
                    if callable(types):
                        types = types(value)
                    if types is not None:
                        if str in types and native_str is not str:
                            if native_str not in types:
                                types = tuple(chain(*(((type_, native_str) if type_ is str else (type_,)) for type_ in types)))
                        if properties.Null not in types:
                            validation_errors.append('Null values are not allowed in `%s.%s`, ' % (
                             qualified_name(type(object_)), property_name) + 'permitted types include: %s.' % ', '.join(('`%s`' % qualified_name(type_) for type_ in types)))
            else:
                try:
                    value_validation_error_messages = validate(value, (property.types), raise_errors=False)
                    if value_validation_error_messages:
                        index = 0
                        for error_message in value_validation_error_messages:
                            value_validation_error_messages[index] = 'Error encountered ' + 'while attempting to validate property `%s`:\n\n' % property_name + error_message

                        validation_errors.extend(value_validation_error_messages)
                except errors.ValidationError as error:
                    try:
                        message = '%s.%s:\n' % (qualified_name(type(object_)), property_name)
                        if error.args:
                            error.args = tuple(chain((
                             error.args[0] + message,), error.args[1:]))
                        else:
                            error.args = (message,)
                    finally:
                        error = None
                        del error

        if instance_hooks is not None:
            if instance_hooks.after_validate is not None:
                instance_hooks.after_validate(object_)
        if raise_errors:
            if validation_errors:
                raise errors.ValidationError('\n'.join(validation_errors))
        return validation_errors


abc.model.Object.register(Object)

class Array(list):
    _format = None
    _hooks = None
    _meta = None

    def __init__(self, items=None, item_types=None):
        self._meta = None
        self._hooks = None
        self._url = None
        self._xpath = None
        self._pointer = None
        url = None
        if isinstance(items, IOBase):
            if hasattr(items, 'url'):
                url = items.url
        elif hasattr(items, 'name'):
            url = urljoin('file:', items.name)
        else:
            items, format_ = detect_format(items)
            if item_types is None:
                if isinstance(items, Array):
                    m = meta.read(items)
                    if meta.read(self) is not m:
                        meta.write(self, deepcopy(m))
            else:
                meta.writable(self).item_types = item_types
        if items is not None:
            for item in items:
                self.append(item)

            if meta.pointer(self) is None:
                meta.pointer(self, '#')
            if meta.xpath(self) is None:
                meta.xpath(self, '')
        if url is not None:
            meta.url(self, url)
        if format_ is not None:
            meta.format_(self, format_)

    def __hash__(self):
        return id(self)

    def __setitem__(self, index, value):
        instance_hooks = hooks.read(self)
        if instance_hooks:
            if instance_hooks.before_setitem:
                index, value = instance_hooks.before_setitem(self, index, value)
        else:
            m = meta.read(self)
            if m is None:
                item_types = None
            else:
                item_types = m.item_types
        value = unmarshal(value, types=item_types)
        super().__setitem__(index, value)
        if instance_hooks:
            if instance_hooks.after_setitem:
                instance_hooks.after_setitem(self, index, value)

    def append(self, value):
        if not isinstance(value, UNMARSHALLABLE_TYPES):
            raise errors.UnmarshalTypeError(value)
        else:
            instance_hooks = hooks.read(self)
            if instance_hooks:
                if instance_hooks.before_append:
                    value = instance_hooks.before_append(self, value)
            else:
                instance_meta = meta.read(self)
                if instance_meta is None:
                    item_types = None
                else:
                    item_types = instance_meta.item_types
            value = unmarshal(value, types=item_types)
            super().append(value)
            if instance_hooks and instance_hooks.after_append:
                instance_hooks.after_append(self, value)

    def __copy__(self):
        return self.__class__(self)

    def __deepcopy__(self, memo=None):
        new_instance = self.__class__()
        im = meta.read(self)
        cm = meta.read(type(self))
        if im is not cm:
            meta.write(new_instance, deepcopy(im, memo=memo))
        ih = hooks.read(self)
        ch = hooks.read(type(self))
        if ih is not ch:
            hooks.write(new_instance, deepcopy(ih, memo=memo))
        for i in self:
            new_instance.append(deepcopy(i, memo=memo))

        return new_instance

    def _marshal(self):
        a = self
        h = hooks.read(a)
        if h is not None:
            if h.before_marshal is not None:
                a = h.before_marshal(a)
        m = meta.read(a)
        a = tuple((marshal(i, types=(None if m is None else m.item_types)) for i in a))
        if h is not None:
            if h.after_marshal is not None:
                a = h.after_marshal(a)
        return a

    def _validate(self, raise_errors=True):
        validation_errors = []
        a = self
        h = hooks.read(a)
        if h is not None:
            if h.before_validate is not None:
                a = h.before_validate(a)
        m = meta.read(a)
        if m.item_types is not None:
            for i in a:
                validation_errors.extend(validate(i, (m.item_types), raise_errors=False))

        if h is not None:
            if h.after_validate is not None:
                h.after_validate(a)
        if raise_errors:
            if validation_errors:
                raise errors.ValidationError('\n'.join(validation_errors))
        return validation_errors

    def __repr__(self):
        representation = [
         qualified_name(type(self)) + '(']
        if len(self) > 0:
            representation.append('    [')
            for i in self:
                ri = qualified_name(i) if isinstance(i, type) else repr(i)
                rils = ri.split('\n')
                if len(rils) > 1:
                    ris = [
                     rils[0]]
                    ris += ['        ' + rvl for rvl in rils[1:]]
                    ri = '\n'.join(ris)
                representation.append('        %s,' % ri)

            im = meta.read(self)
            cm = meta.read(type(self))
            m = None if im is cm else im
            representation.append('    ]' + '' if (m is None or m.item_types is None) else ',')
        else:
            im = meta.read(self)
            cm = meta.read(type(self))
            if im is not cm and im.item_types:
                representation.append('    item_types=(')
                for it in im.item_types:
                    ri = qualified_name(it) if isinstance(it, type) else repr(it)
                    rils = ri.split('\n')
                    if len(rils) > 2:
                        ris = [
                         rils[0]]
                        ris += ['        ' + rvl for rvl in rils[1:-1]]
                        ris.append('        ' + rils[(-1)])
                        ri = '\n'.join(ris)
                    representation.append('        %s,' % ri)

                m = meta.read(self)
                if len(m.item_types) > 1:
                    representation[-1] = representation[(-1)][:-1]
                representation.append('    )')
        representation.append(')')
        if len(representation) > 2:
            return '\n'.join(representation)
        return ''.join(representation)

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        length = len(self)
        if length != len(other):
            return False
        for i in range(length):
            if self[i] != other[i]:
                return False

        return True

    def __ne__(self, other):
        if self == other:
            return False
        return True

    def __str__(self):
        return serialize(self)


abc.model.Array.register(Array)

class Dictionary(collections.OrderedDict):
    _format = None
    _hooks = None
    _meta = None

    def __init__(self, items=None, value_types=None):
        self._meta = None
        self._hooks = None
        self._url = None
        self._xpath = None
        self._pointer = None
        url = None
        if isinstance(items, IOBase):
            if hasattr(items, 'url'):
                url = items.url
        elif hasattr(items, 'name'):
            url = urljoin('file:', items.name)
        else:
            items, format_ = detect_format(items)
            if value_types is None:
                if isinstance(items, Dictionary):
                    m = meta.read(items)
                    if meta.read(self) is not m:
                        meta.write(self, deepcopy(m))
            else:
                meta.writable(self).value_types = value_types
        if items is None:
            super().__init__()
        else:
            if isinstance(items, (collections.OrderedDict, Dictionary)):
                items = items.items()
            else:
                if isinstance(items, dict):
                    items = sorted((items.items()), key=(lambda kv: kv))
            super().__init__(items)
            if meta.pointer(self) is None:
                meta.pointer(self, '#')
            if meta.xpath(self) is None:
                meta.xpath(self, '')
            if url is not None:
                meta.url(self, url)
            if format_ is not None:
                meta.format_(self, format_)

    def __hash__(self):
        return id(self)

    def __setitem__(self, key, value):
        instance_hooks = hooks.read(self)
        if instance_hooks:
            if instance_hooks.before_setitem:
                key, value = instance_hooks.before_setitem(self, key, value)
        else:
            instance_meta = meta.read(self)
            if instance_meta is None:
                value_types = None
            else:
                value_types = instance_meta.value_types
        try:
            unmarshalled_value = unmarshal(value,
              types=value_types)
        except TypeError as error:
            try:
                message = "\n - %s['%s']: " % (
                 qualified_name(type(self)),
                 key)
                if error.args and isinstance(error.args[0], str):
                    error.args = tuple(chain((
                     message + error.args[0],), error.args[1:]))
                else:
                    error.args = (
                     message + repr(value),)
                raise error
            finally:
                error = None
                del error

        if value is None:
            raise RuntimeError(key)
        super().__setitem__(key, unmarshalled_value)
        if instance_hooks:
            if instance_hooks.after_setitem:
                instance_hooks.after_setitem(self, key, unmarshalled_value)

    def __copy__(self):
        new_instance = self.__class__()
        im = meta.read(self)
        cm = meta.read(type(self))
        if im is not cm:
            meta.write(new_instance, im)
        ih = hooks.read(self)
        ch = hooks.read(type(self))
        if ih is not ch:
            hooks.write(new_instance, ih)
        for k, v in self.items():
            new_instance[k] = v

        return new_instance

    def __deepcopy__(self, memo=None):
        new_instance = self.__class__()
        im = meta.read(self)
        cm = meta.read(type(self))
        if im is not cm:
            meta.write(new_instance, deepcopy(im, memo=memo))
        ih = hooks.read(self)
        ch = hooks.read(type(self))
        if ih is not ch:
            hooks.write(new_instance, deepcopy(ih, memo=memo))
        for k, v in self.items():
            new_instance[k] = deepcopy(v, memo=memo)

        return new_instance

    def _marshal(self):
        """
        This method marshals an instance of `Dictionary` as built-in type `OrderedDict` which can be serialized into
        JSON/YAML/XML.
        """
        data = self
        instance_hooks = hooks.read(data)
        if instance_hooks is not None:
            if instance_hooks.before_marshal is not None:
                data = instance_hooks.before_marshal(data)
        else:
            instance_meta = meta.read(data)
            if instance_meta is None:
                value_types = None
            else:
                value_types = instance_meta.value_types
        unmarshalled_data = collections.OrderedDict([(k, marshal(v, types=value_types)) for k, v in data.items()])
        if instance_hooks is not None:
            if instance_hooks.after_marshal is not None:
                unmarshalled_data = instance_hooks.after_marshal(unmarshalled_data)
        return unmarshalled_data

    def _validate(self, raise_errors=True):
        """
        Recursively validate
        """
        validation_errors = []
        d = self
        h = d._hooks or type(d)._hooks
        if h is not None:
            if h.before_validate is not None:
                d = h.before_validate(d)
        else:
            m = meta.read(d)
            if m is None:
                value_types = None
            else:
                value_types = m.value_types
        if value_types is not None:
            for k, v in d.items():
                value_validation_errors = validate(v, value_types, raise_errors=False)
                validation_errors.extend(value_validation_errors)

        if h is not None:
            if h.after_validate is not None:
                h.after_validate(d)
        if raise_errors:
            if validation_errors:
                raise errors.ValidationError('\n'.join(validation_errors))
        return validation_errors

    def __repr__(self):
        representation = [
         qualified_name(type(self)) + '(']
        items = tuple(self.items())
        if len(items) > 0:
            representation.append('    [')
            for k, v in items:
                rv = qualified_name(v) if isinstance(v, type) else repr(v)
                rvls = rv.split('\n')
                if len(rvls) > 1:
                    rvs = [
                     rvls[0]]
                    for rvl in rvls[1:]:
                        rvs.append('            ' + rvl)

                    rv = '\n'.join(rvs)
                    representation += [
                     '        (',
                     '            %s,' % repr(k),
                     '            %s' % rv,
                     '        ),']
                else:
                    representation.append('        (%s, %s),' % (repr(k), rv))

            representation[-1] = representation[(-1)][:-1]
            representation.append('    ]' if (self._meta is None or self._meta.value_types is None) else '    ],')
        else:
            cm = meta.read(type(self))
            im = meta.read(self)
            if cm is not im and self._meta.value_types:
                representation.append('    value_types=(')
                for vt in im.value_types:
                    rv = qualified_name(vt) if isinstance(vt, type) else repr(vt)
                    rvls = rv.split('\n')
                    if len(rvls) > 1:
                        rvs = [
                         rvls[0]]
                        rvs += ['        ' + rvl for rvl in rvls[1:]]
                        rv = '\n'.join(rvs)
                    representation.append('        %s,' % rv)

                if len(self._meta.value_types) > 1:
                    representation[-1] = representation[(-1)][:-1]
                representation.append('    )')
        representation.append(')')
        if len(representation) > 2:
            return '\n'.join(representation)
        return ''.join(representation)

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        keys = tuple(self.keys())
        other_keys = tuple(other.keys())
        if keys != other_keys:
            return False
        for k in keys:
            if self[k] != other[k]:
                return False

        return True

    def __ne__(self, other):
        if self == other:
            return False
        return True

    def __str__(self):
        return serialize(self)


abc.model.Dictionary.register(Dictionary)

def from_meta(name, metadata, module=None, docstring=None):
    """
    Constructs an `Object`, `Array`, or `Dictionary` sub-class from an instance of `serial.meta.Meta`.

    Arguments:

        - name (str): The name of the class.

        - class_meta (serial.meta.Meta)

        - module (str): Specify the value for the class definition's `__module__` property. The invoking module will be
          used if this is not specified (if possible).

        - docstring (str): A docstring to associate with the class definition.
    """

    def typing_from_property--- This code section failed: ---

 L.1135         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'p'
                4  LOAD_GLOBAL              type
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_FALSE    48  'to 48'

 L.1136        10  LOAD_FAST                'p'

 L.1137        12  LOAD_GLOBAL              Union
               14  LOAD_GLOBAL              Dict
               16  LOAD_GLOBAL              Any
               18  LOAD_GLOBAL              Sequence
               20  LOAD_GLOBAL              IO
               22  BUILD_TUPLE_5         5 
               24  COMPARE_OP               in
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L.1139        28  LOAD_FAST                'p'
               30  LOAD_ATTR                __name__
               32  STORE_FAST               'type_hint'
               34  JUMP_FORWARD        488  'to 488'
             36_0  COME_FROM            26  '26'

 L.1141        36  LOAD_GLOBAL              qualified_name
               38  LOAD_FAST                'p'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  STORE_FAST               'type_hint'
            44_46  JUMP_FORWARD        488  'to 488'
             48_0  COME_FROM             8  '8'

 L.1142        48  LOAD_GLOBAL              isinstance
               50  LOAD_FAST                'p'
               52  LOAD_GLOBAL              properties
               54  LOAD_ATTR                DateTime
               56  CALL_FUNCTION_2       2  '2 positional arguments'
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L.1143        60  LOAD_STR                 'datetime'
               62  STORE_FAST               'type_hint'
            64_66  JUMP_FORWARD        488  'to 488'
             68_0  COME_FROM            58  '58'

 L.1144        68  LOAD_GLOBAL              isinstance
               70  LOAD_FAST                'p'
               72  LOAD_GLOBAL              properties
               74  LOAD_ATTR                Date
               76  CALL_FUNCTION_2       2  '2 positional arguments'
               78  POP_JUMP_IF_FALSE    88  'to 88'

 L.1145        80  LOAD_STR                 'date'
               82  STORE_FAST               'type_hint'
            84_86  JUMP_FORWARD        488  'to 488'
             88_0  COME_FROM            78  '78'

 L.1146        88  LOAD_GLOBAL              isinstance
               90  LOAD_FAST                'p'
               92  LOAD_GLOBAL              properties
               94  LOAD_ATTR                Bytes
               96  CALL_FUNCTION_2       2  '2 positional arguments'
               98  POP_JUMP_IF_FALSE   108  'to 108'

 L.1147       100  LOAD_STR                 'bytes'
              102  STORE_FAST               'type_hint'
          104_106  JUMP_FORWARD        488  'to 488'
            108_0  COME_FROM            98  '98'

 L.1148       108  LOAD_GLOBAL              isinstance
              110  LOAD_FAST                'p'
              112  LOAD_GLOBAL              properties
              114  LOAD_ATTR                Integer
              116  CALL_FUNCTION_2       2  '2 positional arguments'
              118  POP_JUMP_IF_FALSE   128  'to 128'

 L.1149       120  LOAD_STR                 'int'
              122  STORE_FAST               'type_hint'
          124_126  JUMP_FORWARD        488  'to 488'
            128_0  COME_FROM           118  '118'

 L.1150       128  LOAD_GLOBAL              isinstance
              130  LOAD_FAST                'p'
              132  LOAD_GLOBAL              properties
              134  LOAD_ATTR                Number
              136  CALL_FUNCTION_2       2  '2 positional arguments'
              138  POP_JUMP_IF_FALSE   152  'to 152'

 L.1151       140  LOAD_GLOBAL              qualified_name
              142  LOAD_GLOBAL              Number
              144  CALL_FUNCTION_1       1  '1 positional argument'
              146  STORE_FAST               'type_hint'
          148_150  JUMP_FORWARD        488  'to 488'
            152_0  COME_FROM           138  '138'

 L.1152       152  LOAD_GLOBAL              isinstance
              154  LOAD_FAST                'p'
              156  LOAD_GLOBAL              properties
              158  LOAD_ATTR                Boolean
              160  CALL_FUNCTION_2       2  '2 positional arguments'
              162  POP_JUMP_IF_FALSE   172  'to 172'

 L.1153       164  LOAD_STR                 'bool'
              166  STORE_FAST               'type_hint'
          168_170  JUMP_FORWARD        488  'to 488'
            172_0  COME_FROM           162  '162'

 L.1154       172  LOAD_GLOBAL              isinstance
              174  LOAD_FAST                'p'
              176  LOAD_GLOBAL              properties
              178  LOAD_ATTR                String
              180  CALL_FUNCTION_2       2  '2 positional arguments'
              182  POP_JUMP_IF_FALSE   192  'to 192'

 L.1155       184  LOAD_STR                 'str'
              186  STORE_FAST               'type_hint'
          188_190  JUMP_FORWARD        488  'to 488'
            192_0  COME_FROM           182  '182'

 L.1156       192  LOAD_GLOBAL              isinstance
              194  LOAD_FAST                'p'
              196  LOAD_GLOBAL              properties
              198  LOAD_ATTR                Array
              200  CALL_FUNCTION_2       2  '2 positional arguments'
          202_204  POP_JUMP_IF_FALSE   304  'to 304'

 L.1157       206  LOAD_CONST               None
              208  STORE_FAST               'item_types'

 L.1158       210  LOAD_FAST                'p'
              212  LOAD_ATTR                item_types
          214_216  POP_JUMP_IF_FALSE   280  'to 280'

 L.1159       218  LOAD_GLOBAL              len
              220  LOAD_FAST                'p'
              222  LOAD_ATTR                item_types
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  LOAD_CONST               1
              228  COMPARE_OP               >
          230_232  POP_JUMP_IF_FALSE   266  'to 266'

 L.1160       234  LOAD_STR                 'Union[%s]'

 L.1161       236  LOAD_STR                 ', '
              238  LOAD_METHOD              join

 L.1162       240  LOAD_CLOSURE             'typing_from_property'
              242  BUILD_TUPLE_1         1 
              244  LOAD_GENEXPR             '<code_object <genexpr>>'
              246  LOAD_STR                 'from_meta.<locals>.typing_from_property.<locals>.<genexpr>'
              248  MAKE_FUNCTION_8          'closure'

 L.1163       250  LOAD_FAST                'p'
              252  LOAD_ATTR                item_types
              254  GET_ITER         
              256  CALL_FUNCTION_1       1  '1 positional argument'
              258  CALL_METHOD_1         1  '1 positional argument'
              260  BINARY_MODULO    
              262  STORE_FAST               'item_types'
              264  JUMP_FORWARD        280  'to 280'
            266_0  COME_FROM           230  '230'

 L.1167       266  LOAD_DEREF               'typing_from_property'
              268  LOAD_FAST                'p'
              270  LOAD_ATTR                item_types
              272  LOAD_CONST               0
              274  BINARY_SUBSCR    
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  STORE_FAST               'item_types'
            280_0  COME_FROM           264  '264'
            280_1  COME_FROM           214  '214'

 L.1168       280  LOAD_STR                 'Sequence'

 L.1170       282  LOAD_FAST                'item_types'
          284_286  POP_JUMP_IF_FALSE   296  'to 296'
              288  LOAD_STR                 '[%s]'
              290  LOAD_FAST                'item_types'
              292  BINARY_MODULO    
              294  JUMP_FORWARD        298  'to 298'
            296_0  COME_FROM           284  '284'

 L.1171       296  LOAD_STR                 ''
            298_0  COME_FROM           294  '294'
              298  BINARY_ADD       
              300  STORE_FAST               'type_hint'
              302  JUMP_FORWARD        488  'to 488'
            304_0  COME_FROM           202  '202'

 L.1173       304  LOAD_GLOBAL              isinstance
              306  LOAD_FAST                'p'
              308  LOAD_GLOBAL              properties
              310  LOAD_ATTR                Dictionary
              312  CALL_FUNCTION_2       2  '2 positional arguments'
          314_316  POP_JUMP_IF_FALSE   412  'to 412'

 L.1174       318  LOAD_CONST               None
              320  STORE_FAST               'value_types'

 L.1175       322  LOAD_FAST                'p'
              324  LOAD_ATTR                value_types
          326_328  POP_JUMP_IF_FALSE   392  'to 392'

 L.1176       330  LOAD_GLOBAL              len
              332  LOAD_FAST                'p'
              334  LOAD_ATTR                value_types
              336  CALL_FUNCTION_1       1  '1 positional argument'
              338  LOAD_CONST               1
              340  COMPARE_OP               >
          342_344  POP_JUMP_IF_FALSE   378  'to 378'

 L.1177       346  LOAD_STR                 'Union[%s]'

 L.1178       348  LOAD_STR                 ', '
              350  LOAD_METHOD              join

 L.1179       352  LOAD_CLOSURE             'typing_from_property'
              354  BUILD_TUPLE_1         1 
              356  LOAD_GENEXPR             '<code_object <genexpr>>'
              358  LOAD_STR                 'from_meta.<locals>.typing_from_property.<locals>.<genexpr>'
              360  MAKE_FUNCTION_8          'closure'

 L.1180       362  LOAD_FAST                'p'
              364  LOAD_ATTR                value_types
              366  GET_ITER         
              368  CALL_FUNCTION_1       1  '1 positional argument'
              370  CALL_METHOD_1         1  '1 positional argument'
              372  BINARY_MODULO    
              374  STORE_FAST               'value_types'
              376  JUMP_FORWARD        392  'to 392'
            378_0  COME_FROM           342  '342'

 L.1184       378  LOAD_DEREF               'typing_from_property'
              380  LOAD_FAST                'p'
              382  LOAD_ATTR                value_types
              384  LOAD_CONST               0
              386  BINARY_SUBSCR    
              388  CALL_FUNCTION_1       1  '1 positional argument'
              390  STORE_FAST               'value_types'
            392_0  COME_FROM           376  '376'
            392_1  COME_FROM           326  '326'

 L.1187       392  LOAD_FAST                'value_types'
          394_396  POP_JUMP_IF_FALSE   406  'to 406'
              398  LOAD_STR                 'Dict[str, %s]'
              400  LOAD_FAST                'value_types'
              402  BINARY_MODULO    
              404  JUMP_FORWARD        408  'to 408'
            406_0  COME_FROM           394  '394'

 L.1188       406  LOAD_STR                 'dict'
            408_0  COME_FROM           404  '404'
              408  STORE_FAST               'type_hint'
              410  JUMP_FORWARD        488  'to 488'
            412_0  COME_FROM           314  '314'

 L.1190       412  LOAD_FAST                'p'
              414  LOAD_ATTR                types
          416_418  POP_JUMP_IF_FALSE   484  'to 484'

 L.1191       420  LOAD_GLOBAL              len
              422  LOAD_FAST                'p'
              424  LOAD_ATTR                types
              426  CALL_FUNCTION_1       1  '1 positional argument'
              428  LOAD_CONST               1
              430  COMPARE_OP               >
          432_434  POP_JUMP_IF_FALSE   468  'to 468'

 L.1192       436  LOAD_STR                 'Union[%s]'
              438  LOAD_STR                 ', '
              440  LOAD_METHOD              join

 L.1193       442  LOAD_CLOSURE             'typing_from_property'
              444  BUILD_TUPLE_1         1 
              446  LOAD_GENEXPR             '<code_object <genexpr>>'
              448  LOAD_STR                 'from_meta.<locals>.typing_from_property.<locals>.<genexpr>'
              450  MAKE_FUNCTION_8          'closure'
              452  LOAD_FAST                'p'
              454  LOAD_ATTR                types
              456  GET_ITER         
              458  CALL_FUNCTION_1       1  '1 positional argument'
              460  CALL_METHOD_1         1  '1 positional argument'
              462  BINARY_MODULO    
              464  STORE_FAST               'type_hint'
              466  JUMP_FORWARD        482  'to 482'
            468_0  COME_FROM           432  '432'

 L.1196       468  LOAD_DEREF               'typing_from_property'
              470  LOAD_FAST                'p'
              472  LOAD_ATTR                types
              474  LOAD_CONST               0
            476_0  COME_FROM            34  '34'
              476  BINARY_SUBSCR    
              478  CALL_FUNCTION_1       1  '1 positional argument'
              480  STORE_FAST               'type_hint'
            482_0  COME_FROM           466  '466'
              482  JUMP_FORWARD        488  'to 488'
            484_0  COME_FROM           416  '416'

 L.1198       484  LOAD_STR                 'Any'
              486  STORE_FAST               'type_hint'
            488_0  COME_FROM           482  '482'
            488_1  COME_FROM           410  '410'
            488_2  COME_FROM           302  '302'
            488_3  COME_FROM           188  '188'
            488_4  COME_FROM           168  '168'
            488_5  COME_FROM           148  '148'
            488_6  COME_FROM           124  '124'
            488_7  COME_FROM           104  '104'
            488_8  COME_FROM            84  '84'
            488_9  COME_FROM            64  '64'
           488_10  COME_FROM            44  '44'

 L.1199       488  LOAD_FAST                'type_hint'
              490  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 476_0

    if docstring is not None:
        if '\t' in docstring:
            docstring = docstring.replace('\t', '    ')
        lines = docstring.split('\n')
        indentation_length = float('inf')
        for line in lines:
            match = re.match('^[ ]+', line)
            if match:
                indentation_length = min(indentation_length, len(match.group()))
            else:
                indentation_length = 0
                break

        wrapped_lines = []
        for line in lines:
            line = '    ' + line[indentation_length:]
            if len(line) > 120:
                indent = re.match('^[ ]*', line).group()
                li = len(indent)
                words = re.split('([\\w]*[\\w,/"\\\'.;\\-?`])', line[li:])
                wrapped_line = ''
                for word in words:
                    if len(wrapped_line) + len(word) + li <= 120:
                        wrapped_line += word
                    else:
                        wrapped_lines.append(indent + wrapped_line)
                        wrapped_line = '' if not word.strip() else word

                if wrapped_line:
                    wrapped_lines.append(indent + wrapped_line)
            else:
                wrapped_lines.append(line)

        docstring = '\n'.join([
         '    """'] + wrapped_lines + [
         '    """'])
    elif isinstance(metadata, meta.Dictionary):
        out = ['class %s(serial.model.Dictionary):' % name]
        if docstring is not None:
            out.append(docstring)
        out.append('\n    pass')
    else:
        if isinstance(metadata, meta.Array):
            out = ['class %s(serial.model.Array):' % name]
            if docstring is not None:
                out.append(docstring)
            out.append('\n    pass')
        else:
            if isinstance(metadata, meta.Object):
                out = ['class %s(serial.model.Object):' % name]
                if docstring is not None:
                    out.append(docstring)
                out += [
                 '',
                 '    def __init__(',
                 '        self,',
                 '        _=None,  # type: Optional[Union[str, bytes, dict, Sequence, IO]]']
                for n, p in metadata.properties.items():
                    out.append('        %s=None,  # type: Optional[%s]' % (n, typing_from_property(p)))

                out.append('    ):')
                for n in metadata.properties.keys():
                    out.append('        self.%s = %s' % (n, n))

                out.append('        super().__init__(_)\n\n')
            else:
                raise ValueError(metadata)
    class_definition = '\n'.join(out)
    namespace = dict(__name__=('from_meta_%s' % name))
    imports = '\n'.join([
     'import serial',
     '',
     'serial.utilities.compatibility.backport()',
     'try:',
     '    from typing import Union, Dict, Any, Sequence, IO',
     'except ImportError:',
     '    Union = Dict = Any = Sequence = IO = None'])
    source = '%s\n\n\n%s' % (imports, class_definition)
    exec(source, namespace)
    result = namespace[name]
    result._source = source
    if module is None:
        try:
            module = sys._getframe(1).f_globals.get('__name__', '__main__')
        except (AttributeError, ValueError):
            pass

    if module is not None:
        result.__module__ = module
    result._meta = metadata
    return result