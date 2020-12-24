# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\protocols\authentication_providers\fileauth.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 914 bytes
from responder3.protocols.authentication_providers.dictauth import DictAuth

class FileAuth(DictAuth):

    def __init__(self):
        DictAuth.__init__(self)
        self.credential_file = None
        self.parse_credfile()

    def setup_defaults(self):
        raise Exception('There are no default settings for fileauth!')

    def setup(self, d):
        self.credential_file = d['credfile']
        self.parse_credfile()

    def test_domain(self, domain):
        return domain in self.credentials

    def parse_credfile(self):
        with open(self.credential_file, 'r') as (f):
            for line in f:
                line = line.strip()
                domain, username, password = line.strip(':')
                if domain not in self.credentials:
                    self.credentials[domain] = {}
                if username not in self.credentials[domain]:
                    self.credentials[domain][username] = password
                else:
                    print('Multiple password for %s:%s, owerwriting password!' % (domain, username))