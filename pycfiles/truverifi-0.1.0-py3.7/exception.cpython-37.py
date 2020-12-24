# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/truverifi/exception.py
# Compiled at: 2019-04-30 01:32:42
# Size of source mod 2**32: 164 bytes


class trueverifiException(Exception):
    pass


class InvalidAPIKeyException(trueverifiException):
    pass


class trueverifiAPIError(trueverifiException):
    pass