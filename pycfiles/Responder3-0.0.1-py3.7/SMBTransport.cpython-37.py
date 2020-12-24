# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\protocols\SMB\SMBTransport.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 2084 bytes
import io, enum, asyncio
from responder3.protocols.SMB.SMB2 import SMB2Message
from responder3.protocols.SMB.SMB import SMBMessage

class SMBVersion(enum.Enum):
    V1 = 255
    V2 = 254


class SMBTransport:

    def __init__(self):
        self.zero = None
        self.length = None
        self.smbmessage = None

    @staticmethod
    def from_bytes(bbuff):
        return SMBTransport.from_buffer(io.BytesIO(bbuff))

    @staticmethod
    def from_buffer(buff):
        smbt = SMBTransport()
        smbt.zero = int.from_bytes((buff.read(1)), byteorder='little', signed=False)
        smbt.length = int.from_bytes((buff.read(3)), byteorder='little', signed=False)
        t = buff.read(smbt.length)
        version = SMBVersion(int.from_bytes((t[0]), byteorder='big', signed=False))
        if version == SMBVersion.V2:
            smbt.smbmessage = SMB2Message.from_bytes(t)
        else:
            if version == SMBVersion.V1:
                smbt.smbmessage = SMBMessage.from_bytes(t)
            else:
                raise Exception('Not SMB traffic!')
        return smbt

    @staticmethod
    async def from_streamreader(reader):
        smbt = SMBTransport()
        t = await asyncio.wait_for((reader.readexactly(1)), timeout=None)
        smbt.zero = int.from_bytes(t, byteorder='big', signed=False)
        t = await asyncio.wait_for((reader.readexactly(3)), timeout=None)
        smbt.length = int.from_bytes(t, byteorder='big', signed=False)
        t = await asyncio.wait_for((reader.readexactly(smbt.length)), timeout=None)
        version = SMBVersion(t[0])
        if version == SMBVersion.V2:
            smbt.smbmessage = SMB2Message.from_bytes(t)
        else:
            if version == SMBVersion.V1:
                smbt.smbmessage = SMBMessage.from_bytes(t)
            else:
                raise Exception('Not SMB traffic!')
        return smbt

    @staticmethod
    def construct(smbmessage):
        smbt = SMBTransport()
        smbt.zero = 0
        smbt.length = len(smbmessage.to_bytes())
        smbt.smbmessage = smbmessage
        return smbt

    def to_bytes(self):
        t = self.zero.to_bytes(1, byteorder='big', signed=False)
        t += self.length.to_bytes(3, byteorder='big', signed=False)
        t += self.smbmessage.to_bytes()
        return t