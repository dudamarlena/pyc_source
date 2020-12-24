# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cuiows/wsproto/connection.py
# Compiled at: 2017-01-22 09:55:14
# Size of source mod 2**32: 13804 bytes
__doc__ = '\nwsproto/connection\n~~~~~~~~~~~~~~\n\nAn implementation of a WebSocket connection.\n'
import os, base64, hashlib
from collections import deque
from enum import Enum
import h11
from .events import ConnectionRequested, ConnectionEstablished, ConnectionClosed, ConnectionFailed, TextReceived, BytesReceived
from .frame_protocol import FrameProtocol, ParseFailed, CloseReason, Opcode
ACCEPT_GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

class ConnectionState(Enum):
    """ConnectionState"""
    CONNECTING = 0
    OPEN = 1
    CLOSING = 2
    CLOSED = 3


class ConnectionType(Enum):
    CLIENT = 1
    SERVER = 2


CLIENT = ConnectionType.CLIENT
SERVER = ConnectionType.SERVER

class WSConnection(object):
    """WSConnection"""

    def __init__(self, conn_type, host=None, resource=None, extensions=None, subprotocols=[]):
        self.client = conn_type is ConnectionType.CLIENT
        self.host = host
        self.resource = resource
        self.subprotocols = subprotocols
        self.extensions = extensions or []
        self.version = '13'
        self._state = ConnectionState.CONNECTING
        self._close_reason = None
        self._nonce = None
        self._outgoing = ''
        self._events = deque()
        self._proto = FrameProtocol(self.client, self.extensions)
        if self.client:
            self._upgrade_connection = h11.Connection(h11.CLIENT)
        else:
            self._upgrade_connection = h11.Connection(h11.SERVER)
        if self.client:
            self.initiate_connection()

    def initiate_connection(self):
        self._generate_nonce()
        headers = {'Host': self.host.encode('ascii'), 
         'Upgrade': 'WebSocket', 
         'Connection': 'Upgrade', 
         'Sec-WebSocket-Key': self._nonce, 
         'Sec-WebSocket-Version': self.version, 
         'Sec-WebSocket-Protocol': ', '.join(self.subprotocols)}
        if self.extensions:
            offers = {e.name:e.offer(self) for e in self.extensions}
            extensions = []
            for name, params in offers.items():
                if params is True:
                    extensions.append(name.encode('ascii'))
                elif params:
                    extensions.append(('%s; %s' % (name, params)).encode('ascii'))

            if extensions:
                headers['Sec-WebSocket-Extensions'] = ', '.join(extensions)
        upgrade = h11.Request(method='GET', target=self.resource, headers=headers.items())
        self._outgoing += self._upgrade_connection.send(upgrade)

    def send_data(self, payload, final=True):
        """
        Send a message or part of a message to the remote peer.

        If ``final`` is ``False`` it indicates that this is part of a longer
        message. If ``final`` is ``True`` it indicates that this is either a
        self-contained message or the last part of a longer message.

        If ``payload`` is of type ``bytes`` then the message is flagged as
        being binary If it is of type ``str`` encoded as UTF-8 and sent as
        text.

        :param payload: The message body to send.
        :type payload: ``bytes`` or ``str``

        :param final: Whether there are more parts to this message to be sent.
        :type final: ``bool``
        """
        self._outgoing += self._proto.send_data(payload, final)

    def close(self, code=CloseReason.NORMAL_CLOSURE, reason=None):
        self._outgoing += self._proto.close(code, reason)
        self._state = ConnectionState.CLOSING

    @property
    def closed(self):
        return self._state is ConnectionState.CLOSED

    def bytes_to_send(self, amount=None):
        """
        Return any data that is to be sent to the remote peer.

        :param amount: (optional) The maximum number of bytes to be provided.
            If ``None`` or not provided it will return all available bytes.
        :type amount: ``int``
        """
        if amount is None:
            data = self._outgoing
            self._outgoing = ''
        else:
            data = self._outgoing[:amount]
            self._outgoing = self._outgoing[amount:]
        return data

    def receive_bytes(self, data):
        """
        Pass some received bytes to the connection for processing.

        :param data: The data received from the remote peer.
        :type data: ``bytes``
        """
        if data is None and self._state is ConnectionState.OPEN:
            self._events.append(ConnectionClosed(CloseReason.ABNORMAL_CLOSURE))
            self._state = ConnectionState.CLOSED
            return
        if data is None:
            self._state = ConnectionState.CLOSED
            return
        if self._state is ConnectionState.CONNECTING:
            event, data = self._process_upgrade(data)
            if event is not None:
                self._events.append(event)
        if self._state is ConnectionState.OPEN:
            self._proto.receive_bytes(data)

    def _process_upgrade(self, data):
        self._upgrade_connection.receive_data(data)
        while 1:
            event = self._upgrade_connection.next_event()
            if event is h11.NEED_DATA:
                break
            elif self.client and isinstance(event, h11.InformationalResponse):
                data = self._upgrade_connection.trailing_data[0]
                return (
                 self._establish_client_connection(event), data)
            if not self.client and isinstance(event, h11.Request):
                return (self._process_connection_request(event), None)

        self._incoming = ''
        return (None, None)

    def events(self):
        """
        Return a generator that provides any events that have been generated
        by protocol activity.

        :returns: generator
        """
        while self._events:
            yield self._events.popleft()

        try:
            for frame in self._proto.received_frames():
                if frame.opcode is Opcode.PING:
                    assert frame.frame_finished and frame.message_finished
                    self._outgoing += self._proto.pong(frame.payload)
                else:
                    if frame.opcode is Opcode.CLOSE:
                        code, reason = frame.payload
                        self.close(code, reason)
                        yield ConnectionClosed(code, reason)
                    else:
                        if frame.opcode is Opcode.TEXT:
                            yield TextReceived(frame.payload, frame.frame_finished, frame.message_finished)
                        elif frame.opcode is Opcode.BINARY:
                            yield BytesReceived(frame.payload, frame.frame_finished, frame.message_finished)

        except ParseFailed as exc:
            self.close(code=exc.code, reason=str(exc))
            yield ConnectionClosed(exc.code, reason=str(exc))

    def _generate_nonce(self):
        self._nonce = base64.b64encode(os.urandom(16))

    def _generate_accept_token(self, token):
        accept_token = token + ACCEPT_GUID
        accept_token = hashlib.sha1(accept_token).digest()
        return base64.b64encode(accept_token)

    def _establish_client_connection(self, event):
        if event.status_code != 101:
            return ConnectionFailed(CloseReason.PROTOCOL_ERROR, 'Bad status code from server')
        headers = dict(event.headers)
        if headers['connection'].lower() != 'upgrade':
            return ConnectionFailed(CloseReason.PROTOCOL_ERROR, 'Missing Connection: Upgrade header')
        if headers['upgrade'].lower() != 'websocket':
            return ConnectionFailed(CloseReason.PROTOCOL_ERROR, 'Missing Upgrade: WebSocket header')
        accept_token = self._generate_accept_token(self._nonce)
        if headers['sec-websocket-accept'] != accept_token:
            return ConnectionFailed(CloseReason.PROTOCOL_ERROR, 'Bad accept token')
        subprotocol = headers.get('sec-websocket-protocol', None)
        extensions = headers.get('sec-websocket-extensions', None)
        if extensions:
            accepts = [e.strip() for e in extensions.split(',')]
            for accept in accepts:
                accept = accept.decode('ascii')
                name = accept.split(';', 1)[0].strip()
                for extension in self.extensions:
                    if extension.name == name:
                        extension.finalize(self, accept)

        self._state = ConnectionState.OPEN
        return ConnectionEstablished(subprotocol, extensions)

    def _process_connection_request(self, event):
        if event.method != 'GET':
            return ConnectionFailed(CloseReason.PROTOCOL_ERROR, 'Request method must be GET')
        headers = dict(event.headers)
        if headers['connection'].lower() != 'upgrade':
            return ConnectionFailed(CloseReason.PROTOCOL_ERROR, 'Missing Connection: Upgrade header')
        if headers['upgrade'].lower() != 'websocket':
            return ConnectionFailed(CloseReason.PROTOCOL_ERROR, 'Missing Upgrade: WebSocket header')
        if 'sec-websocket-version' not in headers:
            return ConnectionFailed(CloseReason.PROTOCOL_ERROR, 'Missing Sec-WebSocket-Version header')
        if 'sec-websocket-key' not in headers:
            return ConnectionFailed(CloseReason.PROTOCOL_ERROR, 'Missing Sec-WebSocket-Key header')
        return ConnectionRequested(event)

    def accept(self, event):
        request = event.h11request
        request_headers = dict(request.headers)
        nonce = request_headers['sec-websocket-key']
        accept_token = self._generate_accept_token(nonce)
        headers = {'Upgrade': 'WebSocket', 
         'Connection': 'Upgrade', 
         'Sec-WebSocket-Accept': accept_token, 
         'Sec-WebSocket-Version': self.version}
        extensions = request_headers.get('sec-websocket-extensions', None)
        accepts = {}
        if extensions:
            offers = [e.strip() for e in extensions.split(',')]
            for offer in offers:
                offer = offer.decode('ascii')
                name = offer.split(';', 1)[0].strip()
                for extension in self.extensions:
                    if extension.name == name:
                        accept = extension.accept(self, offer)
                        if accept is True:
                            accepts[extension.name] = True
                        elif accept:
                            accepts[extension.name] = accept.encode('ascii')

        if accepts:
            extensions = []
            for name, params in accepts.items():
                if params is True:
                    extensions.append(name.encode('ascii'))
                else:
                    params = params.decode('ascii')
                    extensions.append(('%s; %s' % (name, params)).encode('ascii'))

            headers['Sec-WebSocket-Extensions'] = ', '.join(extensions)
        response = h11.InformationalResponse(status_code=101, headers=headers.items())
        self._outgoing += self._upgrade_connection.send(response)
        self._state = ConnectionState.OPEN