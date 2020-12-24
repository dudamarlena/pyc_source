# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/requests_ntlm/requests_ntlm.py
# Compiled at: 2013-08-26 10:52:44
from requests.auth import AuthBase
from requests.adapters import HTTPAdapter
from .ntlm import ntlm

class HttpNtlmAuth(AuthBase):
    """HTTP NTLM Authentication Handler for Requests. Supports pass-the-hash."""

    def __init__(self, username, password):
        r"""
            :username   - Username in 'domain\username' format
            :password   - Password or hash in "ABCDABCDABCDABCD:ABCDABCDABCDABCD" format.
        """
        if ntlm is None:
            raise Exception('NTLM libraries unavailable')
        user_parts = username.split('\\', 1)
        self.domain = user_parts[0].upper()
        self.username = user_parts[1]
        self.password = password
        self.adapter = HTTPAdapter()
        return

    def retry_using_http_NTLM_auth(self, auth_header_field, auth_header, response):
        """Attempts to authenticate using HTTP NTLM challenge/response"""
        if auth_header in response.request.headers:
            return response
        request = response.request
        auth = 'NTLM %s' % ntlm.create_NTLM_NEGOTIATE_MESSAGE('%s\\%s' % (self.domain, self.username))
        request.headers[auth_header] = auth
        request.headers['Connection'] = 'Keep-Alive'
        response2 = self.adapter.send(request)
        if response2.headers.get('set-cookie'):
            headers['Cookie'] = response2.headers.get('set-cookie')
        auth_header_value = response2.headers[auth_header_field]
        ServerChallenge, NegotiateFlags = ntlm.parse_NTLM_CHALLENGE_MESSAGE(auth_header_value[5:])
        auth = 'NTLM %s' % ntlm.create_NTLM_AUTHENTICATE_MESSAGE(ServerChallenge, self.username, self.domain, self.password, NegotiateFlags)
        request.headers[auth_header] = auth
        request.headers['Connection'] = 'Close'
        response = self.adapter.send(request)
        return response

    def response_hook(self, r):
        if r.status_code == 401 and 'ntlm' in r.headers.get('www-authenticate', '').lower():
            return self.retry_using_http_NTLM_auth('www-authenticate', 'Authorization', r)
        if r.status_code == 407 and 'ntlm' in r.headers.get('proxy-authenticate', '').lower():
            return self.retry_using_http_NTLM_auth('proxy-authenticate', 'Proxy-authorization', r)
        return r

    def __call__(self, r):
        r.register_hook('response', self.response_hook)
        return r