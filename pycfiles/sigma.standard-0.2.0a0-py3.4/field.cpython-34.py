# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sigma/standard/field.py
# Compiled at: 2016-01-23 07:23:33
# Size of source mod 2**32: 2033 bytes
import sigma.core as core
from .error import TooLongError, TooShortError, InvalidTypeError, OverMinError, OverMaxError, NotNoneError, RegExpError, WhiteListError, BlackListError

class Field(core.Field):

    def noneable(self, option, value):
        if not option.value:
            if value is None:
                raise NotNoneError(self, option, value)
        return value

    def white_list(self, option, value):
        if value not in option.value:
            raise WhiteListError(self, option, value)
        return value

    def black_list(self, option, value):
        if value in option.value:
            raise BlackListError(self, option, value)
        return value

    def type(self, option, value):
        if not isinstance(value, option.value):
            raise InvalidTypeError(self, option, value)
        return value

    def length(self, option, value):
        m, M = option.value
        length = len(value)
        if m:
            if length < m:
                raise TooShortError(self, option, value)
        if M:
            if length > M:
                raise TooLongError(self, option, value)
        return value

    def size(self, option, value):
        m, M = option.value
        if m:
            if value < m:
                raise OverMinError(self, option, value)
        if M:
            if value > M:
                raise OverMaxError(self, option, value)
        return value

    def match(self, option, value):
        if isinstance(option.value, tuple):
            regexp = option.value[0]
            args = option[1:]
        else:
            regexp = option.value
            args = []
        if regexp.match(value, *args):
            return value
        raise RegExpError(self, option, value)

    def search(self, option, value):
        if isinstance(option.value, tuple):
            regexp = option.value[0]
            args = option.value[1:]
        else:
            regexp = option.value
            args = []
        if regexp.search(value, *args):
            return value
        raise RegExpError(self, option, value)