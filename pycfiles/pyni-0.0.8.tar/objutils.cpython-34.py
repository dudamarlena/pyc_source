# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynhost/objutils.py
# Compiled at: 2015-07-09 21:30:20
# Size of source mod 2**32: 2284 bytes
import struct, socketserver
from base64 import b64encode
from hashlib import sha1
import email

class MyServer(socketserver.TCPServer):

    def __init__(self, info, handler):
        super().__init__(info, handler)
        self.messages = []


class WebSocketsHandler(socketserver.StreamRequestHandler):
    magic = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    debug = False

    def __init__(self, request, client_address, server):
        self.handshake_done = False
        super().__init__(request, client_address, server)
        self.server.messages = []

    def setup(self):
        socketserver.StreamRequestHandler.setup(self)
        if self.debug:
            print('connection established', self.client_address)

    def handle(self):
        while True:
            if not self.handshake_done:
                self.handshake()
            else:
                self.read_next_message()

    def read_next_message(self):
        length = self.rfile.read(2)[1] & 127
        if length == 126:
            length = struct.unpack('>H', self.rfile.read(2).decode('utf-8'))[0]
        elif length == 127:
            length = struct.unpack('>Q', self.rfile.read(8).decode('utf-8'))[0]
        masks = [byte for byte in self.rfile.read(4)]
        decoded = ''
        for char in self.rfile.read(length):
            decoded += chr(char ^ masks[(len(decoded) % 4)])

        self.on_message(decoded)

    def handshake(self):
        data = self.request.recv(1024).strip()
        headers = email.message_from_string(data.decode('UTF-8').split('\r\n', 1)[1])
        if headers.get('Upgrade', None) != 'websocket':
            return
        if self.debug:
            print('Handshaking...')
        key = headers['Sec-WebSocket-Key']
        digest = b64encode(sha1((key + self.magic).encode('UTF-8')).digest()).decode('UTF-8')
        response = 'HTTP/1.1 101 Switching Protocols\r\n'
        response += 'Upgrade: websocket\r\n'
        response += 'Connection: Upgrade\r\n'
        response += 'Sec-WebSocket-Accept: %s\r\n\r\n' % digest
        self.handshake_done = self.request.send(response.encode('UTF-8'))

    def on_message(self, message):
        if message.encode('utf8') != '\x03é':
            self.server.messages.append(message)