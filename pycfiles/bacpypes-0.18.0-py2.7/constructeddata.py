# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/constructeddata.py
# Compiled at: 2020-01-29 15:49:50
"""
Constructed Data
"""
import sys
from copy import deepcopy as _deepcopy
from .errors import DecodingError, EncodingError, MissingRequiredParameter, InvalidParameterDatatype, InvalidTag
from .debugging import ModuleLogger, bacpypes_debugging
from .primitivedata import Atomic, ClosingTag, OpeningTag, Tag, TagList, Unsigned
_debug = 0
_log = ModuleLogger(globals())

class Element():

    def __init__(self, name, klass, context=None, optional=False):
        self.name = name
        self.klass = klass
        self.context = context
        self.optional = optional

    def __repr__(self):
        desc = '%s(%s' % (self.__class__.__name__, self.name)
        desc += ' ' + self.klass.__name__
        if self.context is not None:
            desc += ', context=%r' % (self.context,)
        if self.optional:
            desc += ', optional'
        desc += ')'
        return '<' + desc + ' instance at 0x%08x' % (id(self),) + '>'


@bacpypes_debugging
class Sequence(object):
    sequenceElements = []

    def __init__(self, *args, **kwargs):
        """
        Create a sequence element, optionally providing attribute/property values.
        """
        if _debug:
            Sequence._debug('__init__ %r %r', args, kwargs)
        my_kwargs = {}
        other_kwargs = {}
        for element in self.sequenceElements:
            if element.name in kwargs:
                my_kwargs[element.name] = kwargs[element.name]

        for kw in kwargs:
            if kw not in my_kwargs:
                other_kwargs[kw] = kwargs[kw]

        if _debug:
            Sequence._debug('    - my_kwargs: %r', my_kwargs)
        if _debug:
            Sequence._debug('    - other_kwargs: %r', other_kwargs)
        super(Sequence, self).__init__(*args, **other_kwargs)
        for element in self.sequenceElements:
            setattr(self, element.name, my_kwargs.get(element.name, None))

        return

    def encode(self, taglist):
        """
        """
        global _list_of_classes
        global _sequence_of_classes
        if _debug:
            Sequence._debug('encode %r', taglist)
        if not isinstance(taglist, TagList):
            raise TypeError('TagList expected')
        for element in self.sequenceElements:
            value = getattr(self, element.name, None)
            if element.optional and value is None:
                continue
            if not element.optional and value is None:
                raise MissingRequiredParameter('%s is a missing required element of %s' % (element.name, self.__class__.__name__))
            if element.klass in _sequence_of_classes or element.klass in _list_of_classes:
                if element.context is not None:
                    taglist.append(OpeningTag(element.context))
                if _debug:
                    Sequence._debug('    - build sequence helper: %r %r', element.klass, value)
                helper = element.klass(value)
                helper.encode(taglist)
                if element.context is not None:
                    taglist.append(ClosingTag(element.context))
            elif issubclass(element.klass, (Atomic, AnyAtomic)):
                if _debug:
                    Sequence._debug('    - build helper: %r %r', element.klass, value)
                helper = element.klass(value)
                tag = Tag()
                helper.encode(tag)
                if element.context is not None:
                    tag = tag.app_to_context(element.context)
                taglist.append(tag)
            elif isinstance(value, element.klass):
                if element.context is not None:
                    taglist.append(OpeningTag(element.context))
                value.encode(taglist)
                if element.context is not None:
                    taglist.append(ClosingTag(element.context))
            else:
                raise TypeError('%s must be of type %s' % (element.name, element.klass.__name__))

        return

    def decode(self, taglist):
        """
        """
        if _debug:
            Sequence._debug('decode %r', taglist)
        if not isinstance(taglist, TagList):
            raise TypeError('TagList expected')
        for element in self.sequenceElements:
            tag = taglist.Peek()
            if _debug:
                Sequence._debug('    - element, tag: %r, %r', element, tag)
            if tag is None:
                if element.optional:
                    setattr(self, element.name, None)
                elif element.klass in _sequence_of_classes or element.klass in _list_of_classes:
                    setattr(self, element.name, [])
                else:
                    raise MissingRequiredParameter('%s is a missing required element of %s' % (element.name, self.__class__.__name__))
            elif tag.tagClass == Tag.closingTagClass:
                if not element.optional:
                    raise MissingRequiredParameter('%s is a missing required element of %s' % (element.name, self.__class__.__name__))
                setattr(self, element.name, None)
            elif element.klass in _sequence_of_classes:
                if element.context is not None:
                    if tag.tagClass != Tag.openingTagClass or tag.tagNumber != element.context:
                        if not element.optional:
                            raise MissingRequiredParameter('%s expected opening tag %d' % (element.name, element.context))
                        else:
                            setattr(self, element.name, [])
                            continue
                    taglist.Pop()
                helper = element.klass()
                helper.decode(taglist)
                setattr(self, element.name, helper.value)
                if element.context is not None:
                    tag = taglist.Pop()
                    if tag.tagClass != Tag.closingTagClass or tag.tagNumber != element.context:
                        raise InvalidTag('%s expected closing tag %d' % (element.name, element.context))
            elif issubclass(element.klass, AnyAtomic):
                if element.context is not None:
                    raise InvalidTag('%s any atomic with context tag %d' % (element.name, element.context))
                if tag.tagClass != Tag.applicationTagClass:
                    if not element.optional:
                        raise InvalidParameterDatatype('%s expected any atomic application tag' % (element.name,))
                    else:
                        setattr(self, element.name, None)
                        continue
                taglist.Pop()
                helper = element.klass(tag)
                setattr(self, element.name, helper.value)
            elif issubclass(element.klass, Atomic):
                if element.context is not None:
                    if tag.tagClass != Tag.contextTagClass or tag.tagNumber != element.context:
                        if not element.optional:
                            raise InvalidTag('%s expected context tag %d' % (element.name, element.context))
                        else:
                            setattr(self, element.name, None)
                            continue
                    tag = tag.context_to_app(element.klass._app_tag)
                elif tag.tagClass != Tag.applicationTagClass or tag.tagNumber != element.klass._app_tag:
                    if not element.optional:
                        raise InvalidParameterDatatype('%s expected application tag %s' % (element.name, Tag._app_tag_name[element.klass._app_tag]))
                    else:
                        setattr(self, element.name, None)
                        continue
                taglist.Pop()
                helper = element.klass(tag)
                setattr(self, element.name, helper.value)
            elif issubclass(element.klass, AnyAtomic):
                if element.context is not None:
                    if tag.tagClass != Tag.contextTagClass or tag.tagNumber != element.context:
                        if not element.optional:
                            raise InvalidTag('%s expected context tag %d' % (element.name, element.context))
                        else:
                            setattr(self, element.name, None)
                            continue
                    tag = tag.context_to_app(element.klass._app_tag)
                elif tag.tagClass != Tag.applicationTagClass:
                    if not element.optional:
                        raise InvalidParameterDatatype('%s expected application tag' % (element.name,))
                    else:
                        setattr(self, element.name, None)
                        continue
                taglist.Pop()
                helper = element.klass(tag)
                setattr(self, element.name, helper.value)
            else:
                if element.context is not None:
                    if tag.tagClass != Tag.openingTagClass or tag.tagNumber != element.context:
                        if not element.optional:
                            raise InvalidTag('%s expected opening tag %d' % (element.name, element.context))
                        else:
                            setattr(self, element.name, None)
                            continue
                    taglist.Pop()
                try:
                    backup = taglist.tagList[:]
                    value = element.klass()
                    value.decode(taglist)
                    setattr(self, element.name, value)
                except (DecodingError, InvalidTag) as err:
                    if element.context is None and element.optional:
                        setattr(self, element.name, None)
                        taglist.tagList = backup
                    else:
                        raise

                if element.context is not None:
                    tag = taglist.Pop()
                    if not tag or tag.tagClass != Tag.closingTagClass or tag.tagNumber != element.context:
                        raise InvalidTag('%s expected closing tag %d' % (element.name, element.context))

        return

    def debug_contents(self, indent=1, file=sys.stdout, _ids=None):
        for element in self.sequenceElements:
            value = getattr(self, element.name, None)
            if element.optional and value is None:
                continue
            if not element.optional and value is None:
                file.write('%s%s is a missing required element of %s\n' % ('    ' * indent, element.name, self.__class__.__name__))
                continue
            if element.klass in _sequence_of_classes or element.klass in _list_of_classes:
                file.write('%s%s\n' % ('    ' * indent, element.name))
                helper = element.klass(value)
                helper.debug_contents(indent + 1, file, _ids)
            elif issubclass(element.klass, (Atomic, AnyAtomic)):
                file.write('%s%s = %r\n' % ('    ' * indent, element.name, value))
            elif isinstance(value, element.klass):
                file.write('%s%s\n' % ('    ' * indent, element.name))
                value.debug_contents(indent + 1, file, _ids)
            else:
                file.write('%s%s must be a %s\n' % ('    ' * indent, element.name, element.klass.__name__))

        return

    def dict_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if _debug:
            Sequence._debug('dict_contents use_dict=%r as_class=%r', use_dict, as_class)
        if use_dict is None:
            use_dict = as_class()
        for element in self.sequenceElements:
            value = getattr(self, element.name, None)
            if value is None:
                continue
            if element.klass in _sequence_of_classes or element.klass in _list_of_classes:
                helper = element.klass(value)
                mapped_value = helper.dict_contents(as_class=as_class)
            elif issubclass(element.klass, Atomic):
                mapped_value = value
            elif issubclass(element.klass, AnyAtomic):
                mapped_value = value.value
            elif isinstance(value, element.klass):
                mapped_value = value.dict_contents(as_class=as_class)
                use_dict.__setitem__(element.name, mapped_value)
            else:
                continue
            use_dict.__setitem__(element.name, mapped_value)

        return use_dict


