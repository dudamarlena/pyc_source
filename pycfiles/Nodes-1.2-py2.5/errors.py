# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/nodes/knots/errors.py
# Compiled at: 2009-10-22 13:29:25


class IOWarning(RuntimeWarning):
    pass


class InvalidFormatWarning(IOWarning):
    pass


class InvalidFormatError(IOError):
    pass


class CorruptedWarning(IOWarning):
    pass


class CorruptedError(IOError):
    pass


class MismatchError(TypeError):
    pass