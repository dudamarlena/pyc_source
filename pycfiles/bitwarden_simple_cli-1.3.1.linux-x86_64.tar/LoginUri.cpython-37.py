# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/models/domain/LoginUri.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 709 bytes
from bitwarden_simple_cli.models.domain.DomainBase import Domain
import bitwarden_simple_cli.models.domain.CipherString as CipherString
import bitwarden_simple_cli.models.data.LoginData as LoginData

class LoginUri(Domain):
    uri: CipherString

    def __init__(self, obj, already_encrypted=False):
        super()
        if obj is None:
            return
        self.build_domain_model(self, obj, {'uri': None}, already_encrypted, [])

    def decrypt(self, org_id: str):
        return self.uri.decrypt(org_id)