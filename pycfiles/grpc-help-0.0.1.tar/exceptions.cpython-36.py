# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/caowenbin/xuetangx/grpc-help/grpc_help/exceptions.py
# Compiled at: 2019-01-30 04:23:17
# Size of source mod 2**32: 1756 bytes
import grpc

class RpcException(Exception):
    status_code = grpc.StatusCode.INTERNAL
    default_message = 'A server error occurred.'

    def __init__(self, message):
        if message is None:
            self.message = self.default_message
        else:
            self.message = message

    def __str__(self):
        return self.message


class NotAuthenticatedError(RpcException):
    status_code = grpc.StatusCode.UNAUTHENTICATED
    default_message = 'Authentication credentials were not provided.'


class AuthenticationFailedError(RpcException):
    status_code = grpc.StatusCode.UNAUTHENTICATED
    default_message = 'Incorrect authentication credentials.'


class PermissionDeniedError(RpcException):
    status_code = grpc.StatusCode.PERMISSION_DENIED
    default_message = 'You do not have permission to perform this action.'


class InvalidArgumentError(RpcException):
    status_code = grpc.StatusCode.INVALID_ARGUMENT
    default_message = 'Invalid input.'


class ValidationError(RpcException):
    status_code = grpc.StatusCode.FAILED_PRECONDITION
    default_message = 'Invalid input.'


class ObjectDoesNotExistError(RpcException):
    status_code = grpc.StatusCode.NOT_FOUND
    default_message = 'The requested object does not exist'


class RpcExceptionHandler:

    def __init__(self, rpc_content):
        self.rpc_content = rpc_content

    def __call__(self, exc, stack):
        if issubclass(exc.__class__, RpcException):
            status_code, message = exc.status_code, str(exc)
        else:
            status_code = grpc.StatusCode.UNKNOWN
            message = f"{exc}; reason: {stack}"
        self.rpc_content.set_code(status_code)
        self.rpc_content.set_details(message)
        return self.rpc_content