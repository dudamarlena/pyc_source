# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/quantmind/pulsar-odm/odm/types/choice.py
# Compiled at: 2017-11-24 06:00:10
# Size of source mod 2**32: 3377 bytes
from inspect import isclass
from enum import Enum
from sqlalchemy import types
from pulsar.api import ImproperlyConfigured

class ScalarCoercible(object):

    def _coerce(self, value):
        raise NotImplementedError

    def coercion_listener(self, target, value, oldvalue, initiator):
        return self._coerce(value)


class Choice(object):

    def __init__(self, code, value):
        self.code = code
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Choice):
            return self.code == other.code
        else:
            return other == self.code

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return 'Choice(code={code}, value={value})'.format(code=(self.code),
          value=(self.value))


class ChoiceType(types.TypeDecorator, ScalarCoercible):
    impl = types.Unicode(255)

    def __init__(self, choices, impl=None, **kwargs):
        self.choices = choices
        if isinstance(choices, type):
            if issubclass(choices, Enum):
                self.type_impl = EnumTypeImpl(enum_class=choices, **kwargs)
        else:
            self.type_impl = ChoiceTypeImpl(choices=choices, **kwargs)
        if impl:
            if isclass(impl):
                impl = impl()
            self.impl = impl

    @property
    def python_type(self):
        return self.impl.python_type

    def _coerce(self, value):
        return self.type_impl._coerce(value)

    def process_bind_param(self, value, dialect):
        return self.type_impl.process_bind_param(value, dialect)

    def process_result_value(self, value, dialect):
        return self.type_impl.process_result_value(value, dialect)


class ChoiceTypeImpl(object):
    __doc__ = 'The implementation for the ``Choice`` usage.'

    def __init__(self, choices):
        if not choices:
            raise ImproperlyConfigured('ChoiceType needs list of choices defined.')
        self.choices_dict = dict(choices)

    def _coerce(self, value):
        if value is None:
            return value
        else:
            if isinstance(value, Choice):
                return value
            return Choice(value, self.choices_dict[value])

    def process_bind_param(self, value, dialect):
        if value:
            if isinstance(value, Choice):
                return value.code
        return value

    def process_result_value(self, value, dialect):
        if value:
            return Choice(value, self.choices_dict[value])
        else:
            return value


class EnumTypeImpl(object):
    __doc__ = 'The implementation for the ``Enum`` usage.'

    def __init__(self, enum_class, bind_by_name=True):
        self.enum_class = enum_class
        self.bind_by_name = bind_by_name

    def _coerce(self, value):
        if value:
            return self.enum_class(value)

    def process_bind_param(self, value, dialect):
        ret = None
        if isinstance(value, Enum):
            ret = value.value
        else:
            if self.bind_by_name:
                if isinstance(value, str):
                    for e in self.enum_class:
                        if e.name.lower() == value.lower():
                            ret = e.value

        if value:
            ret = self.enum_class(value).value
        return ret

    def process_result_value(self, value, dialect):
        if value:
            return self.enum_class(value)