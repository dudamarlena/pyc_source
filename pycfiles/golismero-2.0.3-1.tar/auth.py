# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/requests/auth.py
# Compiled at: 2013-08-26 10:52:44
"""
requests.auth
~~~~~~~~~~~~~

This module contains the authentication handlers for Requests.
"""
import os, re, time, hashlib, logging
from base64 import b64encode
from .compat import urlparse, str
from .utils import parse_dict_header
log = logging.getLogger(__name__)
CONTENT_TYPE_FORM_URLENCODED = 'application/x-www-form-urlencoded'
CONTENT_TYPE_MULTI_PART = 'multipart/form-data'

def _basic_auth_str(username, password):
    """Returns a Basic Auth string."""
    return 'Basic ' + b64encode(('%s:%s' % (username, password)).encode('latin1')).strip().decode('latin1')


class AuthBase(object):
    """Base class that all auth implementations derive from"""

    def __call__(self, r):
        raise NotImplementedError('Auth hooks must be callable.')


class HTTPBasicAuth(AuthBase):
    """Attaches HTTP Basic Authentication to the given Request object."""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __call__(self, r):
        r.headers['Authorization'] = _basic_auth_str(self.username, self.password)
        return r


class HTTPProxyAuth(HTTPBasicAuth):
    """Attaches HTTP Proxy Authentication to a given Request object."""

    def __call__(self, r):
        r.headers['Proxy-Authorization'] = _basic_auth_str(self.username, self.password)
        return r


class HTTPDigestAuth(AuthBase):
    """Attaches HTTP Digest Authentication to the given Request object."""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.last_nonce = ''
        self.nonce_count = 0
        self.chal = {}

    def build_digest_header(self, method, url):
        realm = self.chal['realm']
        nonce = self.chal['nonce']
        qop = self.chal.get('qop')
        algorithm = self.chal.get('algorithm')
        opaque = self.chal.get('opaque')
        if algorithm is None:
            _algorithm = 'MD5'
        else:
            _algorithm = algorithm.upper()
        if _algorithm == 'MD5':

            def md5_utf8(x):
                if isinstance(x, str):
                    x = x.encode('utf-8')
                return hashlib.md5(x).hexdigest()

            hash_utf8 = md5_utf8
        elif _algorithm == 'SHA':

            def sha_utf8(x):
                if isinstance(x, str):
                    x = x.encode('utf-8')
                return hashlib.sha1(x).hexdigest()

            hash_utf8 = sha_utf8
        KD = lambda s, d: hash_utf8('%s:%s' % (s, d))
        if hash_utf8 is None:
            return
        else:
            entdig = None
            p_parsed = urlparse(url)
            path = p_parsed.path
            if p_parsed.query:
                path += '?' + p_parsed.query
            A1 = '%s:%s:%s' % (self.username, realm, self.password)
            A2 = '%s:%s' % (method, path)
            if qop == 'auth':
                if nonce == self.last_nonce:
                    self.nonce_count += 1
                else:
                    self.nonce_count = 1
                ncvalue = '%08x' % self.nonce_count
                s = str(self.nonce_count).encode('utf-8')
                s += nonce.encode('utf-8')
                s += time.ctime().encode('utf-8')
                s += os.urandom(8)
                cnonce = hashlib.sha1(s).hexdigest()[:16]
                noncebit = '%s:%s:%s:%s:%s' % (nonce, ncvalue, cnonce, qop, hash_utf8(A2))
                respdig = KD(hash_utf8(A1), noncebit)
            elif qop is None:
                respdig = KD(hash_utf8(A1), '%s:%s' % (nonce, hash_utf8(A2)))
            else:
                return
            self.last_nonce = nonce
            base = 'username="%s", realm="%s", nonce="%s", uri="%s", response="%s"' % (
             self.username, realm, nonce, path, respdig)
            if opaque:
                base += ', opaque="%s"' % opaque
            if algorithm:
                base += ', algorithm="%s"' % algorithm
            if entdig:
                base += ', digest="%s"' % entdig
            if qop:
                base += ', qop=auth, nc=%s, cnonce="%s"' % (ncvalue, cnonce)
            return 'Digest %s' % base

    def handle_401(self, r, **kwargs):
        """Takes the given response and tries digest-auth, if needed."""
        num_401_calls = getattr(self, 'num_401_calls', 1)
        s_auth = r.headers.get('www-authenticate', '')
        if 'digest' in s_auth.lower() and num_401_calls < 2:
            setattr(self, 'num_401_calls', num_401_calls + 1)
            pat = re.compile('digest ', flags=re.IGNORECASE)
            self.chal = parse_dict_header(pat.sub('', s_auth, count=1))
            r.content
            r.raw.release_conn()
            r.request.headers['Authorization'] = self.build_digest_header(r.request.method, r.request.url)
            _r = r.connection.send(r.request, **kwargs)
            _r.history.append(r)
            return _r
        setattr(self, 'num_401_calls', 1)
        return r

    def __call__(self, r):
        if self.last_nonce:
            r.headers['Authorization'] = self.build_digest_header(r.method, r.url)
        r.register_hook('response', self.handle_401)
        return r