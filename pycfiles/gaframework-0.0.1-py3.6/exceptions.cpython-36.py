# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/GaPy/exceptions.py
# Compiled at: 2019-06-09 07:16:27
# Size of source mod 2**32: 205 bytes


class ParentMismatchError(Exception):
    pass


class FitnessError(Exception):
    pass


class BadRangeException(Exception):
    pass


class BadArgumentException(Exception):
    pass