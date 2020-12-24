# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/internal/enum_type_wrapper.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 4040 bytes
"""A simple wrapper around enum types to expose utility functions.

Instances are created as properties with the same name as the enum they wrap
on proto classes.  For usage, see:
  reflection_test.py
"""
__author__ = 'rabsatt@google.com (Kevin Rabsatt)'
import six

class EnumTypeWrapper(object):
    __doc__ = 'A utility for finding the names of enum values.'
    DESCRIPTOR = None

    def __init__(self, enum_type):
        """Inits EnumTypeWrapper with an EnumDescriptor."""
        self._enum_type = enum_type
        self.DESCRIPTOR = enum_type

    def Name(self, number):
        """Returns a string containing the name of an enum value."""
        if number in self._enum_type.values_by_number:
            return self._enum_type.values_by_number[number].name
        else:
            if not isinstance(number, six.integer_types):
                raise TypeError('Enum value for %s must be an int, but got %r.' % (
                 self._enum_type.name, number))
            else:
                raise ValueError('Enum %s has no name defined for value %r' % (
                 self._enum_type.name, number))

    def Value(self, name):
        """Returns the value corresponding to the given enum name."""
        if name in self._enum_type.values_by_name:
            return self._enum_type.values_by_name[name].number
        raise ValueError('Enum %s has no value defined for name %s' % (
         self._enum_type.name, name))

    def keys(self):
        """Return a list of the string names in the enum.

    These are returned in the order they were defined in the .proto file.
    """
        return [value_descriptor.name for value_descriptor in self._enum_type.values]

    def values(self):
        """Return a list of the integer values in the enum.

    These are returned in the order they were defined in the .proto file.
    """
        return [value_descriptor.number for value_descriptor in self._enum_type.values]

    def items(self):
        """Return a list of the (name, value) pairs of the enum.

    These are returned in the order they were defined in the .proto file.
    """
        return [(value_descriptor.name, value_descriptor.number) for value_descriptor in self._enum_type.values]

    def __getattr__(self, name):
        """Returns the value corresponding to the given enum name."""
        if name in self._enum_type.values_by_name:
            return self._enum_type.values_by_name[name].number
        raise AttributeError