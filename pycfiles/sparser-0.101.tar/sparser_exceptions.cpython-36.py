# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../sparser/sparser_exceptions.py
# Compiled at: 2017-03-04 19:15:29
# Size of source mod 2**32: 237 bytes


class SparserError(Exception):
    pass


class SparserSyntaxError(SparserError, SyntaxError):
    pass


class SparserValueError(SparserError, ValueError):
    pass


class SparserUnexpectedError(SparserError, AssertionError):
    pass