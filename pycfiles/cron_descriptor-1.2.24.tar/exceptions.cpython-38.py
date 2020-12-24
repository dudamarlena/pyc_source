# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/urllib3/exceptions.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 6610 bytes
from __future__ import absolute_import
import packages.six.moves.http_client as httplib_IncompleteRead

class HTTPError(Exception):
    """HTTPError"""
    pass


class HTTPWarning(Warning):
    """HTTPWarning"""
    pass


class PoolError(HTTPError):
    """PoolError"""

    def __init__(self, pool, message):
        self.pool = pool
        HTTPError.__init__(self, '%s: %s' % (pool, message))

    def __reduce__(self):
        return (
         self.__class__, (None, None))


class RequestError(PoolError):
    """RequestError"""

    def __init__(self, pool, url, message):
        self.url = url
        PoolError.__init__(self, pool, message)

    def __reduce__(self):
        return (
         self.__class__, (None, self.url, None))


class SSLError(HTTPError):
    """SSLError"""
    pass


class ProxyError(HTTPError):
    """ProxyError"""
    pass


class DecodeError(HTTPError):
    """DecodeError"""
    pass


class ProtocolError(HTTPError):
    """ProtocolError"""
    pass


ConnectionError = ProtocolError

class MaxRetryError(RequestError):
    """MaxRetryError"""

    def __init__(self, pool, url, reason=None):
        self.reason = reason
        message = 'Max retries exceeded with url: %s (Caused by %r)' % (url, reason)
        RequestError.__init__(self, pool, url, message)


class HostChangedError(RequestError):
    """HostChangedError"""

    def __init__(self, pool, url, retries=3):
        message = 'Tried to open a foreign host with url: %s' % url
        RequestError.__init__(self, pool, url, message)
        self.retries = retries


class TimeoutStateError(HTTPError):
    """TimeoutStateError"""
    pass


class TimeoutError(HTTPError):
    """TimeoutError"""
    pass


class ReadTimeoutError(TimeoutError, RequestError):
    """ReadTimeoutError"""
    pass


class ConnectTimeoutError(TimeoutError):
    """ConnectTimeoutError"""
    pass


class NewConnectionError(ConnectTimeoutError, PoolError):
    """NewConnectionError"""
    pass


class EmptyPoolError(PoolError):
    """EmptyPoolError"""
    pass


class ClosedPoolError(PoolError):
    """ClosedPoolError"""
    pass


class LocationValueError(ValueError, HTTPError):
    """LocationValueError"""
    pass


class LocationParseError(LocationValueError):
    """LocationParseError"""

    def __init__(self, location):
        message = 'Failed to parse: %s' % location
        HTTPError.__init__(self, message)
        self.location = location


class ResponseError(HTTPError):
    """ResponseError"""
    GENERIC_ERROR = 'too many error responses'
    SPECIFIC_ERROR = 'too many {status_code} error responses'


class SecurityWarning(HTTPWarning):
    """SecurityWarning"""
    pass


class SubjectAltNameWarning(SecurityWarning):
    """SubjectAltNameWarning"""
    pass


class InsecureRequestWarning(SecurityWarning):
    """InsecureRequestWarning"""
    pass


class SystemTimeWarning(SecurityWarning):
    """SystemTimeWarning"""
    pass


class InsecurePlatformWarning(SecurityWarning):
    """InsecurePlatformWarning"""
    pass


class SNIMissingWarning(HTTPWarning):
    """SNIMissingWarning"""
    pass


class DependencyWarning(HTTPWarning):
    """DependencyWarning"""
    pass


class ResponseNotChunked(ProtocolError, ValueError):
    """ResponseNotChunked"""
    pass


class BodyNotHttplibCompatible(HTTPError):
    """BodyNotHttplibCompatible"""
    pass


class IncompleteRead(HTTPError, httplib_IncompleteRead):
    """IncompleteRead"""

    def __init__(self, partial, expected):
        super(IncompleteRead, self).__init__(partial, expected)

    def __repr__(self):
        return 'IncompleteRead(%i bytes read, %i more expected)' % (
         self.partial,
         self.expected)


class InvalidHeader(HTTPError):
    """InvalidHeader"""
    pass


class ProxySchemeUnknown(AssertionError, ValueError):
    """ProxySchemeUnknown"""

    def __init__(self, scheme):
        message = 'Not supported proxy scheme %s' % scheme
        super(ProxySchemeUnknown, self).__init__(message)


class HeaderParsingError(HTTPError):
    """HeaderParsingError"""

    def __init__(self, defects, unparsed_data):
        message = '%s, unparsed data: %r' % (defects or , unparsed_data)
        super(HeaderParsingError, self).__init__(message)


class UnrewindableBodyError(HTTPError):
    """UnrewindableBodyError"""
    pass