_sequence_of_map = {}
_sequence_of_classes = {}

@bacpypes_debugging
def SequenceOf(klass):
    """Function to return a class that can encode and decode a list of
    some other type."""
    global _array_of_classes
    global _sequence_of_map
    if _debug:
        SequenceOf._debug('SequenceOf %r', klass)
    if klass in _sequence_of_map:
        if _debug:
            SequenceOf._debug('    - found in cache')
        return _sequence_of_map[klass]
    if klass in _sequence_of_classes:
        raise TypeError('nested sequences disallowed')
    if klass in _array_of_classes:
        raise TypeError('sequences of arrays disallowed')

    @bacpypes_debugging
    class _SequenceOf:
        subtype = None

        def __init__(self, value=None):
            if _debug:
                _SequenceOf._debug('(%r)__init__ %r (subtype=%r)', self.__class__.__name__, value, self.subtype)
            if value is None:
                self.value = []
            elif isinstance(value, list):
                self.value = value
            else:
                raise TypeError('invalid constructor datatype')
            return

        def append(self, value):
            if issubclass(self.subtype, Atomic):
                pass
            elif issubclass(self.subtype, AnyAtomic) and not isinstance(value, Atomic):
                raise TypeError('instance of an atomic type required')
            elif not isinstance(value, self.subtype):
                raise TypeError('%s value required' % (self.subtype.__name__,))
            self.value.append(value)

        def __len__(self):
            return len(self.value)

        def __getitem__(self, item):
            return self.value[item]

        def __iter__(self):
            return iter(self.value)

        def encode(self, taglist):
            if _debug:
                _SequenceOf._debug('(%r)encode %r', self.__class__.__name__, taglist)
            for value in self.value:
                if issubclass(self.subtype, (Atomic, AnyAtomic)):
                    helper = self.subtype(value)
                    tag = Tag()
                    helper.encode(tag)
                    taglist.append(tag)
                elif isinstance(value, self.subtype):
                    value.encode(taglist)
                else:
                    raise TypeError('%s must be a %s' % (value, self.subtype.__name__))

        def decode(self, taglist):
            if _debug:
                _SequenceOf._debug('(%r)decode %r', self.__class__.__name__, taglist)
            while len(taglist) != 0:
                tag = taglist.Peek()
                if tag.tagClass == Tag.closingTagClass:
                    return
                if issubclass(self.subtype, (Atomic, AnyAtomic)):
                    if _debug:
                        _SequenceOf._debug('    - building helper: %r %r', self.subtype, tag)
                    taglist.Pop()
                    helper = self.subtype(tag)
                    self.value.append(helper.value)
                else:
                    if _debug:
                        _SequenceOf._debug('    - building value: %r', self.subtype)
                    value = self.subtype()
                    value.decode(taglist)
                    self.value.append(value)

        def debug_contents(self, indent=1, file=sys.stdout, _ids=None):
            i = 0
            for value in self.value:
                if issubclass(self.subtype, (Atomic, AnyAtomic)):
                    file.write('%s[%d] = %r\n' % ('    ' * indent, i, value))
                elif isinstance(value, self.subtype):
                    file.write('%s[%d]' % ('    ' * indent, i))
                    value.debug_contents(indent + 1, file, _ids)
                else:
                    file.write('%s[%d] %s must be a %s' % ('    ' * indent, i, value, self.subtype.__name__))
                i += 1

        def dict_contents(self, use_dict=None, as_class=dict):
            mapped_value = []
            for value in self.value:
                if issubclass(self.subtype, Atomic):
                    mapped_value.append(value)
                elif issubclass(self.subtype, AnyAtomic):
                    mapped_value.append(value.value)
                elif isinstance(value, self.subtype):
                    mapped_value.append(value.dict_contents(as_class=as_class))

            return mapped_value

    setattr(_SequenceOf, 'subtype', klass)
    _SequenceOf.__name__ = 'SequenceOf' + klass.__name__
    if _debug:
        SequenceOf._debug('    - build this class: %r', _SequenceOf)
    _sequence_of_map[klass] = _SequenceOf
    _sequence_of_classes[_SequenceOf] = 1
    return _SequenceOf


