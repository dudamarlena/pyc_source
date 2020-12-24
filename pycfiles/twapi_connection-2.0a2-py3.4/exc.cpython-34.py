# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twapi_connection/exc.py
# Compiled at: 2016-10-24 08:57:26
# Size of source mod 2**32: 1561 bytes


class TwodAPIException(Exception):
    pass


class UnsupportedResponseError(TwodAPIException):
    pass


class ClientError(TwodAPIException):
    pass


class AuthenticationError(ClientError):
    pass


class AccessDeniedError(ClientError):
    pass


class NotFoundError(ClientError):
    pass


class ServerError(TwodAPIException):
    __doc__ = '\n    Remote failed to process the request due to a problem at their end. This\n    represents an HTTP response code of 50X.\n\n    :param int http_status_code:\n\n    '

    def __init__(self, message, http_status_code):
        super(ServerError, self).__init__()
        self.message = message
        self.http_status_code = http_status_code

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '{} {}'.format(self.http_status_code, self.message)