# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sigma/standard/error.py
# Compiled at: 2016-01-23 07:23:33
# Size of source mod 2**32: 1914 bytes
"""
"""
from sigma.core import UnitError

class WhiteListError(UnitError):
    __doc__ = 'WhiteList Constraint.\n    '

    def __str__(self):
        return '{}\nWhite List: {}\n'.format(super(WhiteListError, self).__str__(), self.option.value)


class BlackListError(UnitError):
    __doc__ = 'BlackList Constraint.\n    '

    def __str__(self):
        return '{}\nBlack List: {}\n'.format(super(BlackListError, self).__str__(), self.option.value)


class LengthError(UnitError):
    __doc__ = 'Length Constraint.\n    '

    def __str__(self):
        return '{}\nlength: {}\nlength limitation: {}\n'.format(super(LengthError, self).__str__(), len(self.value), self.option.value)


class TooShortError(LengthError):
    pass


class TooLongError(LengthError):
    pass


class SizeError(UnitError):
    __doc__ = 'Size Constraint.\n    '

    def __str__(self):
        return '{}\nsize limitation: {}\n'.format(super(SizeError, self).__str__(), self.option.value)


class OverMaxError(SizeError):
    pass


class OverMinError(SizeError):
    pass


class NotNoneError(UnitError):
    __doc__ = 'Not None Constraint.\n    '


class InvalidTypeError(UnitError):
    __doc__ = 'Type Constraint.\n    '

    def __str__(self):
        return '{}\nexpected type: {}\nactual type: {}\n'.format(super(InvalidTypeError, self).__str__(), self.option.value, type(self.value))


class RegExpError(UnitError):
    __doc__ = 'RegExp Constraint.\n    '

    def __str__(self):
        return '{}\nregexp: {}\n'.format(super(RegExpError, self).__str__(), self.option.value)