class List(object):
    pass


_list_of_map = {}
_list_of_classes = {}

@bacpypes_debugging
def ListOf(klass):
    """Function to return a class that can encode and decode a list of
    some other type."""
    global _list_of_map
    if _debug:
        ListOf._debug('ListOf %r', klass)
    if klass in _list_of_map:
        if _debug:
            SequenceOf._debug('    - found in cache')
        return _list_of_map[klass]
    if klass in _list_of_classes:
        raise TypeError('nested lists disallowed')
    if klass in _array_of_classes:
        raise TypeError('lists of arrays disallowed')

    @bacpypes_debugging
    class _ListOf(List):
        subtype = None

        def __init__(self, value=None):
            if _debug:
                _ListOf._debug('(%r)__init__ %r (subtype=%r)', self.__class__.__name__, value, self.subtype)
            if value is None:
                self.value = []
            elif isinstance(value, list):
                self.value = value
            else:
                raise TypeError('invalid constructor datatype')
            return

        def append(self, value):
            if issubclass(self.subtype, Atomic):
                pass
            elif issubclass(self.subtype, AnyAtomic) and not isinstance(value, Atomic):
                raise TypeError('instance of an atomic type required')
            elif not isinstance(value, self.subtype):
                raise TypeError('%s value required' % (self.subtype.__name__,))
            self.value.append(value)

        def __len__(self):
            return len(self.value)

        def __getitem__(self, item):
            return self.value[item]

        def encode(self, taglist):
            if _debug:
                _ListOf._debug('(%r)encode %r', self.__class__.__name__, taglist)
            for value in self.value:
                if issubclass(self.subtype, (Atomic, AnyAtomic)):
                    helper = self.subtype(value)
                    tag = Tag()
                    helper.encode(tag)
                    taglist.append(tag)
                elif isinstance(value, self.subtype):
                    value.encode(taglist)
                else:
                    raise TypeError('%s must be a %s' % (value, self.subtype.__name__))

        def decode(self, taglist):
            if _debug:
                _ListOf._debug('(%r)decode %r', self.__class__.__name__, taglist)
            while len(taglist) != 0:
                tag = taglist.Peek()
                if tag.tagClass == Tag.closingTagClass:
                    return
                if issubclass(self.subtype, (Atomic, AnyAtomic)):
                    if _debug:
                        _ListOf._debug('    - building helper: %r %r', self.subtype, tag)
                    taglist.Pop()
                    helper = self.subtype(tag)
                    self.value.append(helper.value)
                else:
                    if _debug:
                        _ListOf._debug('    - building value: %r', self.subtype)
                    value = self.subtype()
                    value.decode(taglist)
                    self.value.append(value)

        def debug_contents(self, indent=1, file=sys.stdout, _ids=None):
            i = 0
            for value in self.value:
                if issubclass(self.subtype, (Atomic, AnyAtomic)):
                    file.write('%s[%d] = %r\n' % ('    ' * indent, i, value))
                elif isinstance(value, self.subtype):
                    file.write('%s[%d]' % ('    ' * indent, i))
                    value.debug_contents(indent + 1, file, _ids)
                else:
                    file.write('%s[%d] %s must be a %s' % ('    ' * indent, i, value, self.subtype.__name__))
                i += 1

        def dict_contents(self, use_dict=None, as_class=dict):
            mapped_value = []
            for value in self.value:
                if issubclass(self.subtype, Atomic):
                    mapped_value.append(value)
                elif issubclass(self.subtype, AnyAtomic):
                    mapped_value.append(value.value)
                elif isinstance(value, self.subtype):
                    mapped_value.append(value.dict_contents(as_class=as_class))

            return mapped_value

    setattr(_ListOf, 'subtype', klass)
    _ListOf.__name__ = 'ListOf' + klass.__name__
    if _debug:
        ListOf._debug('    - build this class: %r', _ListOf)
    _list_of_map[klass] = _ListOf
    _list_of_classes[_ListOf] = 1
    return _ListOf


