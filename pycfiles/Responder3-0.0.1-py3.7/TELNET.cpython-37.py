# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\servers\TELNET.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 2465 bytes
import enum, logging, asyncio
from responder3.core.logging.logger import *
from responder3.core.asyncio_helpers import R3ConnectionClosed
from responder3.core.commons import *
from responder3.protocols.TELNET import *
from responder3.core.servertemplate import ResponderServer, ResponderServerSession

class TELNETSession(ResponderServerSession):

    def __init__(self, connection, log_queue):
        ResponderServerSession.__init__(self, connection, log_queue, self.__class__.__name__)
        self.parser = TELNETMessageParser(self)
        self.banner = None

    def __repr__(self):
        t = '== TELNET Session ==\r\n'
        return t


class TELNET(ResponderServer):

    def init(self):
        if self.settings:
            self.parse_settings()
            return
        self.set_default_settings()

    def set_default_settings(self):
        self.session.banner = ''

    def parse_settings(self):
        if 'banner' in self.settings:
            self.session.banner = self.settings['banner']

    async def send_data(self, data, timeout=None):
        self.cwriter.write(data)
        await self.cwriter.drain()

    async def send_message(self, data, timeout=None):
        """
                Sends actual ascii data to client
                MUST NOT contain the end of line char!
                """
        self.cwriter.write((data + '\r\n').encode())
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
            elif isinstance(result[0], Exception):
                raise result[0]
            else:
                data = result[0]
            if isinstance(data, bytes):
                if self.session.banner:
                    await self.send_message(self.session.banner)
                await self.send_message('Username: ')
                continue
            if not self.username:
                self.username = data
                await self.send_message('Password: ')
                continue
            self.password = self.password or data
            cred = Credential('TELNET', username=(self.username),
              password=(self.password),
              fullhash=('%s:%s' % (self.username, self.password)))
            await self.logger.credential(cred)
            return