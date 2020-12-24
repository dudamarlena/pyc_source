# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\servers\SIP.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 2668 bytes
import enum, logging, asyncio
from responder3.core.logging.logger import *
from responder3.core.asyncio_helpers import *
from responder3.core.commons import *
from responder3.protocols.SIP import *
from responder3.core.servertemplate import ResponderServer, ResponderServerSession
from responder3.protocols.authentication.loader import *

class SIPSession(ResponderServerSession):

    def __init__(self, connection, log_queue):
        ResponderServerSession.__init__(self, connection, log_queue, self.__class__.__name__)
        self.status = SIPSessionStatus.UNAUTHENTICATED
        self.auth_mecha_name, self.auth_mecha = AuthMechaLoader.from_dict({'auth_mecha': 'DIGEST'})
        self.read_cnt = 0


class SIP(ResponderServer):

    def init(self):
        pass

    async def send_data(self, data):
        self.cwriter.write(data)
        await self.cwriter.drain()

    @r3trafficlogexception
    async def run(self):
        while not self.shutdown_evt.is_set():
            if self.cproto == 'UDP':
                if self.session.read_cnt > 0:
                    return
            else:
                self.session.read_cnt += 1
                try:
                    result = await (asyncio.gather)(*[asyncio.wait_for((Request.from_streamreader(self.creader)), timeout=None)], **{'return_exceptions': True})
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
                        req = result[0]
                    if self.session.status == SIPSessionStatus.UNAUTHENTICATED:
                        auth_data = None
                        if 'authorization' in req.spec_headers:
                            auth_line = req.spec_headers['authorization']
                            m = auth_line.find(' ')
                            if m != -1:
                                atype = auth_line[:m]
                                auth_data = auth_line[m + 1:]
                        status, data = self.session.auth_mecha.do_auth(auth_data, method=(req.method), body_data=(req.data))
                        if status == AuthResult.OK or status == AuthResult.FAIL:
                            await self.logger.credential(data.to_credential())
                        if status == AuthResult.OK:
                            self.session.status = SIPSessionStatus.AUTHENTICATED
                            return
                        if status == AuthResult.FAIL:
                            self.session.status = SIPSessionStatus.AUTHFAILED
                            await self.send_data(SIP403Response().to_bytes())
                            return
                        if status == AuthResult.CONTINUE:
                            rdata = self.session.auth_mecha_name.name
                            rdata += ' %s' % data
                            resp = SIP401Response.from_request(req, rdata)
                            data = resp.to_bytes()
                            self.cwriter.write(data)
                            continue
                else:
                    return
            return