class Array(object):
    pass


_array_of_map = {}
_array_of_classes = {}

def ArrayOf(klass, fixed_length=None, prototype=None):
    """Function to return a class that can encode and decode a list of
    some other type."""
    global _array_of_map
    if issubclass(klass, Atomic):
        if prototype is None:
            pass
        elif not klass.is_valid(prototype):
            raise ValueError('prototype %r not valid for %s' % (prototype, klass.__name__))
    elif prototype is None:
        pass
    elif not isinstance(prototype, klass):
        raise ValueError('prototype %r not valid for %s' % (prototype, klass.__name__))
    array_signature = (
     klass, fixed_length, prototype)
    if array_signature in _array_of_map:
        return _array_of_map[array_signature]
    if klass in _array_of_classes:
        raise TypeError('nested arrays disallowed')
    if klass in _sequence_of_classes:
        raise TypeError('arrays of SequenceOf disallowed')

    @bacpypes_debugging
    class ArrayOf(Array):
        subtype = None
        fixed_length = None
        prototype = None

        def __init__(self, value=None):
            if value is None:
                self.value = [
                 0]
                if self.fixed_length is not None:
                    self.fix_length(self.fixed_length)
            elif isinstance(value, list):
                if self.fixed_length is not None and len(value) != self.fixed_length:
                    raise ValueError('invalid array length')
                self.value = [len(value)]
                self.value.extend(value)
            else:
                raise TypeError('invalid constructor datatype')
            return

        def fix_length(self, new_length):
            if len(self.value) > new_length + 1:
                del self.value[new_length + 1:]
            elif len(self.value) < new_length + 1:
                element_count = new_length - len(self.value) + 1
                if issubclass(self.subtype, Atomic):
                    if self.prototype is None:
                        extend_value = self.subtype().value
                    else:
                        extend_value = self.prototype
                    self.value.extend([extend_value] * element_count)
                else:
                    for i in range(element_count):
                        if self.prototype is None:
                            append_value = self.subtype()
                        else:
                            append_value = _deepcopy(self.prototype)
                        self.value.append(append_value)

            self.value[0] = new_length
            return

        def append(self, value):
            if self.fixed_length is not None:
                raise TypeError('fixed length array')
            if issubclass(self.subtype, Atomic):
                pass
            elif issubclass(self.subtype, AnyAtomic) and not isinstance(value, Atomic):
                raise TypeError('instance of an atomic type required')
            elif not isinstance(value, self.subtype):
                raise TypeError('%s value required' % (self.subtype.__name__,))
            self.value.append(value)
            self.value[0] = len(self.value) - 1
            return

        def __len__(self):
            return self.value[0]

        def __getitem__(self, item):
            if item < 0 or item > self.value[0]:
                raise IndexError('index out of range')
            return self.value[item]

        def __setitem__(self, item, value):
            if item < 0 or item > self.value[0]:
                raise IndexError('index out of range')
            if item == 0:
                if self.fixed_length is not None:
                    if value != self.value[0]:
                        raise TypeError('fixed length array')
                    return
                self.fix_length(value)
            else:
                self.value[item] = value
            return

        def __delitem__(self, item):
            if self.fixed_length is not None:
                raise TypeError('fixed length array')
            if item < 1 or item > self.value[0]:
                raise IndexError('index out of range')
            del self.value[item]
            self.value[0] -= 1
            return

        def __iter__(self):
            return iter(self.value[1:])

        def index(self, value):
            for i in range(1, self.value[0] + 1):
                if value == self.value[i]:
                    return i

            raise ValueError('%r not in array' % (value,))

        def remove(self, item):
            if self.fixed_length is not None:
                raise TypeError('fixed length array')
            indx = self.index(item)
            self.__delitem__(indx)
            return

        def encode(self, taglist):
            if _debug:
                ArrayOf._debug('(%r)encode %r', self.__class__.__name__, taglist)
            for value in self.value[1:]:
                if issubclass(self.subtype, (Atomic, AnyAtomic)):
                    helper = self.subtype(value)
                    tag = Tag()
                    helper.encode(tag)
                    taglist.append(tag)
                elif isinstance(value, self.subtype):
                    value.encode(taglist)
                else:
                    raise TypeError('%s must be a %s' % (value, self.subtype.__name__))

        def decode(self, taglist):
            if _debug:
                ArrayOf._debug('(%r)decode %r', self.__class__.__name__, taglist)
            new_value = []
            while len(taglist) != 0:
                tag = taglist.Peek()
                if tag.tagClass == Tag.closingTagClass:
                    break
                if issubclass(self.subtype, (Atomic, AnyAtomic)):
                    if _debug:
                        ArrayOf._debug('    - building helper: %r %r', self.subtype, tag)
                    taglist.Pop()
                    helper = self.subtype(tag)
                    new_value.append(helper.value)
                else:
                    if _debug:
                        ArrayOf._debug('    - building value: %r', self.subtype)
                    value = self.subtype()
                    value.decode(taglist)
                    new_value.append(value)

            if self.fixed_length is not None:
                if self.fixed_length != len(new_value):
                    raise ValueError('invalid array length')
            self.value = [len(new_value)] + new_value
            return

        def encode_item(self, item, taglist):
            if _debug:
                ArrayOf._debug('(%r)encode_item %r %r', self.__class__.__name__, item, taglist)
            if item == 0:
                helper = Unsigned(self.value[0])
                tag = Tag()
                helper.encode(tag)
                taglist.append(tag)
            else:
                value = self.value[item]
                if issubclass(self.subtype, (Atomic, AnyAtomic)):
                    helper = self.subtype(self.value[item])
                    tag = Tag()
                    helper.encode(tag)
                    taglist.append(tag)
                elif isinstance(value, self.subtype):
                    value.encode(taglist)
                else:
                    raise TypeError('%s must be a %s' % (value, self.subtype.__name__))

        def decode_item(self, item, taglist):
            if _debug:
                ArrayOf._debug('(%r)decode_item %r %r', self.__class__.__name__, item, taglist)
            if item == 0:
                helper = Unsigned(taglist.Pop())
                self.value = helper.value
            elif issubclass(self.subtype, (Atomic, AnyAtomic)):
                if _debug:
                    ArrayOf._debug('    - building helper: %r', self.subtype)
                helper = self.subtype(taglist.Pop())
                self.value = helper.value
            else:
                if _debug:
                    ArrayOf._debug('    - building value: %r', self.subtype)
                value = self.subtype()
                value.decode(taglist)
                self.value = value

        def debug_contents(self, indent=1, file=sys.stdout, _ids=None):
            try:
                value_list = enumerate(self.value)
            except TypeError:
                file.write('%s(non-sequence) %r\n' % ('    ' * indent, self.value))
                return

            for i, value in value_list:
                if i == 0:
                    file.write('%slength = %d\n' % ('    ' * indent, value))
                elif issubclass(self.subtype, (Atomic, AnyAtomic)):
                    file.write('%s[%d] = %r\n' % ('    ' * indent, i, value))
                elif isinstance(value, self.subtype):
                    file.write('%s[%d]\n' % ('    ' * indent, i))
                    value.debug_contents(indent + 1, file, _ids)
                else:
                    file.write('%s%s must be a %s' % ('    ' * indent, value, self.subtype.__name__))

        def dict_contents(self, use_dict=None, as_class=dict):
            mapped_value = []
            for value in self.value:
                if issubclass(self.subtype, Atomic):
                    mapped_value.append(value)
                elif issubclass(self.subtype, AnyAtomic):
                    mapped_value.append(value.value)
                elif isinstance(value, self.subtype):
                    mapped_value.append(value.dict_contents(as_class=as_class))

            return mapped_value

    setattr(ArrayOf, 'subtype', klass)
    setattr(ArrayOf, 'fixed_length', fixed_length)
    setattr(ArrayOf, 'prototype', prototype)
    ArrayOf.__name__ = 'ArrayOf' + klass.__name__
    _array_of_map[array_signature] = ArrayOf
    _array_of_classes[ArrayOf] = 1
    return ArrayOf


