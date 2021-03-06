# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/websockets/websockets/http.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 11826 bytes
"""
:mod:`websockets.http` module provides basic HTTP/1.1 support. It is merely
:adequate for WebSocket handshake messages.

These APIs cannot be imported from :mod:`websockets`. They must be imported
from :mod:`websockets.http`.

"""
import asyncio, re, sys
from typing import Any, Dict, Iterable, Iterator, List, Mapping, MutableMapping, Tuple, Union
from .version import version as websockets_version
__all__ = [
 'read_request',
 'read_response',
 'Headers',
 'MultipleValuesError',
 'USER_AGENT']
MAX_HEADERS = 256
MAX_LINE = 4096
USER_AGENT = f"Python/{sys.version[:3]} websockets/{websockets_version}"

def d(value: bytes) -> str:
    """
    Decode a bytestring for interpolating into an error message.

    """
    return value.decode(errors='backslashreplace')


_token_re = re.compile(b"[-!#$%&\\'*+.^_`|~0-9a-zA-Z]+")
_value_re = re.compile(b'[\\x09\\x20-\\x7e\\x80-\\xff]*')

async def read_request(stream: asyncio.StreamReader) -> Tuple[(str, 'Headers')]:
    """
    Read an HTTP/1.1 GET request and return ``(path, headers)``.

    ``path`` isn't URL-decoded or validated in any way.

    ``path`` and ``headers`` are expected to contain only ASCII characters.
    Other characters are represented with surrogate escapes.

    :func:`read_request` doesn't attempt to read the request body because
    WebSocket handshake requests don't have one. If the request contains a
    body, it may be read from ``stream`` after this coroutine returns.

    :param stream: input to read the request from
    :raises EOFError: if the connection is closed without a full HTTP request
    :raises SecurityError: if the request exceeds a security limit
    :raises ValueError: if the request isn't well formatted

    """
    try:
        request_line = await read_line(stream)
    except EOFError as exc:
        try:
            raise EOFError('connection closed while reading HTTP request line') from exc
        finally:
            exc = None
            del exc

    try:
        method, raw_path, version = request_line.split(b' ', 2)
    except ValueError:
        raise ValueError(f"invalid HTTP request line: {d(request_line)}") from None

    if method != b'GET':
        raise ValueError(f"unsupported HTTP method: {d(method)}")
    if version != b'HTTP/1.1':
        raise ValueError(f"unsupported HTTP version: {d(version)}")
    path = raw_path.decode('ascii', 'surrogateescape')
    headers = await read_headers(stream)
    return (
     path, headers)


async def read_response(stream: asyncio.StreamReader) -> Tuple[(int, str, 'Headers')]:
    """
    Read an HTTP/1.1 response and return ``(status_code, reason, headers)``.

    ``reason`` and ``headers`` are expected to contain only ASCII characters.
    Other characters are represented with surrogate escapes.

    :func:`read_request` doesn't attempt to read the response body because
    WebSocket handshake responses don't have one. If the response contains a
    body, it may be read from ``stream`` after this coroutine returns.

    :param stream: input to read the response from
    :raises EOFError: if the connection is closed without a full HTTP response
    :raises SecurityError: if the response exceeds a security limit
    :raises ValueError: if the response isn't well formatted

    """
    try:
        status_line = await read_line(stream)
    except EOFError as exc:
        try:
            raise EOFError('connection closed while reading HTTP status line') from exc
        finally:
            exc = None
            del exc

    try:
        version, raw_status_code, raw_reason = status_line.split(b' ', 2)
    except ValueError:
        raise ValueError(f"invalid HTTP status line: {d(status_line)}") from None

    if version != b'HTTP/1.1':
        raise ValueError(f"unsupported HTTP version: {d(version)}")
    try:
        status_code = int(raw_status_code)
    except ValueError:
        raise ValueError(f"invalid HTTP status code: {d(raw_status_code)}") from None

    if not 100 <= status_code < 1000:
        raise ValueError(f"unsupported HTTP status code: {d(raw_status_code)}")
    if not _value_re.fullmatch(raw_reason):
        raise ValueError(f"invalid HTTP reason phrase: {d(raw_reason)}")
    reason = raw_reason.decode()
    headers = await read_headers(stream)
    return (
     status_code, reason, headers)


