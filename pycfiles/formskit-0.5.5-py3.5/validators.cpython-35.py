# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/formskit/validators.py
# Compiled at: 2015-07-25 09:04:48
# Size of source mod 2**32: 2881 bytes
import re
from decimal import Decimal, InvalidOperation

class FieldValidator(object):
    message = None

    def __init__(self):
        if self.message is None:
            self.message = self.__class__.__name__

    def init_field(self, field):
        self.field = field

    def make_field(self):
        if self.validate_field() is False:
            self.set_field_error()

    def make_value(self, field_value):
        self.field_value = field_value
        self.value = field_value.value
        if self.validate_value() is False:
            self.set_value_error()

    @property
    def value_converted(self):
        return self.field.convert(self.value)

    def set_field_error(self):
        self.field.set_error(self.message)

    def set_value_error(self):
        self.field_value.set_error(self.message)

    def validate_field(self):
        pass


class NotEmpty(FieldValidator):
    __doc__ = 'Will fail if no value found of value is empty or has only whitespaces'

    def validate_field(self):
        return len(self.field.values) > 0

    def validate_value(self):
        if self.value is None:
            return False
        if type(self.value) == str and self.value.strip() == '':
            return False
        if type(self.value) == bytes and self.value.strip() == b'':
            return False
        if type(self.value) in [list, dict, tuple] and len(self.value) == 0:
            return False
        return True


class IsDigit(FieldValidator):
    __doc__ = 'Will fail if value is not a digit.'
    regex = re.compile('^-{0,1}[0-9]+$')

    def validate_value(self):
        if not self.value:
            return True
        return re.search(self.regex, self.value) is not None


class IsDecimal(FieldValidator):
    __doc__ = 'Will fail if value can not be converted to decimal.Decimal.'

    def validate_value(self):
        try:
            Decimal(self.value)
            return True
        except InvalidOperation:
            return False


class IsEmail(FieldValidator):
    __doc__ = 'Will fail if value is not an email.'
    regex = re.compile('^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$')

    def validate_value(self):
        if len(self.value) > 7:
            return re.match(self.regex, self.value) is not None
        return False


class IsValueInAvalibleValues(FieldValidator):
    __doc__ = 'Will fail if value is not in list.'

    def __init__(self, allow_empty=False):
        super().__init__()
        self.allow_empty = allow_empty

    def validate_value(self):
        if self.allow_empty:
            if self.value is None:
                return True
            if type(self.value) == str and self.value.strip() == '':
                pass
            return True
        return self.value_converted in [avalible.value for avalible in self.field.avalible_values]