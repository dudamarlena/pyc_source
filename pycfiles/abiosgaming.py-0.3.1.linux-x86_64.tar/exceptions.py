# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/abiosgaming/exceptions.py
# Compiled at: 2015-11-29 16:17:48


class AbiosError(Exception):
    pass


class PaginationNotFound(AbiosError):
    pass


class NoMatchupFound(AbiosError):
    pass