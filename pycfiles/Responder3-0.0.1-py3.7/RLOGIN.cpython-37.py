# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\servers\RLOGIN.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 1721 bytes
import enum, logging, asyncio
from responder3.core.logging.logger import *
from responder3.core.asyncio_helpers import R3ConnectionClosed
from responder3.core.commons import *
from responder3.protocols.RLOGIN import *
from responder3.core.servertemplate import ResponderServer, ResponderServerSession

class RLOGINSession(ResponderServerSession):

    def __init__(self, connection, log_queue):
        ResponderServerSession.__init__(self, connection, log_queue, self.__class__.__name__)
        self.current_state = RloginSessionState.BEFORE_AUTH


class RLOGIN(ResponderServer):

    def init(self):
        pass

    async def send_data(self, data):
        self.cwriter.write(data)
        await self.cwriter.drain()

    @r3trafficlogexception
    async def run(self):
        while not self.shutdown_evt.is_set():
            if self.session.current_state == RloginSessionState.BEFORE_AUTH:
                try:
                    result = await (asyncio.gather)(*[AuthenticationMessage.from_streamreader((self.creader), timeout=None)], **{'return_exceptions': True})
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
                    auth_msg = result[0]
                await self.logger.credential(auth_msg.to_credential())
                return
            if self.session.current_state == RloginSessionState.AUTHENTICATED:
                return
            raise Exception('Unknown RLOGIN state!')