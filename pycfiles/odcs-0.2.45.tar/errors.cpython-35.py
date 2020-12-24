# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/errors.py
# Compiled at: 2017-08-31 11:17:14
# Size of source mod 2**32: 1366 bytes
""" Defines custom exceptions and error handling functions """

class NotFound(ValueError):
    pass


class BadRequest(ValueError):
    pass


class Unauthorized(ValueError):
    pass


class Forbidden(ValueError):
    pass