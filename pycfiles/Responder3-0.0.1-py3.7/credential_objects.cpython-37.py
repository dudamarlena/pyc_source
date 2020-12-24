# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\protocols\authentication_providers\credential_objects.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 650 bytes
from responder3.core.logging.log_objects import Credential

class PlaintextCredential:

    def __init__(self, domain, username, password):
        self.domain = domain
        self.username = username
        self.password = password

    def to_credential(self):
        if self.domain:
            return Credential('plaintext',
              domain=(self.domain),
              username=(self.username),
              password=(self.password),
              fullhash=('%s:%s:%s' % (self.domain, self.username, self.password)))
        return Credential('plaintext',
          username=(self.username),
          password=(self.password),
          fullhash=('%s:%s' % (self.username, self.password)))