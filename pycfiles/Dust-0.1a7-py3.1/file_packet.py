# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/services/file/file_packet.py
# Compiled at: 2010-06-01 14:14:50
import json, time, struct, random
from dust.core.dust_packet import makeLength
from dust.core.util import encode
from dust.extensions.multiplex.multiplex_packet import MultiplexPacket

class FileMessage:

    def __init__(self):
        self.headersLength = None
        self.headersLengthValue = None
        self.headers = None
        self.data = None
        self.message = None
        return

    def createFileMessage(self, headers, data):
        self.headers = json.dumps(headers).encode('ascii')
        self.headersLengthValue = len(self.headers)
        self.headersLength = makeLength(self.headersLengthValue, 4)
        self.data = data
        if self.data:
            self.message = self.headersLength + self.headers + self.data
        else:
            self.message = self.headersLength + self.headers

    def decodeFileMessage(self, message):
        self.message = message
        self.headersLength = self.message[:4]
        self.headersLengthValue = struct.unpack('I', self.headersLength)[0]
        self.headers = json.loads(self.message[4:self.headersLengthValue + 4].decode('ascii'))
        if self.headersLengthValue + 4 == len(self.message):
            self.data = None
        else:
            self.data = self.message[self.headersLengthValue + 4:]
        return


class FilePacket(MultiplexPacket):

    def __init__(self):
        MultiplexPacket.__init__(self)
        self.file = None
        return

    def createFilePacket(self, sk, headers, data):
        self.file = FileMessage()
        self.file.createFileMessage(headers, data)
        self.createMultiplexPacket(sk, 'file', self.file.message)

    def decodeMultiplexPacket(self, sk, packet):
        self.decodeMultiplexPacket(sk, packet)
        self.file = FileMessage()
        self.file.decodeFileMessage(self.multiplex.data)