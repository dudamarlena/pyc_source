# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\protocols\authentication\loader.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 1633 bytes
from responder3.protocols.authentication.common import *
from responder3.protocols.authentication.CRAM import *
from responder3.protocols.authentication.DIGEST import *
import responder3.protocols.authentication.BASIC as BASIC
from responder3.protocols.authentication.SASL import *
from responder3.protocols.authentication.NTLM import NTLMAUTHHandler
from responder3.protocols.authentication_providers.dictauth import DictAuth
from responder3.protocols.authentication_providers.fileauth import FileAuth
from responder3.protocols.authentication_providers.common import *

class AuthMechaLoader:

    def __init__(self):
        pass

    @staticmethod
    def from_dict(d):
        mecha = AuthMecha(d['auth_mecha'].upper())
        credential_provider = DictAuth()
        credential_provider.setup_defaults()
        if 'credentials_provider' in d:
            credential_provider = credprov2class[d['credentials_provider']['name'].upper()]()
            if 'settings' in d['credentials_provider']:
                credential_provider.setup(d['credentials_provider']['settings'])
            else:
                credential_provider.setup_defaults()
        else:
            auth_obj = authmecha2class[mecha](credential_provider)
            if 'settings' in d:
                auth_obj.setup(d['settings'])
            else:
                auth_obj.setup_defaults()
        return (
         mecha, auth_obj)

    @staticmethod
    def from_json(self, data):
        return AuthMechaLoader.from_dict(json.loads(data))


authmecha2class = {AuthMecha.BASIC: BASIC, 
 AuthMecha.CRAM: None, 
 AuthMecha.DIGEST: DIGEST, 
 AuthMecha.SASL: None, 
 AuthMecha.NTLM: NTLMAUTHHandler}
credprov2class = {CredProvider.DICT: DictAuth, 
 CredProvider.FILE: FileAuth}