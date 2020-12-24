# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/martensm/fizzbotz/fizzbotz/exceptions.py
# Compiled at: 2016-02-18 00:02:19
# Size of source mod 2**32: 311 bytes


class FizzbotzException(Exception):
    __doc__ = 'Base exception for Fizzbotz exceptions.'


class StringLengthError(FizzbotzException):
    __doc__ = 'String argument is too long/too short.'


class EmptyStringError(FizzbotzException):
    __doc__ = 'String argument is empty.'