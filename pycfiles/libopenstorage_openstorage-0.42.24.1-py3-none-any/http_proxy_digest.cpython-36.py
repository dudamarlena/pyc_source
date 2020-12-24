# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/requests-toolbelt/requests_toolbelt/auth/http_proxy_digest.py
# Compiled at: 2020-01-10 16:25:32
# Size of source mod 2**32: 3705 bytes
"""The module containing HTTPProxyDigestAuth."""
import re
from requests import cookies, utils
from . import _digest_auth_compat as auth

class HTTPProxyDigestAuth(auth.HTTPDigestAuth):
    __doc__ = 'HTTP digest authentication between proxy\n\n    :param stale_rejects: The number of rejects indicate that:\n        the client may wish to simply retry the request\n        with a new encrypted response, without reprompting the user for a\n        new username and password. i.e., retry build_digest_header\n    :type stale_rejects: int\n    '
    _pat = re.compile('digest ', flags=(re.IGNORECASE))

    def __init__(self, *args, **kwargs):
        (super(HTTPProxyDigestAuth, self).__init__)(*args, **kwargs)
        self.stale_rejects = 0
        self.init_per_thread_state()

    @property
    def stale_rejects(self):
        thread_local = getattr(self, '_thread_local', None)
        if thread_local is None:
            return self._stale_rejects
        else:
            return thread_local.stale_rejects

    @stale_rejects.setter
    def stale_rejects(self, value):
        thread_local = getattr(self, '_thread_local', None)
        if thread_local is None:
            self._stale_rejects = value
        else:
            thread_local.stale_rejects = value

    def init_per_thread_state(self):
        try:
            super(HTTPProxyDigestAuth, self).init_per_thread_state()
        except AttributeError:
            pass

    def handle_407(self, r, **kwargs):
        """Handle HTTP 407 only once, otherwise give up

        :param r: current response
        :returns: responses, along with the new response
        """
        if r.status_code == 407 and self.stale_rejects < 2:
            s_auth = r.headers.get('proxy-authenticate')
            if s_auth is None:
                raise IOError('proxy server violated RFC 7235:407 response MUST contain header proxy-authenticate')
            else:
                if not self._pat.match(s_auth):
                    return r
            self.chal = utils.parse_dict_header(self._pat.sub('', s_auth, count=1))
            if 'Proxy-Authorization' in r.request.headers:
                if 'stale' in self.chal:
                    if self.chal['stale'].lower() == 'true':
                        self.stale_rejects += 1
                    elif self.chal['stale'].lower() == 'false':
                        raise IOError('User or password is invalid')
            r.content
            r.close()
            prep = r.request.copy()
            cookies.extract_cookies_to_jar(prep._cookies, r.request, r.raw)
            prep.prepare_cookies(prep._cookies)
            prep.headers['Proxy-Authorization'] = self.build_digest_header(prep.method, prep.url)
            _r = (r.connection.send)(prep, **kwargs)
            _r.history.append(r)
            _r.request = prep
            return _r
        else:
            return r

    def __call__(self, r):
        self.init_per_thread_state()
        if self.last_nonce:
            r.headers['Proxy-Authorization'] = self.build_digest_header(r.method, r.url)
        r.register_hook('response', self.handle_407)
        return r