async def read_headers(stream: asyncio.StreamReader) -> 'Headers':
    """
    Read HTTP headers from ``stream``.

    Non-ASCII characters are represented with surrogate escapes.

    """
    headers = Headers()
    for _ in range(MAX_HEADERS + 1):
        try:
            line = await read_line(stream)
        except EOFError as exc:
            try:
                raise EOFError('connection closed while reading HTTP headers') from exc
            finally:
                exc = None
                del exc

        if line == b'':
            break
        try:
            raw_name, raw_value = line.split(b':', 1)
        except ValueError:
            raise ValueError(f"invalid HTTP header line: {d(line)}") from None

        if not _token_re.fullmatch(raw_name):
            raise ValueError(f"invalid HTTP header name: {d(raw_name)}")
        raw_value = raw_value.strip(b' \t')
        if not _value_re.fullmatch(raw_value):
            raise ValueError(f"invalid HTTP header value: {d(raw_value)}")
        name = raw_name.decode('ascii')
        value = raw_value.decode('ascii', 'surrogateescape')
        headers[name] = value
    else:
        raise websockets.exceptions.SecurityError('too many HTTP headers')

    return headers


async def read_line(stream: asyncio.StreamReader) -> bytes:
    """
    Read a single line from ``stream``.

    CRLF is stripped from the return value.

    """
    line = await stream.readline()
    if len(line) > MAX_LINE:
        raise websockets.exceptions.SecurityError('line too long')
    if not line.endswith(b'\r\n'):
        raise EOFError('line without CRLF')
    return line[:-2]


class MultipleValuesError(LookupError):
    __doc__ = '\n    Exception raised when :class:`Headers` has more than one value for a key.\n\n    '

    def __str__(self):
        if len(self.args) == 1:
            return repr(self.args[0])
        return super().__str__()


class Headers(MutableMapping[(str, str)]):
    __doc__ = "\n    Efficient data structure for manipulating HTTP headers.\n\n    A :class:`list` of ``(name, values)`` is inefficient for lookups.\n\n    A :class:`dict` doesn't suffice because header names are case-insensitive\n    and multiple occurrences of headers with the same name are possible.\n\n    :class:`Headers` stores HTTP headers in a hybrid data structure to provide\n    efficient insertions and lookups while preserving the original data.\n\n    In order to account for multiple values with minimal hassle,\n    :class:`Headers` follows this logic:\n\n    - When getting a header with ``headers[name]``:\n        - if there's no value, :exc:`KeyError` is raised;\n        - if there's exactly one value, it's returned;\n        - if there's more than one value, :exc:`MultipleValuesError` is raised.\n\n    - When setting a header with ``headers[name] = value``, the value is\n      appended to the list of values for that header.\n\n    - When deleting a header with ``del headers[name]``, all values for that\n      header are removed (this is slow).\n\n    Other methods for manipulating headers are consistent with this logic.\n\n    As long as no header occurs multiple times, :class:`Headers` behaves like\n    :class:`dict`, except keys are lower-cased to provide case-insensitivity.\n\n    Two methods support support manipulating multiple values explicitly:\n\n    - :meth:`get_all` returns a list of all values for a header;\n    - :meth:`raw_items` returns an iterator of ``(name, values)`` pairs.\n\n    "
    __slots__ = [
     '_dict', '_list']

    def __init__(self, *args: Any, **kwargs: str) -> None:
        self._dict = {}
        self._list = []
        (self.update)(*args, **kwargs)

    def __str__(self) -> str:
        return ''.join((f"{key}: {value}\r\n" for key, value in self._list)) + '\r\n'

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._list!r})"

    def copy(self) -> 'Headers':
        copy = self.__class__()
        copy._dict = self._dict.copy()
        copy._list = self._list.copy()
        return copy

    def __contains__(self, key: object) -> bool:
        return isinstance(key, str) and key.lower() in self._dict

    def __iter__(self) -> Iterator[str]:
        return iter(self._dict)

    def __len__(self) -> int:
        return len(self._dict)

    def __getitem__(self, key: str) -> str:
        value = self._dict[key.lower()]
        if len(value) == 1:
            return value[0]
        raise MultipleValuesError(key)

    def __setitem__(self, key: str, value: str) -> None:
        self._dict.setdefault(key.lower(), []).append(value)
        self._list.append((key, value))

    def __delitem__(self, key: str) -> None:
        key_lower = key.lower()
        self._dict.__delitem__(key_lower)
        self._list = [(k, v) for k, v in self._list if k.lower() != key_lower]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Headers):
            return NotImplemented
        return self._list == other._list

    def clear(self) -> None:
        """
        Remove all headers.

        """
        self._dict = {}
        self._list = []

    def get_all(self, key: str) -> List[str]:
        """
        Return the (possibly empty) list of all values for a header.

        :param key: header name

        """
        return self._dict.get(key.lower(), [])

    def raw_items(self) -> Iterator[Tuple[(str, str)]]:
        """
        Return an iterator of all values as ``(name, value)`` pairs.

        """
        return iter(self._list)


HeadersLike = Union[(Headers, Mapping[(str, str)], Iterable[Tuple[(str, str)]])]
import websockets.exceptions