@bacpypes_debugging
class Choice(object):
    choiceElements = []

    def __init__(self, **kwargs):
        """
        Create a choice element, optionally providing attribute/property values.
        There should only be one, but that is not strictly enforced.
        """
        if _debug:
            Choice._debug('__init__ %r', kwargs)
        my_kwargs = {}
        other_kwargs = {}
        for element in self.choiceElements:
            if element.name in kwargs:
                my_kwargs[element.name] = kwargs[element.name]

        for kw in kwargs:
            if kw not in my_kwargs:
                other_kwargs[kw] = kwargs[kw]

        if _debug:
            Choice._debug('    - my_kwargs: %r', my_kwargs)
        if _debug:
            Choice._debug('    - other_kwargs: %r', other_kwargs)
        super(Choice, self).__init__(**other_kwargs)
        for element in self.choiceElements:
            setattr(self, element.name, my_kwargs.get(element.name, None))

        return

    def encode(self, taglist):
        if _debug:
            Choice._debug('(%r)encode %r', self.__class__.__name__, taglist)
        for element in self.choiceElements:
            value = getattr(self, element.name, None)
            if value is None:
                continue
            if issubclass(element.klass, (Atomic, AnyAtomic)):
                helper = element.klass(value)
                tag = Tag()
                helper.encode(tag)
                if element.context is not None:
                    tag = tag.app_to_context(element.context)
                taglist.append(tag)
                break
            elif isinstance(value, element.klass):
                if element.context is not None:
                    taglist.append(OpeningTag(element.context))
                value.encode(taglist)
                if element.context is not None:
                    taglist.append(ClosingTag(element.context))
                break
            else:
                raise TypeError('%s must be a %s' % (element.name, element.klass.__name__))
        else:
            raise AttributeError('missing choice of %s' % (self.__class__.__name__,))

        return

    def decode(self, taglist):
        if _debug:
            Choice._debug('(%r)decode %r', self.__class__.__name__, taglist)
        tag = taglist.Peek()
        if tag is None:
            raise AttributeError('missing choice of %s' % (self.__class__.__name__,))
        if tag.tagClass == Tag.closingTagClass:
            raise AttributeError('missing choice of %s' % (self.__class__.__name__,))
        foundElement = {}
        for element in self.choiceElements:
            if _debug:
                Choice._debug('    - checking choice: %s', element.name)
            if element.klass in _sequence_of_classes or element.klass in _list_of_classes:
                if element.context is None:
                    raise NotImplementedError('choice of a SequenceOf must be context encoded')
                if tag.tagClass != Tag.contextTagClass or tag.tagNumber != element.context:
                    continue
                taglist.Pop()
                helper = element.klass()
                helper.decode(taglist)
                foundElement[element.name] = helper.value
                tag = taglist.Pop()
                if tag.tagClass != Tag.closingTagClass or tag.tagNumber != element.context:
                    raise InvalidTag('%s expected closing tag %d' % (element.name, element.context))
                if _debug:
                    Choice._debug('    - found choice (sequence)')
                break
            elif issubclass(element.klass, (Atomic, AnyAtomic)):
                if element.context is not None:
                    if tag.tagClass != Tag.contextTagClass or tag.tagNumber != element.context:
                        continue
                    tag = tag.context_to_app(element.klass._app_tag)
                elif tag.tagClass != Tag.applicationTagClass or tag.tagNumber != element.klass._app_tag:
                    continue
                taglist.Pop()
                helper = element.klass(tag)
                foundElement[element.name] = helper.value
                if _debug:
                    Choice._debug('    - found choice (atomic)')
                break
            else:
                if element.context is None:
                    raise NotImplementedError('choice of non-atomic data must be context encoded')
                if tag.tagClass != Tag.openingTagClass or tag.tagNumber != element.context:
                    continue
                taglist.Pop()
                value = element.klass()
                value.decode(taglist)
                foundElement[element.name] = value
                tag = taglist.Pop()
                if tag.tagClass != Tag.closingTagClass or tag.tagNumber != element.context:
                    raise InvalidTag('%s expected closing tag %d' % (element.name, element.context))
                if _debug:
                    Choice._debug('    - found choice (structure)')
                break
        else:
            raise AttributeError('missing choice of %s' % (self.__class__.__name__,))

        for element in self.choiceElements:
            setattr(self, element.name, foundElement.get(element.name, None))

        return

    def debug_contents(self, indent=1, file=sys.stdout, _ids=None):
        for element in self.choiceElements:
            value = getattr(self, element.name, None)
            if value is None:
                continue
            elif issubclass(element.klass, (Atomic, AnyAtomic)):
                file.write('%s%s = %r\n' % ('    ' * indent, element.name, value))
                break
            elif isinstance(value, element.klass):
                file.write('%s%s\n' % ('    ' * indent, element.name))
                value.debug_contents(indent + 1, file, _ids)
                break
            else:
                file.write('%s%s must be a %s' % ('    ' * indent, element.name, element.klass.__name__))
        else:
            file.write('%smissing choice of %s' % ('    ' * indent, self.__class__.__name__))

        return

    def dict_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if _debug:
            Choice._debug('dict_contents use_dict=%r as_class=%r', use_dict, as_class)
        if use_dict is None:
            use_dict = as_class()
        for element in self.choiceElements:
            value = getattr(self, element.name, None)
            if value is None:
                continue
            if issubclass(element.klass, Atomic):
                mapped_value = value
            elif issubclass(element.klass, AnyAtomic):
                mapped_value = value.value
            elif isinstance(value, element.klass):
                mapped_value = value.dict_contents(as_class=as_class)
            use_dict.__setitem__(element.name, mapped_value)
            break

        return use_dict


