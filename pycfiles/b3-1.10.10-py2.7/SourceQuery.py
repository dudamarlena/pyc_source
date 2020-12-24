# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\lib\sourcelib\SourceQuery.py
# Compiled at: 2013-02-18 23:04:31
"""http://developer.valvesoftware.com/wiki/Server_Queries"""
import socket, struct, sys, time, StringIO
PACKETSIZE = 1400
WHOLE = -1
SPLIT = -2
A2S_INFO = ord('T')
A2S_INFO_STRING = 'Source Engine Query'
A2S_INFO_REPLY = ord('I')
A2S_PLAYER = ord('U')
A2S_PLAYER_REPLY = ord('D')
A2S_RULES = ord('V')
A2S_RULES_REPLY = ord('E')
CHALLENGE = -1
S2C_CHALLENGE = ord('A')

class SourceQueryPacket(StringIO.StringIO):

    def putByte(self, val):
        self.write(struct.pack('<B', val))

    def getByte(self):
        return struct.unpack('<B', self.read(1))[0]

    def putShort(self, val):
        self.write(struct.pack('<h', val))

    def getShort(self):
        return struct.unpack('<h', self.read(2))[0]

    def putLong(self, val):
        self.write(struct.pack('<l', val))

    def getLong(self):
        return struct.unpack('<l', self.read(4))[0]

    def getLongLong(self):
        return struct.unpack('<Q', self.read(8))[0]

    def putFloat(self, val):
        self.write(struct.pack('<f', val))

    def getFloat(self):
        return struct.unpack('<f', self.read(4))[0]

    def putString(self, val):
        self.write(val + '\x00')

    def getString(self):
        val = self.getvalue()
        start = self.tell()
        end = val.index('\x00', start)
        val = val[start:end]
        self.seek(end + 1)
        return val


class SourceQueryError(Exception):
    pass


class SourceQuery(object):
    """Example usage:

       import SourceQuery
       server = SourceQuery.SourceQuery('1.2.3.4', 27015)
       print server.ping()
       print server.info()
       print server.player()
       print server.rules()
    """

    def __init__(self, host, port=27015, timeout=1.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.udp = False

    def disconnect(self):
        if self.udp:
            self.udp.close()
            self.udp = False

    def connect(self, challenge=False):
        self.disconnect()
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.settimeout(self.timeout)
        self.udp.connect((self.host, self.port))
        if challenge:
            return self.challenge()

    def receive(self):
        packet = SourceQueryPacket(self.udp.recv(PACKETSIZE))
        typ = packet.getLong()
        if typ == WHOLE:
            return packet
        if typ == SPLIT:
            reqid = packet.getLong()
            total = packet.getByte()
            num = packet.getByte()
            splitsize = packet.getShort()
            result = [ 0 for x in xrange(total) ]
            result[num] = packet.read()
            while 0 in result:
                packet = SourceQueryPacket(self.udp.recv(PACKETSIZE))
                if packet.getLong() == SPLIT and packet.getLong() == reqid:
                    total = packet.getByte()
                    num = packet.getByte()
                    splitsize = packet.getShort()
                    result[num] = packet.read()
                else:
                    raise SourceQueryError('Invalid split packet')

            packet = SourceQueryPacket(('').join(result))
            if packet.getLong() == WHOLE:
                return packet
            raise SourceQueryError('Invalid split packet')
        else:
            raise SourceQueryError('Received invalid packet type %d' % (typ,))

    def challenge(self):
        packet = SourceQueryPacket()
        packet.putLong(WHOLE)
        packet.putByte(A2S_PLAYER)
        packet.putLong(CHALLENGE)
        self.udp.send(packet.getvalue())
        packet = self.receive()
        if packet.getByte() == S2C_CHALLENGE:
            challenge = packet.getLong()
            return challenge

    def ping(self):
        """Deprecated. Use info()['ping'] instead."""
        return self.info()['ping']

    def info(self):
        """Return a dict with server info and ping."""
        self.connect()
        packet = SourceQueryPacket()
        packet.putLong(WHOLE)
        packet.putByte(A2S_INFO)
        packet.putString(A2S_INFO_STRING)
        before = time.time()
        self.udp.send(packet.getvalue())
        packet = self.receive()
        after = time.time()
        if packet.getByte() == A2S_INFO_REPLY:
            result = {}
            result['ping'] = after - before
            result['network_version'] = packet.getByte()
            result['hostname'] = packet.getString()
            result['map'] = packet.getString()
            result['gamedir'] = packet.getString()
            result['gamedesc'] = packet.getString()
            result['appid'] = packet.getShort()
            result['numplayers'] = packet.getByte()
            result['maxplayers'] = packet.getByte()
            result['numbots'] = packet.getByte()
            result['dedicated'] = chr(packet.getByte())
            result['os'] = chr(packet.getByte())
            result['passworded'] = packet.getByte()
            result['secure'] = packet.getByte()
            result['version'] = packet.getString()
            try:
                edf = packet.getByte()
                result['edf'] = edf
                if edf & 128:
                    result['port'] = packet.getShort()
                if edf & 16:
                    result['steamid'] = packet.getLongLong()
                if edf & 64:
                    result['specport'] = packet.getShort()
                    result['specname'] = packet.getString()
                if edf & 32:
                    result['tag'] = packet.getString()
            except:
                pass

            return result

    def player(self):
        challenge = self.connect(True)
        packet = SourceQueryPacket()
        packet.putLong(WHOLE)
        packet.putByte(A2S_PLAYER)
        packet.putLong(challenge)
        self.udp.send(packet.getvalue())
        packet = self.receive()
        if packet.getByte() == A2S_PLAYER_REPLY:
            numplayers = packet.getByte()
            result = []
            try:
                for x in xrange(numplayers):
                    player = {}
                    player['index'] = packet.getByte()
                    player['name'] = packet.getString()
                    player['kills'] = packet.getLong()
                    player['time'] = packet.getFloat()
                    result.append(player)

            except:
                pass

            return result

    def rules(self):
        challenge = self.connect(True)
        packet = SourceQueryPacket()
        packet.putLong(WHOLE)
        packet.putByte(A2S_RULES)
        packet.putLong(challenge)
        self.udp.send(packet.getvalue())
        packet = self.receive()
        if packet.getByte() == A2S_RULES_REPLY:
            rules = {}
            numrules = packet.getShort()
            while 1:
                try:
                    key = packet.getString()
                    rules[key] = packet.getString()
                except:
                    break

            return rules