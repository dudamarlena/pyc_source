# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\binstruct.py
# Compiled at: 2014-09-08 15:49:34


def big_endian(original_class):
    """The big_endian function is a class decorator for classes derived from
    :class:`.StructTemplate`. By default a StructTemplate class interpretes its
    fields in little endian format. Using this decorator you change this
    behavior.

    :param original_class: The class you want to turn into a big endian
                           structure."""
    orig_init = original_class.__init__

    def __init__(self, *args, **kwargs):
        orig_init(self, *args, **kwargs)
        self.endian = 'big'

    original_class.__init__ = __init__
    return original_class


class Field(object):

    def __init__(self, start, size):
        self.start = start
        self.size = size


class NumericField(Field):

    def __get__(self, instance, owner):
        start = instance.start_offset + self.start
        values = instance.array[start:start + self.size]
        powers = range(len(values))
        powers = map(lambda x: 256 ** x, powers)
        if instance.endian == 'big':
            powers = reversed(list(powers))
        summands = map(int.__mul__, values, powers)
        return sum(summands)

    def validate_set_value(self, value):
        if value >= 2 ** (self.size * 8):
            raise ValueError('%u does not fit in this field' % value)

    def __set__(self, instance, value):
        self.validate_set_value(value)
        powers = []
        for i in range(self.size):
            powers.append(int(value % 256))
            value //= 256

        if instance.endian == 'big':
            powers = list(reversed(powers))
        powers.extend(self.size * [0])
        start = instance.start_offset + self.start
        instance.array[start:(start + self.size)] = powers[0:self.size]


class Int8Field(NumericField):
    """A numeric field representing a signed integer of 8 bits."""

    def __init__(self, start):
        NumericField.__init__(self, start, 1)


class UInt8Field(NumericField):
    """A numeric field representing an unsigned integer of 8 bits."""

    def __init__(self, start):
        NumericField.__init__(self, start, 1)


class Int16Field(NumericField):
    """A numeric field representing a signed integer of 16 bits."""

    def __init__(self, start):
        NumericField.__init__(self, start, 2)


class UInt16Field(NumericField):
    """A numeric field representing an unsigned integer of 16 bits."""

    def __init__(self, start):
        NumericField.__init__(self, start, 2)


class Int32Field(NumericField):
    """A numeric field representing a signed integer of 32 bits."""

    def __init__(self, start):
        NumericField.__init__(self, start, 4)


class UInt32Field(NumericField):
    """A numeric field representing an unsigned integer of 32 bits."""

    def __init__(self, start):
        NumericField.__init__(self, start, 4)


class StringField(Field):
    """A field representing a Python string."""

    def __init__(self, start, length):
        Field.__init__(self, start, length)

    def __get__(self, instance, owner):
        start = instance.start_offset + self.start
        values = instance.array[start:start + self.size]
        return ('').join(map(chr, values))

    def __set__(self, instance, value):
        assert len(value) <= self.size
        start = instance.start_offset + self.start
        instance.array[start:(start + len(value))] = list(map(ord, value))


class Subrange(object):
    """A sub range behaves like a list. It returns and modifies the values of
    an other list by selecting a subrange of it."""

    def __init__(self, array, start_offset, length):
        self.array = array
        self.start_offset = start_offset
        self.length = length

    def __len__(self):
        return self.length

    def __getitem__(self, key):
        if type(key) == slice:
            return self.array[self.start_offset + key.start:self.start_offset + key.stop]
        else:
            return self.array[(self.start_offset + key)]

    def __setitem__(self, key, value):
        if type(key) == slice:
            self.array[(self.start_offset + key.start):(self.start_offset + key.stop)] = value
        else:
            self.array[self.start_offset + key] = value


class RawField(Field):
    """A special field to access data in a raw byte-wise manner."""

    def __init__(self, start, size):
        self.start = start
        self.size = size

    def __get__(self, instance, owner):
        return Subrange(instance.array, instance.start_offset + self.start, self.size)

    def __set__(self, instance, value):
        raise ValueError('Cannot set a raw type field directly')


class ClassWithLengthMetaType(type):

    def __len__(self):
        return self.clslength()


ClassWithLength = ClassWithLengthMetaType('ClassWithLength', (object,), {})

class StructTemplate(ClassWithLength):
    """The main class for defining field accessible structures."""

    def __init__(self, array, start_offset):
        self.array = array
        self.start_offset = start_offset
        self.endian = 'little'

    @classmethod
    def clslength(cls):
        len = 0
        for attr in cls.__dict__.values():
            if isinstance(attr, Field):
                len = max(len, attr.start + attr.size)

        return len

    def __len__(self):
        """Returns the length of this structure. """
        return len(self.__class__)

    def set_endianess(self, endianess):
        """Switch the endianess of the defined structure.

        :param endianess: A string giving the new endianess. "little" for
                          little endian and "big" for big endian.
        """
        self.endian = endianess


class NestedStructField(Field):

    def __init__(self, start, nested_structure_type):
        self.start = start
        self.nested_structure_type = nested_structure_type

    def __get__(self, instance, owner):
        return self.nested_structure_type(instance.array, self.start)

    def __set__(self, instance, value):
        raise ValueError('Cannot set a nested structure')