# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/urllib3/urllib3/contrib/ntlmpool.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 4201 bytes
"""
NTLM authenticating pool, contributed by erikcederstran

Issue #10, see: http://code.google.com/p/urllib3/issues/detail?id=10
"""
from __future__ import absolute_import
from logging import getLogger
from ntlm import ntlm
from .. import HTTPSConnectionPool
from packages.six.moves.http_client import HTTPSConnection
log = getLogger(__name__)

class NTLMConnectionPool(HTTPSConnectionPool):
    __doc__ = '\n    Implements an NTLM authentication version of an urllib3 connection pool\n    '
    scheme = 'https'

    def __init__(self, user, pw, authurl, *args, **kwargs):
        (super(NTLMConnectionPool, self).__init__)(*args, **kwargs)
        self.authurl = authurl
        self.rawuser = user
        user_parts = user.split('\\', 1)
        self.domain = user_parts[0].upper()
        self.user = user_parts[1]
        self.pw = pw

    def _new_conn(self):
        self.num_connections += 1
        log.debug('Starting NTLM HTTPS connection no. %d: https://%s%s', self.num_connections, self.host, self.authurl)
        headers = {'Connection': 'Keep-Alive'}
        req_header = 'Authorization'
        resp_header = 'www-authenticate'
        conn = HTTPSConnection(host=(self.host), port=(self.port))
        headers[req_header] = 'NTLM %s' % ntlm.create_NTLM_NEGOTIATE_MESSAGE(self.rawuser)
        log.debug('Request headers: %s', headers)
        conn.request('GET', self.authurl, None, headers)
        res = conn.getresponse()
        reshdr = dict(res.getheaders())
        log.debug('Response status: %s %s', res.status, res.reason)
        log.debug('Response headers: %s', reshdr)
        log.debug('Response data: %s [...]', res.read(100))
        res.fp = None
        auth_header_values = reshdr[resp_header].split(', ')
        auth_header_value = None
        for s in auth_header_values:
            if s[:5] == 'NTLM ':
                auth_header_value = s[5:]

        if auth_header_value is None:
            raise Exception('Unexpected %s response header: %s' % (resp_header, reshdr[resp_header]))
        ServerChallenge, NegotiateFlags = ntlm.parse_NTLM_CHALLENGE_MESSAGE(auth_header_value)
        auth_msg = ntlm.create_NTLM_AUTHENTICATE_MESSAGE(ServerChallenge, self.user, self.domain, self.pw, NegotiateFlags)
        headers[req_header] = 'NTLM %s' % auth_msg
        log.debug('Request headers: %s', headers)
        conn.request('GET', self.authurl, None, headers)
        res = conn.getresponse()
        log.debug('Response status: %s %s', res.status, res.reason)
        log.debug('Response headers: %s', dict(res.getheaders()))
        log.debug('Response data: %s [...]', res.read()[:100])
        if res.status != 200:
            if res.status == 401:
                raise Exception('Server rejected request: wrong username or password')
            raise Exception('Wrong server response: %s %s' % (res.status, res.reason))
        res.fp = None
        log.debug('Connection established')
        return conn

    def urlopen(self, method, url, body=None, headers=None, retries=3, redirect=True, assert_same_host=True):
        if headers is None:
            headers = {}
        headers['Connection'] = 'Keep-Alive'
        return super(NTLMConnectionPool, self).urlopen(method, url, body, headers, retries, redirect, assert_same_host)