# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\servers\MYSQL.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 5460 bytes
import enum, logging, asyncio
from responder3.core.logging.logger import *
from responder3.core.asyncio_helpers import R3ConnectionClosed
from responder3.core.commons import *
from responder3.protocols.MYSQL import *
from responder3.core.servertemplate import ResponderServer, ResponderServerSession

class MYSQLSession(ResponderServerSession):

    def __init__(self, connection, log_queue):
        ResponderServerSession.__init__(self, connection, log_queue, self.__class__.__name__)
        self.parser = MYSQLMessageParser(self)
        self.status = MYSQLSessionStatus.INITIAL_HANDSHAKE
        self.server_version = None
        self.server_challenge = None
        self.sequence_id = 0
        self.auth_type = None
        self.username = None

    def __repr__(self):
        t = '== MYSQL Session ==\r\n'
        t += 'status:      %s\r\n' % repr(self.status)
        return t


class MYSQL(ResponderServer):

    def init(self):
        if self.settings:
            self.parse_settings()
            return
        self.set_default_settings()

    def set_default_settings(self):
        self.session.server_version = '5.0.54'
        self.session.server_challenge = 'AAAAAAAAAAAAAAAAAAAA'
        self.session.auth_type = MYSQLAuthType.SECURE

    def parse_settings(self):
        if 'server_version' in self.settings:
            self.session.server_version = self.settings['server_version']
        if 'server_challenge' in self.settings:
            self.session.server_challenge = self.settings['server_challenge']
        if 'auth_type' in self.settings:
            self.session.auth_type = MYSQLAuthType(self.settings['auth_type'].upper())

    async def send_data(self, data):
        self.cwriter.write(data)
        await self.cwriter.drain()

    @r3trafficlogexception
    async def run(self):
        if self.session.auth_type == MYSQLAuthType.SECURE:
            handshake = HandshakeV10_New(self.session.server_version, self.session.server_challenge[:8], self.session.server_challenge[8:])
        else:
            if self.session.auth_type == MYSQLAuthType.PLAIN or self.session.auth_type == MYSQLAuthType.OLD:
                handshake = HandshakeV10_Clear(self.session.server_version, self.session.server_challenge[:8])
            else:
                raise Exception('Auth type not implemented! TODO! %s' % self.auth_type.name)
        await asyncio.wait_for((self.send_data(handshake.to_bytes())),
          timeout=1)
        self.session.sequence_id += 1
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
                self.session.sequence_id += 1
                if self.session.status == MYSQLSessionStatus.INITIAL_HANDSHAKE:
                    if isinstance(msg, HandshakeResponse41):
                        self.session.username = msg.username
                        if self.session.auth_type == MYSQLAuthType.SECURE:
                            fullhash = '$mysqlna$%s*%s' % (self.session.server_challenge.encode().hex(), msg.auth_response.hex())
                            cred = Credential('MYSQL', username=(msg.username),
                              fullhash=fullhash)
                            await self.logger.credential(cred)
                            return
                        elif self.session.auth_type == MYSQLAuthType.PLAIN:
                            switch = AuthSwitchRequest_Clear(self.session.sequence_id)
                            self.session.status = MYSQLSessionStatus.AUTHENTICATION_SWITCH
                            await self.send_data(switch.to_bytes())
                            continue
                        else:
                            if self.session.auth_type == MYSQLAuthType.OLD:
                                switch = AuthSwitchRequest_Old(self.session.sequence_id, self.session.server_challenge[:8])
                                self.session.status = MYSQLSessionStatus.AUTHENTICATION_SWITCH
                                await self.send_data(switch.to_bytes())
                                continue
                            else:
                                raise Exception('Auth type not implemented! TODO! %s' % self.auth_type.name)
                    else:
                        raise Exception('Unexpected packet!')
            else:
                if self.session.status == MYSQLSessionStatus.AUTHENTICATION_SWITCH:
                    if isinstance(msg, AuthSwitchResponse):
                        if self.session.auth_type == MYSQLAuthType.PLAIN:
                            cred = Credential('MYSQL-PLAIN', username=(self.session.username),
                              password=(msg.auth_plugin_data.decode()),
                              fullhash=('%s:%s' % (self.session.username, msg.auth_plugin_data.decode())))
                            await self.logger.credential(cred)
                            return
                        if self.session.auth_type == MYSQLAuthType.OLD:
                            cred = Credential('MYSQL-OLD', username=(self.session.username),
                              fullhash=('%s:%s' % (self.session.username, msg.auth_plugin_data)))
                            await self.logger.credential(cred)
                            return
                    else:
                        raise Exception('Unexpected packet!')