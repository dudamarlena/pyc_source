# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexcom_reader/packetwriter.py
# Compiled at: 2015-12-15 13:09:56
import crc16, struct

class PacketWriter(object):
    MAX_PAYLOAD = 1584
    MIN_LEN = 6
    MAX_LEN = 1590
    SOF = 1
    OFFSET_SOF = 0
    OFFSET_LENGTH = 1
    OFFSET_CMD = 3
    OFFSET_PAYLOAD = 4

    def __init__(self):
        self._packet = None
        return

    def Clear(self):
        self._packet = None
        return

    def NewSOF(self, v):
        self._packet[0] = chr(v)

    def PacketString(self):
        return ('').join(self._packet)

    def AppendCrc(self):
        self.SetLength()
        ps = self.PacketString()
        crc = crc16.crc16(ps, 0, len(ps))
        for x in struct.pack('H', crc):
            self._packet.append(x)

    def SetLength(self):
        self._packet[1] = chr(len(self._packet) + 2)

    def _Add(self, x):
        try:
            len(x)
            for y in x:
                self._Add(y)

        except:
            self._packet.append(x)

    def ComposePacket(self, command, payload=None):
        assert self._packet is None
        self._packet = ['\x01', None, '\x00', chr(command)]
        if payload:
            self._Add(payload)
        self.AppendCrc()
        return