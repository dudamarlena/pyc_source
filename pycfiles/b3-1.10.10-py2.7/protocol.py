# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\homefront\protocol.py
# Compiled at: 2016-03-08 18:42:10
"""
Module implementing the Homefront protocol. Provide the Client class which
creates a connection to a Homefront gameserver
"""
import asyncore, socket, time
from struct import pack, unpack
from hashlib import sha1

class MessageType(object):
    CONNECT = 'CC'
    CLIENT_TRANSMISSION = 'CT'
    CLIENT_DISCONNECT = 'CD'
    CLIENT_PING = 'CP'
    SERVER_ANNOUNCE = 'SA'
    SERVER_RESPONSE = 'SR'
    SERVER_DISCONNECT = 'SD'
    SERVER_TRANSMISSION = 'ST'

    @staticmethod
    def type2str(t):
        names = {MessageType.CONNECT: 'CONNECT', 
           MessageType.CLIENT_TRANSMISSION: 'CLIENT_TRANSMISSION', 
           MessageType.CLIENT_DISCONNECT: 'CLIENT_DISCONNECT', 
           MessageType.CLIENT_PING: 'CLIENT_PING', 
           MessageType.SERVER_ANNOUNCE: 'SERVER_ANNOUNCE', 
           MessageType.SERVER_RESPONSE: 'SERVER_RESPONSE', 
           MessageType.SERVER_DISCONNECT: 'SERVER_DISCONNECT', 
           MessageType.SERVER_TRANSMISSION: 'SERVER_TRANSMISSION'}
        try:
            return names[t]
        except KeyError:
            return 'unkown(%s)' % t


class ChannelType(object):
    BROADCAST = 0
    NORMAL = 1
    CHATTER = 2
    GAMEPLAY = 3
    SERVER = 4

    @staticmethod
    def type2str(t):
        names = {ChannelType.BROADCAST: 'BROADCAST', 
           ChannelType.NORMAL: 'NORMAL', 
           ChannelType.CHATTER: 'CHATTER', 
           ChannelType.GAMEPLAY: 'GAMEPLAY', 
           ChannelType.SERVER: 'SERVER'}
        try:
            return names[t]
        except KeyError:
            return 'unkown(%s)' % t


class Packet(object):
    message = None
    channel = None
    data = None

    def encode(self):
        s = self.message[0:2]
        s += pack('>i', len(self.data))
        s += self.data.encode('utf-8')
        return s

    def decode(self, packet):
        if len(packet) <= 7:
            raise ValueError('too few data to extract a packet')
        self.message = packet[0:2]
        self.channel, = unpack('>B', packet[2])
        datalength = Packet.decodeIncomingPacketSize(packet)
        str = packet[7:7 + datalength]
        self.data = str.decode('utf-8')

    @staticmethod
    def decodeIncomingPacketSize(packet):
        return unpack('>i', packet[3:7])[0]

    def getMessageTypeAsStr(self):
        return MessageType.type2str(self.message)

    def getChannelTypeAsStr(self):
        return ChannelType.type2str(self.channel)

    def __str__(self):
        return '[Message: %s], [Channel: %s], [Data: %s]' % (self.getMessageTypeAsStr(), self.getChannelTypeAsStr(), self.data)


class Client(asyncore.dispatcher_with_send):

    def __init__(self, console, host, port, password, keepalive=False):
        asyncore.dispatcher_with_send.__init__(self)
        self.console = console
        self._host = host
        self._port = port
        self._password = password
        self.keepalive = keepalive
        self._buffer_in = ''
        self.authed = False
        self.server_version = None
        self.last_pong_time = self.last_ping_time = time.time()
        self._handlers = set()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self._host, self._port))
        return

    def handle_connect(self):
        self.console.verbose('now connected to Homefront gameserver')
        self.login()
        self.ping()

    def handle_close(self):
        self.console.verbose('connection to Homefront gameserver closed')
        self.close()
        self.authed = False
        if self.keepalive:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect((self._host, self._port))

    def handle_read(self):
        data = self.recv(8192)
        self.console.verbose2('read %s char from Homefront gameserver' % len(data))
        self._buffer_in += data
        p = self._readPacket()
        while p is not None:
            for handler in self._handlers:
                try:
                    handler(p)
                except Exception as err:
                    self.console.exception(err)

            p = self._readPacket()

        return

    def add_listener(self, handler):
        self._handlers.add(handler)
        return self

    def remove_listener(self, handler):
        try:
            self._handlers.remove(handler)
        except:
            raise ValueError('handler is not handling this event, so cannot unhandle it')

        return self

    def login(self):
        """
        Authenticate to the server
        Message Type: ClientTransmission
        Format : PASS: "[string: SHA1Hash]"
        SHA1Hash: A 60 byte ASCII string with a 40-bit SHA1 Hash converted to 
            uppercase hexadecimal text and spaces inserted between each pair.
        """

        def twobytwo(s):
            i = 0
            while i < len(s):
                yield s[i:i + 2]
                i += 2

        sha1_pass_bytes = sha1(self._password).hexdigest()
        self.command('PASS: "%s"' % (' ').join(twobytwo(sha1_pass_bytes.upper())))

    def ping(self):
        """
        Used to keep the connection alive.
        After 10 seconds of inactivity the server will drop the connection
        """
        packet = Packet()
        packet.message = MessageType.CLIENT_PING
        packet.data = 'PING'
        try:
            self.send(packet.encode())
            self.last_ping_time = time.time()
        except socket.error as e:
            self.console.error(repr(e))

    def command(self, text):
        """
        Send command to server.
        """
        packet = Packet()
        packet.message = MessageType.CLIENT_TRANSMISSION
        packet.data = text
        try:
            self.send(packet.encode())
        except socket.error as e:
            self.console.error(repr(e))

    def _readPacket(self):
        if len(self._buffer_in) > 7:
            packetlength = Packet.decodeIncomingPacketSize(self._buffer_in)
            if len(self._buffer_in) >= 7 + packetlength:
                p = Packet()
                p.decode(self._buffer_in)
                self._buffer_in = self._buffer_in[7 + packetlength:]
                self._inspect_packet(p)
                return p

    def _inspect_packet(self, p):
        if p.data == 'PONG':
            self.last_pong_time = time.time()
        elif p.channel == ChannelType.SERVER and p.data == 'AUTH: true':
            self.authed = True
        elif p.channel == ChannelType.SERVER and p.data.startswith('HELLO: '):
            self.server_version = p.data[7:]