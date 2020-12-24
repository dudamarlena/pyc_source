# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/mvc/constrant.py
# Compiled at: 2018-05-30 05:31:20
__all__ = [
 'RequestMethod', 'HTTPStatus']
__authors__ = ['Tim Chow']
from .exception import UnkownRequestMethodError

class RequestMethod(object):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    CONNECT = 'CONNECT'
    OPTIONS = 'OPTIONS'
    TRACE = 'TRACE'

    @classmethod
    def from_string(cls, string):
        for attr_name, attr_value in vars(cls).iteritems():
            if not isinstance(attr_value, basestring):
                continue
            if attr_value == string.upper():
                return getattr(cls, attr_name)

        raise UnkownRequestMethodError


class HTTPStatus(object):
    Continue = 100
    OK = 200
    MovedPermanently = 301
    MovedTemporarily = 302
    NotModified = 304
    BadRequest = 400
    Unauthorized = 401
    Forbidden = 403
    NotFound = 404
    MethodNotAllowed = 405
    InternalError = 500
    BadGateway = 502
    NotAvaliableTemporarily = 503
    GatewayTimeout = 504

    @classmethod
    def get_message(cls, code):
        for attr_name, attr_value in vars(cls).iteritems():
            if not isinstance(attr_value, int):
                continue
            if attr_value == code:
                return attr_name

        return 'Unkown'