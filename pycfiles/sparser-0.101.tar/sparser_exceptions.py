# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../sparser/sparser_exceptions.py
# Compiled at: 2017-03-04 19:15:29


class SparserError(Exception):
    pass


class SparserSyntaxError(SparserError, SyntaxError):
    pass


class SparserValueError(SparserError, ValueError):
    pass


class SparserUnexpectedError(SparserError, AssertionError):
    pass