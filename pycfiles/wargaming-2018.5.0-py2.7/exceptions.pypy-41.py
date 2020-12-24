# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wargaming/exceptions.py
# Compiled at: 2018-05-14 16:33:13


class APIError(Exception):
    """Basic API error"""
    pass


class RequestError(APIError):
    """API request error

    Raises if Wargaming API returns error
    """

    def __init__(self, code, field, message, value):
        super(RequestError, self).__init__(message)
        self.code = code
        self.field = field
        self.message = message
        self.value = value


class ValidationError(APIError):
    """Invalid param value error"""
    pass