# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-target-g7omgaxk/lib/python/yaml/constructor.py
# Compiled at: 2019-03-12 19:45:05
# Size of source mod 2**32: 27187 bytes
__all__ = [
 'BaseConstructor',
 'SafeConstructor',
 'FullConstructor',
 'UnsafeConstructor',
 'Constructor',
 'ConstructorError']
from .error import *
from .nodes import *
import collections.abc, datetime, base64, binascii, re, sys, types

class ConstructorError(MarkedYAMLError):
    pass


class BaseConstructor:
    yaml_constructors = {}
    yaml_multi_constructors = {}

    def __init__(self):
        self.constructed_objects = {}
        self.recursive_objects = {}
        self.state_generators = []
        self.deep_construct = False

    def check_data(self):
        return self.check_node()

    def get_data(self):
        if self.check_node():
            return self.construct_document(self.get_node())

    def get_single_data(self):
        node = self.get_single_node()
        if node is not None:
            return self.construct_document(node)

    def construct_document(self, node):
        data = self.construct_object(node)
        while self.state_generators:
            state_generators = self.state_generators
            self.state_generators = []
            for generator in state_generators:
                for dummy in generator:
                    pass

        self.constructed_objects = {}
        self.recursive_objects = {}
        self.deep_construct = False
        return data

    def construct_object(self, node, deep=False):
        if node in self.constructed_objects:
            return self.constructed_objects[node]
        if deep:
            old_deep = self.deep_construct
            self.deep_construct = True
        if node in self.recursive_objects:
            raise ConstructorError(None, None, 'found unconstructable recursive node', node.start_mark)
        self.recursive_objects[node] = None
        constructor = None
        tag_suffix = None
        if node.tag in self.yaml_constructors:
            constructor = self.yaml_constructors[node.tag]
        else:
            for tag_prefix in self.yaml_multi_constructors:
                if node.tag.startswith(tag_prefix):
                    tag_suffix = node.tag[len(tag_prefix):]
                    constructor = self.yaml_multi_constructors[tag_prefix]
                    break
            else:
                if None in self.yaml_multi_constructors:
                    tag_suffix = node.tag
                    constructor = self.yaml_multi_constructors[None]
                else:
                    if None in self.yaml_constructors:
                        constructor = self.yaml_constructors[None]
                    else:
                        if isinstance(node, ScalarNode):
                            constructor = self.__class__.construct_scalar
                        else:
                            if isinstance(node, SequenceNode):
                                constructor = self.__class__.construct_sequence
                            else:
                                if isinstance(node, MappingNode):
                                    constructor = self.__class__.construct_mapping

            if tag_suffix is None:
                data = constructor(self, node)
            else:
                data = constructor(self, tag_suffix, node)
            if isinstance(data, types.GeneratorType):
                generator = data
                data = next(generator)
                if self.deep_construct:
                    for dummy in generator:
                        pass

                else:
                    self.state_generators.append(generator)
            self.constructed_objects[node] = data
            del self.recursive_objects[node]
            if deep:
                self.deep_construct = old_deep
            return data

    def construct_scalar(self, node):
        if not isinstance(node, ScalarNode):
            raise ConstructorError(None, None, 'expected a scalar node, but found %s' % node.id, node.start_mark)
        return node.value

    def construct_sequence(self, node, deep=False):
        if not isinstance(node, SequenceNode):
            raise ConstructorError(None, None, 'expected a sequence node, but found %s' % node.id, node.start_mark)
        return [self.construct_object(child, deep=deep) for child in node.value]

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, MappingNode):
            raise ConstructorError(None, None, 'expected a mapping node, but found %s' % node.id, node.start_mark)
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, collections.abc.Hashable):
                raise ConstructorError('while constructing a mapping', node.start_mark, 'found unhashable key', key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value

        return mapping

    def construct_pairs(self, node, deep=False):
        if not isinstance(node, MappingNode):
            raise ConstructorError(None, None, 'expected a mapping node, but found %s' % node.id, node.start_mark)
        pairs = []
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            value = self.construct_object(value_node, deep=deep)
            pairs.append((key, value))

        return pairs

    @classmethod
    def add_constructor(cls, tag, constructor):
        if 'yaml_constructors' not in cls.__dict__:
            cls.yaml_constructors = cls.yaml_constructors.copy()
        cls.yaml_constructors[tag] = constructor

    @classmethod
    def add_multi_constructor(cls, tag_prefix, multi_constructor):
        if 'yaml_multi_constructors' not in cls.__dict__:
            cls.yaml_multi_constructors = cls.yaml_multi_constructors.copy()
        cls.yaml_multi_constructors[tag_prefix] = multi_constructor


class SafeConstructor(BaseConstructor):

    def construct_scalar(self, node):
        if isinstance(node, MappingNode):
            for key_node, value_node in node.value:
                if key_node.tag == 'tag:yaml.org,2002:value':
                    return self.construct_scalar(value_node)

        return super().construct_scalar(node)

    def flatten_mapping(self, node):
        merge = []
        index = 0
        while index < len(node.value):
            key_node, value_node = node.value[index]
            if key_node.tag == 'tag:yaml.org,2002:merge':
                del node.value[index]
                if isinstance(value_node, MappingNode):
                    self.flatten_mapping(value_node)
                    merge.extend(value_node.value)
                else:
                    if isinstance(value_node, SequenceNode):
                        submerge = []
                        for subnode in value_node.value:
                            if not isinstance(subnode, MappingNode):
                                raise ConstructorError('while constructing a mapping', node.start_mark, 'expected a mapping for merging, but found %s' % subnode.id, subnode.start_mark)
                            self.flatten_mapping(subnode)
                            submerge.append(subnode.value)

                        submerge.reverse()
                        for value in submerge:
                            merge.extend(value)

                    else:
                        raise ConstructorError('while constructing a mapping', node.start_mark, 'expected a mapping or list of mappings for merging, but found %s' % value_node.id, value_node.start_mark)
            elif key_node.tag == 'tag:yaml.org,2002:value':
                key_node.tag = 'tag:yaml.org,2002:str'
                index += 1
            else:
                index += 1

        if merge:
            node.value = merge + node.value

    def construct_mapping(self, node, deep=False):
        if isinstance(node, MappingNode):
            self.flatten_mapping(node)
        return super().construct_mapping(node, deep=deep)

    def construct_yaml_null(self, node):
        self.construct_scalar(node)

    bool_values = {'yes':True, 
     'no':False, 
     'true':True, 
     'false':False, 
     'on':True, 
     'off':False}

    def construct_yaml_bool(self, node):
        value = self.construct_scalar(node)
        return self.bool_values[value.lower()]

    def construct_yaml_int(self, node):
        value = self.construct_scalar(node)
        value = value.replace('_', '')
        sign = 1
        if value[0] == '-':
            sign = -1
        if value[0] in '+-':
            value = value[1:]
        if value == '0':
            return 0
        if value.startswith('0b'):
            return sign * int(value[2:], 2)
        if value.startswith('0x'):
            return sign * int(value[2:], 16)
        if value[0] == '0':
            return sign * int(value, 8)
        if ':' in value:
            digits = [int(part) for part in value.split(':')]
            digits.reverse()
            base = 1
            value = 0
            for digit in digits:
                value += digit * base
                base *= 60

            return sign * value
        return sign * int(value)

    inf_value = 1e+300
    while inf_value != inf_value * inf_value:
        inf_value *= inf_value

    nan_value = -inf_value / inf_value

    def construct_yaml_float(self, node):
        value = self.construct_scalar(node)
        value = value.replace('_', '').lower()
        sign = 1
        if value[0] == '-':
            sign = -1
        if value[0] in '+-':
            value = value[1:]
        if value == '.inf':
            return sign * self.inf_value
        if value == '.nan':
            return self.nan_value
        if ':' in value:
            digits = [float(part) for part in value.split(':')]
            digits.reverse()
            base = 1
            value = 0.0
            for digit in digits:
                value += digit * base
                base *= 60

            return sign * value
        return sign * float(value)

    def construct_yaml_binary(self, node):
        try:
            value = self.construct_scalar(node).encode('ascii')
        except UnicodeEncodeError as exc:
            try:
                raise ConstructorError(None, None, 'failed to convert base64 data into ascii: %s' % exc, node.start_mark)
            finally:
                exc = None
                del exc

        try:
            if hasattr(base64, 'decodebytes'):
                return base64.decodebytes(value)
            return base64.decodestring(value)
        except binascii.Error as exc:
            try:
                raise ConstructorError(None, None, 'failed to decode base64 data: %s' % exc, node.start_mark)
            finally:
                exc = None
                del exc

    timestamp_regexp = re.compile('^(?P<year>[0-9][0-9][0-9][0-9])\n                -(?P<month>[0-9][0-9]?)\n                -(?P<day>[0-9][0-9]?)\n                (?:(?:[Tt]|[ \\t]+)\n                (?P<hour>[0-9][0-9]?)\n                :(?P<minute>[0-9][0-9])\n                :(?P<second>[0-9][0-9])\n                (?:\\.(?P<fraction>[0-9]*))?\n                (?:[ \\t]*(?P<tz>Z|(?P<tz_sign>[-+])(?P<tz_hour>[0-9][0-9]?)\n                (?::(?P<tz_minute>[0-9][0-9]))?))?)?$', re.X)

    def construct_yaml_timestamp(self, node):
        value = self.construct_scalar(node)
        match = self.timestamp_regexp.match(node.value)
        values = match.groupdict()
        year = int(values['year'])
        month = int(values['month'])
        day = int(values['day'])
        if not values['hour']:
            return datetime.date(year, month, day)
        hour = int(values['hour'])
        minute = int(values['minute'])
        second = int(values['second'])
        fraction = 0
        if values['fraction']:
            fraction = values['fraction'][:6]
            while len(fraction) < 6:
                fraction += '0'

            fraction = int(fraction)
        delta = None
        if values['tz_sign']:
            tz_hour = int(values['tz_hour'])
            tz_minute = int(values['tz_minute'] or 0)
            delta = datetime.timedelta(hours=tz_hour, minutes=tz_minute)
            if values['tz_sign'] == '-':
                delta = -delta
        data = datetime.datetime(year, month, day, hour, minute, second, fraction)
        if delta:
            data -= delta
        return data

    def construct_yaml_omap(self, node):
        omap = []
        yield omap
        if not isinstance(node, SequenceNode):
            raise ConstructorError('while constructing an ordered map', node.start_mark, 'expected a sequence, but found %s' % node.id, node.start_mark)
        for subnode in node.value:
            if not isinstance(subnode, MappingNode):
                raise ConstructorError('while constructing an ordered map', node.start_mark, 'expected a mapping of length 1, but found %s' % subnode.id, subnode.start_mark)
            if len(subnode.value) != 1:
                raise ConstructorError('while constructing an ordered map', node.start_mark, 'expected a single mapping item, but found %d items' % len(subnode.value), subnode.start_mark)
            key_node, value_node = subnode.value[0]
            key = self.construct_object(key_node)
            value = self.construct_object(value_node)
            omap.append((key, value))

    def construct_yaml_pairs(self, node):
        pairs = []
        yield pairs
        if not isinstance(node, SequenceNode):
            raise ConstructorError('while constructing pairs', node.start_mark, 'expected a sequence, but found %s' % node.id, node.start_mark)
        for subnode in node.value:
            if not isinstance(subnode, MappingNode):
                raise ConstructorError('while constructing pairs', node.start_mark, 'expected a mapping of length 1, but found %s' % subnode.id, subnode.start_mark)
            if len(subnode.value) != 1:
                raise ConstructorError('while constructing pairs', node.start_mark, 'expected a single mapping item, but found %d items' % len(subnode.value), subnode.start_mark)
            key_node, value_node = subnode.value[0]
            key = self.construct_object(key_node)
            value = self.construct_object(value_node)
            pairs.append((key, value))

    def construct_yaml_set(self, node):
        data = set()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_yaml_str(self, node):
        return self.construct_scalar(node)

    def construct_yaml_seq(self, node):
        data = []
        yield data
        data.extend(self.construct_sequence(node))

    def construct_yaml_map(self, node):
        data = {}
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_yaml_object(self, node, cls):
        data = cls.__new__(cls)
        yield data
        if hasattr(data, '__setstate__'):
            state = self.construct_mapping(node, deep=True)
            data.__setstate__(state)
        else:
            state = self.construct_mapping(node)
            data.__dict__.update(state)

    def construct_undefined(self, node):
        raise ConstructorError(None, None, 'could not determine a constructor for the tag %r' % node.tag, node.start_mark)


SafeConstructor.add_constructor('tag:yaml.org,2002:null', SafeConstructor.construct_yaml_null)
SafeConstructor.add_constructor('tag:yaml.org,2002:bool', SafeConstructor.construct_yaml_bool)
SafeConstructor.add_constructor('tag:yaml.org,2002:int', SafeConstructor.construct_yaml_int)
SafeConstructor.add_constructor('tag:yaml.org,2002:float', SafeConstructor.construct_yaml_float)
SafeConstructor.add_constructor('tag:yaml.org,2002:binary', SafeConstructor.construct_yaml_binary)
SafeConstructor.add_constructor('tag:yaml.org,2002:timestamp', SafeConstructor.construct_yaml_timestamp)
SafeConstructor.add_constructor('tag:yaml.org,2002:omap', SafeConstructor.construct_yaml_omap)
SafeConstructor.add_constructor('tag:yaml.org,2002:pairs', SafeConstructor.construct_yaml_pairs)
SafeConstructor.add_constructor('tag:yaml.org,2002:set', SafeConstructor.construct_yaml_set)
SafeConstructor.add_constructor('tag:yaml.org,2002:str', SafeConstructor.construct_yaml_str)
SafeConstructor.add_constructor('tag:yaml.org,2002:seq', SafeConstructor.construct_yaml_seq)
SafeConstructor.add_constructor('tag:yaml.org,2002:map', SafeConstructor.construct_yaml_map)
SafeConstructor.add_constructor(None, SafeConstructor.construct_undefined)

class FullConstructor(SafeConstructor):

    def construct_python_str(self, node):
        return self.construct_scalar(node)

    def construct_python_unicode(self, node):
        return self.construct_scalar(node)

    def construct_python_bytes(self, node):
        try:
            value = self.construct_scalar(node).encode('ascii')
        except UnicodeEncodeError as exc:
            try:
                raise ConstructorError(None, None, 'failed to convert base64 data into ascii: %s' % exc, node.start_mark)
            finally:
                exc = None
                del exc

        try:
            if hasattr(base64, 'decodebytes'):
                return base64.decodebytes(value)
            return base64.decodestring(value)
        except binascii.Error as exc:
            try:
                raise ConstructorError(None, None, 'failed to decode base64 data: %s' % exc, node.start_mark)
            finally:
                exc = None
                del exc

    def construct_python_long(self, node):
        return self.construct_yaml_int(node)

    def construct_python_complex(self, node):
        return complex(self.construct_scalar(node))

    def construct_python_tuple(self, node):
        return tuple(self.construct_sequence(node))

    def find_python_module(self, name, mark, unsafe=False):
        if not name:
            raise ConstructorError('while constructing a Python module', mark, 'expected non-empty name appended to the tag', mark)
        if unsafe:
            try:
                __import__(name)
            except ImportError as exc:
                try:
                    raise ConstructorError('while constructing a Python module', mark, 'cannot find module %r (%s)' % (name, exc), mark)
                finally:
                    exc = None
                    del exc

        if name not in sys.modules:
            raise ConstructorError('while constructing a Python module', mark, 'module %r is not imported' % name, mark)
        return sys.modules[name]

    def find_python_name(self, name, mark, unsafe=False):
        if not name:
            raise ConstructorError('while constructing a Python object', mark, 'expected non-empty name appended to the tag', mark)
        else:
            if '.' in name:
                module_name, object_name = name.rsplit('.', 1)
            else:
                module_name = 'builtins'
                object_name = name
            if unsafe:
                try:
                    __import__(module_name)
                except ImportError as exc:
                    try:
                        raise ConstructorError('while constructing a Python object', mark, 'cannot find module %r (%s)' % (module_name, exc), mark)
                    finally:
                        exc = None
                        del exc

            if module_name not in sys.modules:
                raise ConstructorError('while constructing a Python object', mark, 'module %r is not imported' % module_name, mark)
            module = sys.modules[module_name]
            raise (hasattr(module, object_name) or ConstructorError)('while constructing a Python object', mark, 'cannot find %r in the module %r' % (
             object_name, module.__name__), mark)
        return getattr(module, object_name)

    def construct_python_name(self, suffix, node):
        value = self.construct_scalar(node)
        if value:
            raise ConstructorError('while constructing a Python name', node.start_mark, 'expected the empty value, but found %r' % value, node.start_mark)
        return self.find_python_name(suffix, node.start_mark)

    def construct_python_module(self, suffix, node):
        value = self.construct_scalar(node)
        if value:
            raise ConstructorError('while constructing a Python module', node.start_mark, 'expected the empty value, but found %r' % value, node.start_mark)
        return self.find_python_module(suffix, node.start_mark)

    def make_python_instance(self, suffix, node, args=None, kwds=None, newobj=False, unsafe=False):
        if not args:
            args = []
        else:
            if not kwds:
                kwds = {}
            cls = self.find_python_name(suffix, node.start_mark)
            if not unsafe:
                if not isinstance(cls, type):
                    raise ConstructorError('while constructing a Python instance', node.start_mark, 'expected a class, but found %r' % type(cls), node.start_mark)
            if newobj and isinstance(cls, type):
                return (cls.__new__)(cls, *args, **kwds)
        return cls(*args, **kwds)

    def set_python_instance_state(self, instance, state):
        if hasattr(instance, '__setstate__'):
            instance.__setstate__(state)
        else:
            slotstate = {}
            if isinstance(state, tuple):
                if len(state) == 2:
                    state, slotstate = state
            elif hasattr(instance, '__dict__'):
                instance.__dict__.update(state)
            else:
                if state:
                    slotstate.update(state)
            for key, value in slotstate.items():
                setattr(object, key, value)

    def construct_python_object(self, suffix, node):
        instance = self.make_python_instance(suffix, node, newobj=True)
        yield instance
        deep = hasattr(instance, '__setstate__')
        state = self.construct_mapping(node, deep=deep)
        self.set_python_instance_state(instance, state)

    def construct_python_object_apply(self, suffix, node, newobj=False):
        if isinstance(node, SequenceNode):
            args = self.construct_sequence(node, deep=True)
            kwds = {}
            state = {}
            listitems = []
            dictitems = {}
        else:
            value = self.construct_mapping(node, deep=True)
            args = value.get('args', [])
            kwds = value.get('kwds', {})
            state = value.get('state', {})
            listitems = value.get('listitems', [])
            dictitems = value.get('dictitems', {})
        instance = self.make_python_instance(suffix, node, args, kwds, newobj)
        if state:
            self.set_python_instance_state(instance, state)
        if listitems:
            instance.extend(listitems)
        if dictitems:
            for key in dictitems:
                instance[key] = dictitems[key]

        return instance

    def construct_python_object_new(self, suffix, node):
        return self.construct_python_object_apply(suffix, node, newobj=True)


FullConstructor.add_constructor('tag:yaml.org,2002:python/none', FullConstructor.construct_yaml_null)
FullConstructor.add_constructor('tag:yaml.org,2002:python/bool', FullConstructor.construct_yaml_bool)
FullConstructor.add_constructor('tag:yaml.org,2002:python/str', FullConstructor.construct_python_str)
FullConstructor.add_constructor('tag:yaml.org,2002:python/unicode', FullConstructor.construct_python_unicode)
FullConstructor.add_constructor('tag:yaml.org,2002:python/bytes', FullConstructor.construct_python_bytes)
FullConstructor.add_constructor('tag:yaml.org,2002:python/int', FullConstructor.construct_yaml_int)
FullConstructor.add_constructor('tag:yaml.org,2002:python/long', FullConstructor.construct_python_long)
FullConstructor.add_constructor('tag:yaml.org,2002:python/float', FullConstructor.construct_yaml_float)
FullConstructor.add_constructor('tag:yaml.org,2002:python/complex', FullConstructor.construct_python_complex)
FullConstructor.add_constructor('tag:yaml.org,2002:python/list', FullConstructor.construct_yaml_seq)
FullConstructor.add_constructor('tag:yaml.org,2002:python/tuple', FullConstructor.construct_python_tuple)
FullConstructor.add_constructor('tag:yaml.org,2002:python/dict', FullConstructor.construct_yaml_map)
FullConstructor.add_multi_constructor('tag:yaml.org,2002:python/name:', FullConstructor.construct_python_name)
FullConstructor.add_multi_constructor('tag:yaml.org,2002:python/module:', FullConstructor.construct_python_module)
FullConstructor.add_multi_constructor('tag:yaml.org,2002:python/object:', FullConstructor.construct_python_object)
FullConstructor.add_multi_constructor('tag:yaml.org,2002:python/object/apply:', FullConstructor.construct_python_object_apply)
FullConstructor.add_multi_constructor('tag:yaml.org,2002:python/object/new:', FullConstructor.construct_python_object_new)

class UnsafeConstructor(FullConstructor):

    def find_python_module(self, name, mark):
        return super(UnsafeConstructor, self).find_python_module(name, mark, unsafe=True)

    def find_python_name(self, name, mark):
        return super(UnsafeConstructor, self).find_python_name(name, mark, unsafe=True)

    def make_python_instance(self, suffix, node, args=None, kwds=None, newobj=False):
        return super(UnsafeConstructor, self).make_python_instance(suffix,
          node, args, kwds, newobj, unsafe=True)


class Constructor(UnsafeConstructor):
    pass