# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/core/data_packet.py
# Compiled at: 2010-06-01 14:10:25
from dust.core.dust_packet import DustPacket

class DataPacket(DustPacket):

    def __init__(self):
        DustPacket.__init__(self)

    def createDataPacket(self, key, data, entropy):
        self.createDustPacket(key, data, entropy)

    def decodeDataPacket(self, key, packet):
        self.decodeDustPacket(key, packet)