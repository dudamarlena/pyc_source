# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/exceptions.py
# Compiled at: 2017-03-03 12:29:47
# Size of source mod 2**32: 496 bytes
__author__ = 'stas'

class BaseException(Exception):
    status = 500
    name = 'Server Error'


class ValidationError(BaseException):
    status = 400
    name = 'Validation Error'

    def __init__(self, data):
        """
        :param data: Can be string or dict in format {field: "Message"}
        """
        self.data = data


class AuthorizationError(BaseException):
    status = 401
    name = 'Not authorized'


class NotFound(BaseException):
    status = 404
    name = 'Not Found'