@bacpypes_debugging
class Any():

    def __init__(self, *args):
        self.tagList = TagList()
        for arg in args:
            self.cast_in(arg)

    def encode(self, taglist):
        if _debug:
            Any._debug('encode %r', taglist)
        taglist.extend(self.tagList)

    def decode(self, taglist):
        if _debug:
            Any._debug('decode %r', taglist)
        lvl = 0
        while len(taglist) != 0:
            tag = taglist.Peek()
            if tag.tagClass == Tag.openingTagClass:
                lvl += 1
            elif tag.tagClass == Tag.closingTagClass:
                lvl -= 1
                if lvl < 0:
                    break
            self.tagList.append(taglist.Pop())

        if lvl > 0:
            raise DecodingError('mismatched open/close tags')

    def cast_in(self, element):
        """encode the element into the internal tag list."""
        if _debug:
            Any._debug('cast_in %r', element)
        t = TagList()
        if isinstance(element, Atomic):
            tag = Tag()
            element.encode(tag)
            t.append(tag)
        elif isinstance(element, AnyAtomic):
            tag = Tag()
            element.value.encode(tag)
            t.append(tag)
        else:
            element.encode(t)
        self.tagList.extend(t.tagList)

    def cast_out(self, klass):
        """Interpret the content as a particular class."""
        if _debug:
            Any._debug('cast_out %r', klass)
        if klass in _sequence_of_classes or klass in _list_of_classes:
            helper = klass()
            t = TagList(self.tagList[:])
            helper.decode(t)
            if len(t) != 0:
                raise DecodingError('incomplete cast')
            return helper.value
        else:
            if klass in _array_of_classes:
                helper = klass()
                t = TagList(self.tagList[:])
                helper.decode(t)
                if len(t) != 0:
                    raise DecodingError('incomplete cast')
                return helper.value[1:]
            if issubclass(klass, (Atomic, AnyAtomic)):
                if len(self.tagList) == 0:
                    raise DecodingError('missing cast component')
                if len(self.tagList) > 1:
                    raise DecodingError('too many cast components')
                if _debug:
                    Any._debug('    - building helper: %r', klass)
                helper = klass(self.tagList[0])
                return helper.value
            if _debug:
                Any._debug('    - building value: %r', klass)
            value = klass()
            t = TagList(self.tagList[:])
            value.decode(t)
            if len(t) != 0:
                raise DecodingError('incomplete cast')
            return value

    def is_application_class_null(self):
        if _debug:
            Any._debug('is_application_class_null')
        return len(self.tagList) == 1 and self.tagList[0].tagClass == Tag.applicationTagClass and self.tagList[0].tagNumber == Tag.nullAppTag

    def debug_contents(self, indent=1, file=sys.stdout, _ids=None):
        self.tagList.debug_contents(indent, file, _ids)

    def dict_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if _debug:
            Any._debug('dict_contents use_dict=%r as_class=%r', use_dict, as_class)
        rslt_list = []
        for tag in self.tagList:
            use_dict = as_class()
            use_dict.__setitem__('class', tag.tagClass)
            use_dict.__setitem__('number', tag.tagNumber)
            use_dict.__setitem__('lvt', tag.tagLVT)
            rslt_list = use_dict

        return rslt_list


