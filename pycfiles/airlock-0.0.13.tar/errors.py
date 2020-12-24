# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jeremydw/git/edu-buy-flow/lib/airlock/errors.py
# Compiled at: 2015-03-23 15:11:53
from protorpc import remote

class Error(Exception):
    status = 500
    message = 'Error'

    def __init__(self, message):
        super(Error, self).__init__(message)
        if message is not None:
            self.message = message
        return


class BadRequestError(Error, remote.ApplicationError):
    status = 400


class XsrfTokenError(BadRequestError):
    pass


class MissingXsrfTokenError(XsrfTokenError):
    pass


class XsrfTokenMismatchError(XsrfTokenError):
    pass


class BadXsrfTokenError(XsrfTokenError):
    pass


class NotFoundError(Error, remote.ApplicationError):
    status = 404
    message = 'Not found.'


class ConflictError(Error, remote.ApplicationError):
    status = 409


class NotAuthorizedError(Error, remote.ApplicationError):
    status = 401
    message = 'Not authorized.'


class ForbiddenError(Error, remote.ApplicationError):
    status = 403
    message = 'Forbidden.'