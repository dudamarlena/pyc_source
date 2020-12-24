# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/websockets/websockets/exceptions.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 8824 bytes
"""
:mod:`websockets.exceptions` defines the following exception hierarchy:

* :exc:`WebSocketException`
    * :exc:`ConnectionClosed`
        * :exc:`ConnectionClosedError`
        * :exc:`ConnectionClosedOK`
    * :exc:`InvalidHandshake`
        * :exc:`SecurityError`
        * :exc:`InvalidMessage`
        * :exc:`InvalidHeader`
            * :exc:`InvalidHeaderFormat`
            * :exc:`InvalidHeaderValue`
            * :exc:`InvalidOrigin`
            * :exc:`InvalidUpgrade`
        * :exc:`InvalidStatusCode`
        * :exc:`NegotiationError`
            * :exc:`DuplicateParameter`
            * :exc:`InvalidParameterName`
            * :exc:`InvalidParameterValue`
        * :exc:`AbortHandshake`
        * :exc:`RedirectHandshake`
    * :exc:`InvalidState`
    * :exc:`InvalidURI`
    * :exc:`PayloadTooBig`
    * :exc:`ProtocolError`

"""
import http
from typing import Optional
from .http import Headers, HeadersLike
__all__ = [
 'WebSocketException',
 'ConnectionClosed',
 'ConnectionClosedError',
 'ConnectionClosedOK',
 'InvalidHandshake',
 'SecurityError',
 'InvalidMessage',
 'InvalidHeader',
 'InvalidHeaderFormat',
 'InvalidHeaderValue',
 'InvalidOrigin',
 'InvalidUpgrade',
 'InvalidStatusCode',
 'NegotiationError',
 'DuplicateParameter',
 'InvalidParameterName',
 'InvalidParameterValue',
 'AbortHandshake',
 'RedirectHandshake',
 'InvalidState',
 'InvalidURI',
 'PayloadTooBig',
 'ProtocolError',
 'WebSocketProtocolError']

class WebSocketException(Exception):
    __doc__ = '\n    Base class for all exceptions defined by :mod:`websockets`.\n\n    '


CLOSE_CODES = {1000:'OK', 
 1001:'going away', 
 1002:'protocol error', 
 1003:'unsupported type', 
 1005:'no status code [internal]', 
 1006:'connection closed abnormally [internal]', 
 1007:'invalid data', 
 1008:'policy violation', 
 1009:'message too big', 
 1010:'extension required', 
 1011:'unexpected error', 
 1015:'TLS failure [internal]'}

def format_close(code: int, reason: str) -> str:
    """
    Display a human-readable version of the close code and reason.

    """
    if 3000 <= code < 4000:
        explanation = 'registered'
    else:
        if 4000 <= code < 5000:
            explanation = 'private use'
        else:
            explanation = CLOSE_CODES.get(code, 'unknown')
    result = f"code = {code} ({explanation}), "
    if reason:
        result += f"reason = {reason}"
    else:
        result += 'no reason'
    return result


class ConnectionClosed(WebSocketException):
    __doc__ = '\n    Raised when trying to interact with a closed connection.\n\n    Provides the connection close code and reason in its ``code`` and\n    ``reason`` attributes respectively.\n\n    '

    def __init__(self, code, reason):
        self.code = code
        self.reason = reason
        super().__init__(format_close(code, reason))


class ConnectionClosedError(ConnectionClosed):
    __doc__ = '\n    Like :exc:`ConnectionClosed`, when the connection terminated with an error.\n\n    This means the close code is different from 1000 (OK) and 1001 (going away).\n\n    '

    def __init__(self, code, reason):
        if not (code != 1000 and code != 1001):
            raise AssertionError
        super().__init__(code, reason)


class ConnectionClosedOK(ConnectionClosed):
    __doc__ = '\n    Like :exc:`ConnectionClosed`, when the connection terminated properly.\n\n    This means the close code is 1000 (OK) or 1001 (going away).\n\n    '

    def __init__(self, code, reason):
        if not code == 1000:
            assert code == 1001
        super().__init__(code, reason)


class InvalidHandshake(WebSocketException):
    __doc__ = '\n    Raised during the handshake when the WebSocket connection fails.\n\n    '


class SecurityError(InvalidHandshake):
    __doc__ = '\n    Raised when a handshake request or response breaks a security rule.\n\n    Security limits are hard coded.\n\n    '