@bacpypes_debugging
class AnyAtomic(Atomic):

    def __init__(self, arg=None):
        if _debug:
            AnyAtomic._debug('__init__ %r', arg)
        self.value = None
        if arg is None:
            pass
        elif isinstance(arg, Atomic):
            self.value = arg
        elif isinstance(arg, Tag):
            self.value = arg.app_to_object()
        else:
            raise TypeError('invalid constructor datatype')
        return

    def encode(self, tag):
        if _debug:
            AnyAtomic._debug('encode %r', tag)
        self.value.encode(tag)

    def decode(self, tag):
        if _debug:
            AnyAtomic._debug('decode %r', tag)
        if tag.tagClass != Tag.applicationTagClass:
            raise ValueError('application tag required')
        self.value = tag.app_to_object()

    @classmethod
    def is_valid(cls, arg):
        """Return True if arg is valid value for the class."""
        return isinstance(arg, Atomic) and not isinstance(arg, AnyAtomic)

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, str(self.value))

    def __repr__(self):
        desc = self.__module__ + '.' + self.__class__.__name__
        if self.value:
            desc += '(' + self.value.__class__.__name__ + ')'
            desc += ' ' + str(self.value)
        return '<' + desc + ' instance at 0x%08x' % (id(self),) + '>'


@bacpypes_debugging
class SequenceOfAny(Any):

    def cast_in(self, element):
        """encode the element into the internal tag list."""
        if _debug:
            SequenceOfAny._debug('cast_in %r', element)
        if not isinstance(element, List):
            raise EncodingError('%r is not a list' % (element,))
        t = TagList()
        element.encode(t)
        self.tagList.extend(t.tagList)

    def cast_out(self, klass):
        """Interpret the content as a particular class."""
        if _debug:
            SequenceOfAny._debug('cast_out %r', klass)
        if not issubclass(klass, List):
            raise DecodingError('%r is not a list' % (klass,))
        helper = klass()
        t = TagList(self.tagList[:])
        helper.decode(t)
        if len(t) != 0:
            raise DecodingError('incomplete cast')
        return helper.value