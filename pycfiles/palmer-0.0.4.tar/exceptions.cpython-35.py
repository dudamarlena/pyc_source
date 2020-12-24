# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/loup/Workspace/Projects/personal/palmer/palmer/exceptions.py
# Compiled at: 2016-11-16 03:38:41
# Size of source mod 2**32: 1465 bytes
from palmer.utils import http_statuses
from palmer.utils.translation import lazy_gettext as _

class APIException(Exception):
    status_code = http_statuses.HTTP_500_INTERNAL_SERVER_ERROR
    message = _('A server error occurred.')

    def __init__(self, message=None, status_code=None, errors=None):
        if errors is None:
            errors = {}
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.errors = errors

    def __str__(self):
        return self.message


class NotAuthenticated(APIException):
    status_code = http_statuses.HTTP_401_UNAUTHORIZED
    default_detail = _('Authentication credentials were not provided.')


class AuthenticationFailed(APIException):
    status_code = http_statuses.HTTP_401_UNAUTHORIZED
    message = _('Incorrect authentication credentials.')


class PermissionDenied(APIException):
    status_code = http_statuses.HTTP_403_FORBIDDEN
    message = _('You do not have permission to perform this action.')


class ValidationError(APIException):
    status_code = http_statuses.HTTP_400_BAD_REQUEST
    message = _('Invalid input.')


class NotFound(APIException):
    status_code = http_statuses.HTTP_404_NOT_FOUND
    message = _('Not found.')


class MethodNotAllowed(APIException):
    status_code = http_statuses.HTTP_405_METHOD_NOT_ALLOWED
    message = _('Method not allowed.')