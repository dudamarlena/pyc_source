# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/takumakanari/develop/my/song2-dev/env/lib/python2.7/site-packages/song2/types.py
# Compiled at: 2016-08-15 21:37:27
from __future__ import absolute_import
import copy

class InvalidValue(ValueError):
    pass


class InvalidType(ValueError):

    def __init__(self, name, excepted, val):
        self.name = name
        self.excepted = excepted
        self.val = val

    def __str__(self):
        return '%s=%s: %s is expected, but %s' % (self.name, self.val,
         self.excepted, type(self.val))


class _Property(object):
    typ = None
    VALIDATE_CONTINUE = 1
    VALIDATE_STOP = 2

    def __init__(self, nullable=True, empty=True, default=None):
        self.nullable = nullable
        self.empty = empty
        self._default = default
        self.is_rewritable = False

    @property
    def default(self):
        return self._default

    def rewritable(self):
        self.is_rewritable = True
        return self

    def validate(self, name, v):
        if v:
            if not isinstance(v, self.typ):
                raise InvalidType(name, self.typ, v)
            return self.VALIDATE_CONTINUE
        else:
            if v is None:
                if not self.nullable:
                    raise InvalidValue('"%s" is not nullable' % name)
            elif not self.empty:
                raise InvalidValue('"%s" should be non-empty value' % name)
            return self.VALIDATE_STOP


class String(_Property):
    typ = basestring


class StringValue(String):

    def __init__(self, default=None):
        super(StringValue, self).__init__(nullable=False, empty=False, default=default)


class Int(_Property):
    typ = int

    def __init__(self, default=0):
        super(Int, self).__init__(nullable=False, empty=True, default=default)


class Float(Int):
    typ = float

    def __init__(self, default=0.0):
        super(Float, self).__init__(default=default)


class Long(Int):
    typ = long

    def __init__(self, default=0):
        super(Long, self).__init__(default=default)


class Bool(_Property):
    typ = bool

    def __init__(self, default=False):
        super(Bool, self).__init__(nullable=False, empty=True, default=default)


class Nested(_Property):

    def __init__(self, cls, nullable=True, empty=True, default=None):
        self.typ = cls
        super(Nested, self).__init__(nullable=nullable, empty=empty, default=default)

    @property
    def default(self):
        if self._default is not None:
            return copy.deepcopy(self._default)
        else:
            return


class ArrayOf(_Property):
    typ = (
     list, tuple)

    def __init__(self, cls, nullable=True, empty=True, default=[]):
        self.element_type = cls
        super(ArrayOf, self).__init__(nullable=nullable, empty=empty, default=default)

    @property
    def default(self):
        if self._default is not None:
            return copy.deepcopy(self._default)
        else:
            return

    def validate(self, name, values):
        if super(ArrayOf, self).validate(name, values) == self.VALIDATE_CONTINUE:
            for v in values:
                if not isinstance(v, self.element_type):
                    raise InvalidType(name, self.element_type, v)


class ListOf(ArrayOf):
    typ = list

    def __init__(self, cls, nullable=True, empty=True, default=[]):
        super(ListOf, self).__init__(cls, nullable=nullable, empty=empty, default=default)


class TupleOf(ArrayOf):
    typ = tuple

    def __init__(self, cls, nullable=True, empty=True, default=()):
        super(TupleOf, self).__init__(cls, nullable=nullable, empty=empty, default=default)


def _array_type_dynamically(typ):

    class _DynamicArrayOf(ArrayOf):

        def __init__(self, nullable=True, empty=True, default=[]):
            super(_DynamicArrayOf, self).__init__(typ, nullable=nullable, empty=empty, default=default)

    return _DynamicArrayOf


StringArray = _array_type_dynamically(basestring)
IntArray = _array_type_dynamically(int)
FloatArray = _array_type_dynamically(float)
LongArray = _array_type_dynamically(long)
BoolArray = _array_type_dynamically(bool)

class DictOf(_Property):
    typ = dict

    def __init__(self, key_type, value_type, nullable=True, empty=True, default={}, value_nullable=True):
        self.key_type = key_type
        self.value_type = value_type
        self.value_nullable = value_nullable
        super(DictOf, self).__init__(nullable=nullable, empty=empty, default=default)

    @property
    def default(self):
        if self._default is not None:
            return copy.deepcopy(self._default)
        else:
            return

    def validate(self, name, val):
        if super(DictOf, self).validate(name, val) == self.VALIDATE_CONTINUE:
            for k, v in val.items():
                if not isinstance(k, self.key_type):
                    raise InvalidType(name, self.key_type, k)
                if v is None:
                    if not self.value_nullable:
                        raise InvalidValue('%s.%s is not nullable' % (name, k))
                elif not isinstance(v, self.value_type):
                    raise InvalidType(name, self.value_type, v)

        return


def _dict_type_dynamically(typ):

    class _DynamicDictOf(DictOf):

        def __init__(self, value_type, nullable=True, empty=True, default={}, value_nullable=True):
            super(_DynamicDictOf, self).__init__(typ, value_type, nullable=nullable, empty=empty, default=default, value_nullable=value_nullable)

    return _DynamicDictOf


StringDict = _dict_type_dynamically(basestring)