# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/Cellar/python/2.7.10_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/geventwebsocket/exceptions.py
# Compiled at: 2015-11-13 17:02:49
from socket import error as socket_error

class WebSocketError(socket_error):
    """
    Base class for all websocket errors.
    """


class ProtocolError(WebSocketError):
    """
    Raised if an error occurs when de/encoding the websocket protocol.
    """


class FrameTooLargeException(ProtocolError):
    """
    Raised if a frame is received that is too large.
    """