class InvalidMessage(InvalidHandshake):
    __doc__ = '\n    Raised when a handshake request or response is malformed.\n\n    '


class InvalidHeader(InvalidHandshake):
    __doc__ = "\n    Raised when a HTTP header doesn't have a valid format or value.\n\n    "

    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        if value is None:
            message = f"missing {name} header"
        else:
            if value == '':
                message = f"empty {name} header"
            else:
                message = f"invalid {name} header: {value}"
        super().__init__(message)


class InvalidHeaderFormat(InvalidHeader):
    __doc__ = "\n    Raised when a HTTP header cannot be parsed.\n\n    The format of the header doesn't match the grammar for that header.\n\n    "

    def __init__(self, name, error, header, pos):
        self.name = name
        error = f"{error} at {pos} in {header}"
        super().__init__(name, error)


class InvalidHeaderValue(InvalidHeader):
    __doc__ = "\n    Raised when a HTTP header has a wrong value.\n\n    The format of the header is correct but a value isn't acceptable.\n\n    "


class InvalidOrigin(InvalidHeader):
    __doc__ = "\n    Raised when the Origin header in a request isn't allowed.\n\n    "

    def __init__(self, origin):
        super().__init__('Origin', origin)


class InvalidUpgrade(InvalidHeader):
    __doc__ = "\n    Raised when the Upgrade or Connection header isn't correct.\n\n    "


class InvalidStatusCode(InvalidHandshake):
    __doc__ = '\n    Raised when a handshake response status code is invalid.\n\n    The integer status code is available in the ``status_code`` attribute.\n\n    '

    def __init__(self, status_code):
        self.status_code = status_code
        message = f"server rejected WebSocket connection: HTTP {status_code}"
        super().__init__(message)


class NegotiationError(InvalidHandshake):
    __doc__ = '\n    Raised when negotiating an extension fails.\n\n    '


class DuplicateParameter(NegotiationError):
    __doc__ = '\n    Raised when a parameter name is repeated in an extension header.\n\n    '

    def __init__(self, name):
        self.name = name
        message = f"duplicate parameter: {name}"
        super().__init__(message)


class InvalidParameterName(NegotiationError):
    __doc__ = '\n    Raised when a parameter name in an extension header is invalid.\n\n    '

    def __init__(self, name):
        self.name = name
        message = f"invalid parameter name: {name}"
        super().__init__(message)


class InvalidParameterValue(NegotiationError):
    __doc__ = '\n    Raised when a parameter value in an extension header is invalid.\n\n    '

    def __init__(self, name, value):
        self.name = name
        self.value = value
        if value is None:
            message = f"missing value for parameter {name}"
        else:
            if value == '':
                message = f"empty value for parameter {name}"
            else:
                message = f"invalid value for parameter {name}: {value}"
        super().__init__(message)


class AbortHandshake(InvalidHandshake):
    __doc__ = '\n    Raised to abort the handshake on purpose and return a HTTP response.\n\n    This exception is an implementation detail.\n\n    The public API is :meth:`~server.WebSocketServerProtocol.process_request`.\n\n    '

    def __init__(self, status, headers, body=b''):
        self.status = status
        self.headers = Headers(headers)
        self.body = body
        message = f"HTTP {status}, {len(self.headers)} headers, {len(body)} bytes"
        super().__init__(message)


class RedirectHandshake(InvalidHandshake):
    __doc__ = '\n    Raised when a handshake gets redirected.\n\n    This exception is an implementation detail.\n\n    '

    def __init__(self, uri: str) -> None:
        self.uri = uri

    def __str__(self) -> str:
        return f"redirect to {self.uri}"


class InvalidState(WebSocketException, AssertionError):
    __doc__ = '\n    Raised when an operation is forbidden in the current state.\n\n    This exception is an implementation detail.\n\n    It should never be raised in normal circumstances.\n\n    '


class InvalidURI(WebSocketException):
    __doc__ = "\n    Raised when connecting to an URI that isn't a valid WebSocket URI.\n\n    "

    def __init__(self, uri):
        self.uri = uri
        message = "{} isn't a valid URI".format(uri)
        super().__init__(message)


class PayloadTooBig(WebSocketException):
    __doc__ = '\n    Raised when receiving a frame with a payload exceeding the maximum size.\n\n    '


class ProtocolError(WebSocketException):
    __doc__ = '\n    Raised when the other side breaks the protocol.\n\n    '


WebSocketProtocolError = ProtocolError