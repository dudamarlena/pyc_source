# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cuiows/wsproto/events.py
# Compiled at: 2017-01-22 09:55:14
# Size of source mod 2**32: 2037 bytes
__doc__ = '\nwsproto/events\n~~~~~~~~~~\n\nEvents that result from processing data on a WebSocket connection.\n'

class ConnectionRequested(object):

    def __init__(self, h11request):
        self.h11request = h11request

    def __repr__(self):
        path = self.h11request.target
        headers = dict(self.h11request.headers)
        host = headers['host']
        version = headers['sec-websocket-version']
        subprotocol = headers.get('sec-websocket-protocol', None)
        extensions = []
        fmt = '<%s host=%s path=%s version=%s subprotocol=%r extensions=%r>'
        return fmt % (self.__class__.__name__, host, path, version,
         subprotocol, extensions)


class ConnectionEstablished(object):

    def __init__(self, subprotocol=None, extensions=None):
        self.subprotocol = subprotocol
        self.extensions = extensions
        if self.extensions is None:
            self.extensions = []

    def __repr__(self):
        return '<ConnectionEstablished subprotocol=%r extensions=%r>' % (
         self.subprotocol, self.extensions)


class ConnectionClosed(object):

    def __init__(self, code, reason=None):
        self.code = code
        self.reason = reason

    def __repr__(self):
        return '<%s code=%r reason="%s">' % (self.__class__.__name__,
         self.code, self.reason)


class ConnectionFailed(ConnectionClosed):
    pass


class DataReceived(object):

    def __init__(self, data, frame_finished, message_finished):
        self.data = data
        self.frame_finished = frame_finished
        self.message_finished = message_finished


class TextReceived(DataReceived):
    pass


class BytesReceived(DataReceived):
    pass