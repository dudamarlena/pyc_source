# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/Cellar/python/2.7.10_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/geventwebsocket/exceptions.py
# Compiled at: 2015-11-13 17:02:49
from socket import error as socket_error

class WebSocketError(socket_error):
    """
    Base class for all websocket errors.
    """
    pass


class ProtocolError(WebSocketError):
    """
    Raised if an error occurs when de/encoding the websocket protocol.
    """
    pass


class FrameTooLargeException(ProtocolError):
    """
    Raised if a frame is received that is too large.
    """
    pass