# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/tomchristie/GitHub/api-star/api_star/exceptions.py
# Compiled at: 2016-04-14 17:35:57
# Size of source mod 2**32: 1125 bytes


class APIException(Exception):
    code = 500
    description = 'An error occurred.'

    def __init__(self, description=None, code=None):
        if description is not None:
            self.description = description
        if code is not None:
            self.code = code
        return

    def __str__(self):
        return '%s' % self.description


class BadRequest(APIException):
    code = 400
    description = 'Malformed request.'


class ValidationError(APIException):
    code = 400
    description = 'Invalid data in request.'


class Unauthorized(APIException):
    code = 401
    description = 'Incorrect authentication credentials.'


class Forbidden(APIException):
    code = 403
    description = 'You do not have permission to perform this action.'


class NotFound(APIException):
    code = 404
    description = 'No resource could be found at this URL.'


class NotAcceptable(APIException):
    code = 406
    description = 'The request `Accept` header could not be satisfied.'


class UnsupportedMediaType(APIException):
    code = 415
    description = 'Unsupported media type in the request `Content-Type` header.'