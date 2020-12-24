# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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