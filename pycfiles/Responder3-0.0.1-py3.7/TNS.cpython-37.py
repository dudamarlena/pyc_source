# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\servers\TNS.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 2508 bytes
import enum, logging, asyncio
from responder3.core.logging.logger import *
from responder3.core.asyncio_helpers import R3ConnectionClosed
from responder3.core.commons import *
from responder3.protocols.TNS import *
from responder3.core.servertemplate import ResponderServer, ResponderServerSession

class TNSSession(ResponderServerSession):

    def __init__(self, connection, log_queue):
        ResponderServerSession.__init__(self, connection, log_queue, self.__class__.__name__)
        self.parser = TNSPacket
        self.firstpacket = True

    def __repr__(self):
        t = '== TNS Session ==\r\n'
        return t


class TNS(ResponderServer):

    def init(self):
        pass

    async def send_data(self, data):
        self.cwriter.write(data)
        await self.cwriter.drain()

    @r3trafficlogexception
    async def run(self):
        while not self.shutdown_evt.is_set():
            try:
                result = await (asyncio.gather)(*[asyncio.wait_for((self.session.parser.from_streamreader(self.creader)), timeout=None)], **{'return_exceptions': True})
            except asyncio.CancelledError as e:
                try:
                    raise e
                finally:
                    e = None
                    del e

            if isinstance(result[0], R3ConnectionClosed):
                return
                if isinstance(result[0], Exception):
                    raise result[0]
                else:
                    msg = result[0]
                print(msg)
                if self.session.firstpacket == True:
                    ta = TNSResend()
                    packet = TNSPacket()
                    packet.payload = ta
                    await self.send_data(packet.to_bytes())
                    self.session.firstpacket = False
                    continue
                if msg.header.packet_type == TNSPacketType.CONNECT:
                    ta = TNSAccept()
                    ta.version = 308
                    ta.service_flags = 0
                    ta.sdu_size = 2048
                    ta.maximum_tdu_size = 32767
                    ta.byte_order = 256
                    ta.data_length = None
                    ta.data_offset = 24
                    ta.flags1 = 65
                    ta.flags2 = 1
                    ta.padding = None
                    ta.data = None
                    packet = TNSPacket()
                    packet.payload = ta
                    await self.send_data(packet.to_bytes())
            elif msg.header.packet_type == TNSPacketType.DATA:
                t = 'deadbeef00920a2001000004000004000300000000000400050a2001000008000100000b58884d7db000120001deadbeef00030000000400040001000100020001000300000000000400050a20010000020003e0e100020006fcff0002000200000000000400050a200100000c0001001106100c0f0a0b080201030003000200000000000400050a20010000030001000301'
                ta = TNSData()
                ta.flags = 0
                ta.data = bytes.fromhex(t)
                packet = TNSPacket()
                packet.payload = ta
                await self.send_data(packet.to_bytes())