# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/models/domain/Login.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 1121 bytes
from bitwarden_simple_cli.models.domain.DomainBase import Domain
import bitwarden_simple_cli.models.domain.CipherString as CipherString
import bitwarden_simple_cli.models.data.LoginData as LoginData
import bitwarden_simple_cli.models.domain.LoginUri as LoginUri

class Login(Domain):
    username: CipherString
    password: CipherString
    uris = None
    uris: []

    def __init__(self, obj, already_encrypted=False):
        super().__init__()
        if obj is None:
            return
        self.build_domain_model(self, obj, {'username':None, 
         'password':None}, already_encrypted, [])
        if obj.get('uris'):
            self.uris = []
            for uri in obj['uris']:
                self.uris.append(LoginUri(uri, already_encrypted))

    def decrypt_field(self, field, org_id):
        return self[field].decrypt(org_id)

    def decrypt_uri(self, org_id, i=1):
        return self.uris[(i - 1)].decrypt(org_id)