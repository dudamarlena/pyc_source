# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/websockets/websockets/uri.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 2244 bytes
"""
:mod:`websockets.uri` parses WebSocket URIs.

See `section 3 of RFC 6455`_.

.. _section 3 of RFC 6455: http://tools.ietf.org/html/rfc6455#section-3

"""
import urllib.parse
from typing import NamedTuple, Optional, Tuple
from .exceptions import InvalidURI
__all__ = [
 'parse_uri', 'WebSocketURI']

class WebSocketURI(NamedTuple):
    __doc__ = "\n    WebSocket URI.\n\n    :param bool secure: secure flag\n    :param str host: lower-case host\n    :param int port: port, always set even if it's the default\n    :param str resource_name: path and optional query\n    :param str user_info: ``(username, password)`` tuple when the URI contains\n      `User Information`_, else ``None``.\n\n    .. _User Information: https://tools.ietf.org/html/rfc3986#section-3.2.1\n    "
    secure: bool
    host: str
    port: int
    resource_name: str
    user_info: Optional[Tuple[(str, str)]]


WebSocketURI.secure.__doc__ = ''
WebSocketURI.host.__doc__ = ''
WebSocketURI.port.__doc__ = ''
WebSocketURI.resource_name.__doc__ = ''
WebSocketURI.user_info.__doc__ = ''

def parse_uri(uri: str) -> WebSocketURI:
    """
    Parse and validate a WebSocket URI.

    :raises ValueError: if ``uri`` isn't a valid WebSocket URI.

    """
    parsed = urllib.parse.urlparse(uri)
    try:
        assert parsed.scheme in ('ws', 'wss')
        assert parsed.params == ''
        assert parsed.fragment == ''
        assert parsed.hostname is not None
    except AssertionError as exc:
        try:
            raise InvalidURI(uri) from exc
        finally:
            exc = None
            del exc

    secure = parsed.scheme == 'wss'
    host = parsed.hostname
    port = parsed.port or (443 if secure else 80)
    resource_name = parsed.path or '/'
    if parsed.query:
        resource_name += '?' + parsed.query
    user_info = None
    if parsed.username is not None:
        if parsed.password is None:
            raise InvalidURI(uri)
        user_info = (
         parsed.username, parsed.password)
    return WebSocketURI(secure, host, port, resource_name, user_info)