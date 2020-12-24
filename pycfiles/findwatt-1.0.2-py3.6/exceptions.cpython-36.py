# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/findwatt/exceptions.py
# Compiled at: 2018-10-07 05:33:45
# Size of source mod 2**32: 249 bytes


class MissingInformation(Exception):
    pass


class AlreadyExists(Exception):
    pass


class APIError(Exception):
    pass


class DoesNotExist(Exception):
    pass


class Unauthorized(Exception):
    pass


class NotReady(Exception):
    pass