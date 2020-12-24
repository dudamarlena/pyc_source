# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\servers\LDAP.py
# Compiled at: 2019-08-15 18:27:11
# Size of source mod 2**32: 7222 bytes
import logging, asyncio
from responder3.core.logging.logger import *
from responder3.core.asyncio_helpers import R3ConnectionClosed
from responder3.core.commons import *
from responder3.protocols.LDAP import *
from responder3.core.servertemplate import ResponderServer, ResponderServerSession
from responder3.protocols.authentication.NTLM import *

class LDAPSession(ResponderServerSession):

    def __init__(self, connection, log_queue):
        ResponderServerSession.__init__(self, connection, log_queue, self.__class__.__name__)
        self.auth_type = None
        self.auth_handler = None
        self.is_authed = False
        self.parser = LdapParser

    def __repr__(self):
        t = '== LDAPSession ==\r\n'
        return t


class LDAP(ResponderServer):

    def init(self):
        self.parse_settings()

    def parse_settings(self):
        pass

    async def send_search_done(self, msg_id):
        t = {'resultCode':0, 
         'matchedDN':b'', 
         'diagnosticMessage':b''}
        po = {'searchResDone': SearchResultDone(t)}
        b = {'messageID':msg_id, 
         'protocolOp':protocolOp(po)}
        resp = LDAPMessage(b)
        self.cwriter.write(resp.dump())
        await self.cwriter.drain()

    async def send_search_result(self, msg_id, search_result_dict):
        po = {'searchResEntry': SearchResultEntry(search_result_dict)}
        b = {'messageID':msg_id, 
         'protocolOp':protocolOp(po)}
        resp = LDAPMessage(b)
        self.cwriter.write(resp.dump())
        await self.cwriter.drain()
        await self.send_search_done(msg_id)

    async def send_capabilities(self, msg_id):
        x = [
         {'type':b'supportedCapabilities', 
          'attributes':[
           '1.2.840.113556.1.4.800'.encode(),
           '1.2.840.113556.1.4.1670'.encode(),
           '1.2.840.113556.1.4.1791'.encode(),
           '1.2.840.113556.1.4.1935'.encode(),
           '1.2.840.113556.1.4.1935'.encode(),
           '1.2.840.113556.1.4.2080'.encode(),
           '1.2.840.113556.1.4.2237'.encode()]}]
        t = {'objectName':b'', 
         'attributes':PartialAttributeList(x)}
        await self.send_search_result(msg_id, t)

    async def send_sasl_mechanisms(self, msg_id):
        x = [
         {'type':b'supportedSASLMechanisms', 
          'attributes':[
           'NTLM'.encode()]}]
        t = {'objectName':b'', 
         'attributes':PartialAttributeList(x)}
        await self.send_search_result(msg_id, t)

    async def send_unauthorized_msg(self, msg_id):
        t = {'resultCode':49, 
         'matchedDN':b'', 
         'diagnosticMessage':'8009030C: LdapErr: DSID-0C0906A1, comment: AcceptSecurityContext error, data 52e, v3839'.encode()}
        po = {'bindResponse': BindResponse(t)}
        b = {'messageID':msg_id, 
         'protocolOp':protocolOp(po)}
        resp = LDAPMessage(b)
        self.cwriter.write(resp.dump())
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
                msg = result[0]
            req = msg.native
            if (isinstance(msg['protocolOp'].chosen, BindRequest) or req['protocolOp']['attributes'][0]) == b'supportedCapabilities':
                await self.send_capabilities(req['messageID'])
                continue
            else:
                if req['protocolOp']['attributes'][0] == b'supportedSASLMechanisms':
                    await self.send_sasl_mechanisms(req['messageID'])
                    continue
            if self.session.is_authed == False:
                msg_id = req['messageID']
                bindreq = msg['protocolOp'].chosen
                auth_data = req['protocolOp']['authentication']
                auth_type = bindreq['authentication'].chosen
                if (self.session.auth_type or isinstance)(auth_type, (SicilyPackageDiscovery, SicilyNegotiate)):
                    self.session.auth_type = 'NTLM'
                    self.auth_handler = NTLMAUTHHandler()
                    self.auth_handler.setup()
                else:
                    if isinstance(auth_type, SaslCredentials):
                        if auth_data['mechanism'] == b'PLAIN':
                            username, password = auth_data['credentials'][1:].split(b'\x00')
                            cred = Credential(credtype='SASL - PLAIN',
                              username=(username.decode()),
                              password=(password.decode()),
                              fullhash=('%s:%s' % (username.decode(), password.decode())))
                            await self.logger.credential(cred)
                        await self.send_unauthorized_msg(msg_id)
                        return
                    if isinstance(auth_type, core.OctetString):
                        cred = Credential(credtype='PLAIN',
                          username=(req['protocolOp']['name'].decode()),
                          password=(req['protocolOp']['authentication'].decode()),
                          fullhash=('%s:%s' % (req['protocolOp']['name'].decode(), req['protocolOp']['authentication'].decode())))
                        await self.logger.credential(cred)
                        await self.send_unauthorized_msg(msg_id)
                        return
                    if self.session.auth_type == 'NTLM':
                        if isinstance(auth_type, SicilyPackageDiscovery):
                            t = {'resultCode':0,  'matchedDN':'NTLM'.encode(), 
                             'diagnosticMessage':b''}
                            po = {'bindResponse': BindResponse(t)}
                            b = {'messageID':msg_id, 
                             'protocolOp':protocolOp(po)}
                            resp = LDAPMessage(b)
                            self.cwriter.write(resp.dump())
                            await self.cwriter.drain()
                            continue
                    elif isinstance(auth_type, SicilyNegotiate) and isinstance(self.auth_handler, NTLMAUTHHandler):
                        status, challenge = self.auth_handler.do_auth(auth_data)
                        t = {'resultCode':0, 
                         'matchedDN':challenge, 
                         'diagnosticMessage':b''}
                        po = {'bindResponse': BindResponse(t)}
                        b = {'messageID':msg_id, 
                         'protocolOp':protocolOp(po)}
                        resp = LDAPMessage(b)
                        self.cwriter.write(resp.dump())
                        await self.cwriter.drain()
                    else:
                        if isinstance(auth_type, SicilyResponse):
                            if isinstance(self.auth_handler, NTLMAUTHHandler):
                                status, cred = self.auth_handler.do_auth(auth_data)
                                if cred:
                                    await self.logger.credential(cred.to_credential())
                                await self.send_unauthorized_msg(msg_id)
                                return
                            else:
                                raise Exception('Unknown auth type!')