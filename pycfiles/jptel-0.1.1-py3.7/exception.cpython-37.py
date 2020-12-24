# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/jptel/exception.py
# Compiled at: 2019-03-26 04:46:05
# Size of source mod 2**32: 141 bytes


class InvalidCharacterException(ValueError):
    pass


class InvalidTelephoneNumberException(ValueError):
    pass