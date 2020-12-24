# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/exception.py
# Compiled at: 2016-06-13 14:11:03
"""
Exceptions common to OpenStack projects
"""
import logging
from vsm.openstack.common.gettextutils import _
_FATAL_EXCEPTION_FORMAT_ERRORS = False

class Error(Exception):

    def __init__(self, message=None):
        super(Error, self).__init__(message)


class ApiError(Error):

    def __init__(self, message='Unknown', code='Unknown'):
        self.message = message
        self.code = code
        super(ApiError, self).__init__('%s: %s' % (code, message))


class NotFound(Error):
    pass


class UnknownScheme(Error):
    msg = "Unknown scheme '%s' found in URI"

    def __init__(self, scheme):
        msg = self.__class__.msg % scheme
        super(UnknownScheme, self).__init__(msg)


class BadStoreUri(Error):
    msg = 'The Store URI %s was malformed. Reason: %s'

    def __init__(self, uri, reason):
        msg = self.__class__.msg % (uri, reason)
        super(BadStoreUri, self).__init__(msg)


class Duplicate(Error):
    pass


class NotAuthorized(Error):
    pass


class NotEmpty(Error):
    pass


class Invalid(Error):
    pass


class BadInputError(Exception):
    """Error resulting from a client sending bad input to a server"""
    pass


class MissingArgumentError(Error):
    pass


class DatabaseMigrationError(Error):
    pass


class ClientConnectionError(Exception):
    """Error resulting from a client connecting to a server"""
    pass


def wrap_exception(f):

    def _wrap(*args, **kw):
        try:
            return f(*args, **kw)
        except Exception as e:
            if not isinstance(e, Error):
                logging.exception(_('Uncaught exception'))
                raise Error(str(e))
            raise

    _wrap.func_name = f.func_name
    return _wrap


class OpenstackException(Exception):
    """
    Base Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = 'An unknown exception occurred'

    def __init__(self, **kwargs):
        try:
            self._error_string = self.message % kwargs
        except Exception as e:
            if _FATAL_EXCEPTION_FORMAT_ERRORS:
                raise e
            else:
                self._error_string = self.message

    def __str__(self):
        return self._error_string


class MalformedRequestBody(OpenstackException):
    message = 'Malformed message body: %(reason)s'


class InvalidContentType(OpenstackException):
    message = 'Invalid content type %(content_type)s'