# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\gaeio\src\segpy\header.py
# Compiled at: 2020-04-25 14:33:31
# Size of source mod 2**32: 7034 bytes
from collections import OrderedDict
from weakref import WeakKeyDictionary
from itertools import chain
import os, sys
sys.path.append(os.path.dirname(__file__)[:-6][:-4][:-6])
from gaeio.src.segpy.docstring import docstring_property
from gaeio.src.segpy.util import underscores_to_camelcase, first_sentence, super_class

class Header:
    __doc__ = 'An abstract base class for header format definitions.'

    def __init__(self, **kwargs):
        for keyword, arg in kwargs.items():
            if keyword not in self.ordered_field_names():
                raise TypeError('{!r} is not a recognised field name for {!r}'.format(keyword, self.__class__.__name__))
            setattr(self, keyword, arg)

    _ordered_field_names = tuple()

    @classmethod
    def ordered_field_names(cls):
        """The ordered list of field names.

        This is a metamethod which should be called on cls.

        Returns:
            An tuple containing the field names in order.
        """
        if cls is Header:
            return cls._ordered_field_names
        else:
            return super_class(cls).ordered_field_names() + cls._ordered_field_names


class FormatMeta(type):
    __doc__ = 'A metaclass for header format classes.\n    '

    @classmethod
    def __prepare__(mcs, name, bases):
        return OrderedDict()

    def __new__(mcs, name, bases, namespace):
        namespace['_ordered_field_names'] = tuple(name for name, attr in namespace.items() if isinstance(attr, HeaderFieldDescriptor))
        transitive_bases = set(chain.from_iterable(type(base).mro(base) for base in bases))
        if Header not in transitive_bases:
            bases = (
             Header,) + bases
        for attr_name, attr in namespace.items():
            if isinstance(attr, HeaderFieldDescriptor):
                if attr._name is None:
                    attr._name = attr_name
                attr_class = attr.__class__
                if issubclass(attr_class, NamedField) and attr_class is not NamedField:
                    attr_class.__name__ = underscores_to_camelcase(attr_name)
                    attr_class.__doc__ = attr.documentation

        return super().__new__(mcs, name, bases, namespace)


class NamedField:
    __doc__ = 'Instances of NamedField can be detected by the NamedDescriptorResolver metaclass.'

    def __init__(self, value_type, offset, default, documentation):
        self._name = None
        self._value_type = value_type
        self._offset = int(offset)
        self._default = self._value_type(default)
        self._documentation = str(documentation)

    @property
    def name(self):
        """The field name."""
        return self._name

    @property
    def value_type(self):
        """The field value type (e.g. Int32)"""
        return self._value_type

    @property
    def offset(self):
        """The offset in bytes from the beginning of the header."""
        return self._offset

    @property
    def default(self):
        """The default value of the field. Must be convertible to value_type."""
        return self._default

    @property
    def documentation(self):
        """A descriptive text string."""
        return self._documentation

    @docstring_property(__doc__)
    def __doc__(self):
        return first_sentence(self._documentation)

    def __repr__(self):
        return '{}(name={!r}, value_type={!r}, offset={!r}, default={!r})'.format(self.__class__.__name__, self.name, self.value_type.__name__, self.offset, self.default)


def field(value_type, offset, default, documentation):
    """
    Args:
        value_type: The type of the field (e.g. Int32)

        offset: The offset in bytes for this field from the start of the header.

        default: The default value for this field.

        documentation: A docstring for the field. The first sentence should be usable
            as a brief description.

    Returns:
        An instance of a subclass of NamedField class.
    """

    class SpecificField(HeaderFieldDescriptor):
        pass

    return SpecificField(value_type, offset, default, documentation)


class HeaderFieldDescriptor:

    def __init__(self, value_type, offset, default, documentation):
        self._named_field = NamedField(value_type, offset, default, documentation)
        self._instance_data = WeakKeyDictionary()

    @property
    def _name(self):
        return self._named_field.name

    @_name.setter
    def _name(self, value):
        self._named_field._name = value

    def __get__(self, instance, owner):
        """Retrieve the format or instance data.

        When called on the class we return a NamedField instance containing the format data. For example:

            line_seq_num_default = TraceHeaderRev1.line_sequence_num.default
            line_seq_num_offset = TraceHeaderRev1.line_sequence_num.offset

        When called on an instance we return the field value.

            line_seq_num = my_trace_header.line_sequence_num
        """
        if instance is None:
            return self._named_field
        else:
            if instance not in self._instance_data:
                return self._named_field.default
            return self._instance_data[instance]

    def __set__(self, instance, value):
        """Set the field value."""
        try:
            self._instance_data[instance] = self._named_field._value_type(value)
        except ValueError as e:
            raise ValueError('Assigned value {!r} for {} attribute must be convertible to {}: {}'.format(value, self._name, self._named_field._value_type.__name__, e)) from e

    def __delete__(self, instance):
        raise AttributeError("Can't delete {} attribute".format(self._name))

    @docstring_property(__doc__)
    def __doc__(self):
        return self._named_field._documentation