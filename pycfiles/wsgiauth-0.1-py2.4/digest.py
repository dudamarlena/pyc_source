# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiauth\digest.py
# Compiled at: 2006-10-30 14:24:18
"""HTTP Digest Authentication

This module implements digest HTTP authentication as described in the
HTTP 1.1 specification:

http://www.w3.org/Protocols/HTTP/1.1/spec.html#DigestAA
"""
import md5, time, random
from wsgiauth.base import HTTPAuth, Scheme
__all__ = [
 'digest', 'digest_password']

def digest_password(realm, username, password):
    """ construct the appropriate hashcode needed for HTTP digest """
    return md5.new('%s:%s:%s' % (username, realm, password)).hexdigest()


def digest(realm, authfunc, **kw):
    """Decorator for HTTP digest middleware."""

    def decorator(application):
        return HTTPAuth(application, realm, authfunc, DigestAuth, **kw)

    return decorator


_nonce = dict()

class DigestAuth(Scheme):
    """Performs HTTP digest authentication."""
    __module__ = __name__
    authtype = 'digest'

    def __init__(self, realm, authfunc, **kw):
        super(DigestAuth, self).__init__(realm, authfunc, **kw)
        self.nonce = kw.get('nonce', _nonce)

    def _response(self, stale=''):
        """Builds the authentication error."""

        def coroutine(environ, start_response):
            nonce = md5.new('%s:%s' % (time.time(), random.random())).hexdigest()
            opaque = md5.new('%s:%s' % (time.time(), random.random())).hexdigest()
            self.nonce[nonce] = None
            parts = {'realm': self.realm, 'qop': 'auth', 'nonce': nonce, 'opaque': opaque}
            if stale:
                parts['stale'] = 'true'
            head = (', ').join([ '%s="%s"' % (k, v) for (k, v) in parts.items() ])
            start_response('401 Unauthorized', [('content-type', 'text/plain'), ('WWW-Authenticate', 'Digest %s' % head)])
            return [
             self.message]

        return coroutine

    def compute(self, ha1, username, response, method, path, nonce, nc, cnonce, qop):
        """Computes the authentication, raises error if unsuccessful."""
        if not ha1:
            return self.response()
        ha2 = md5.new('%s:%s' % (method, path)).hexdigest()
        if qop:
            chk = '%s:%s:%s:%s:%s:%s' % (ha1, nonce, nc, cnonce, qop, ha2)
        else:
            chk = '%s:%s:%s' % (ha1, nonce, ha2)
        if response != md5.new(chk).hexdigest():
            if nonce in self.nonce:
                del self.nonce[nonce]
            return self.response()
        pnc = self.nonce.get(nonce, '00000000')
        if nc <= pnc:
            if nonce in self.nonce:
                del self.nonce[nonce]
            return self.response(stale=True)
        self.nonce[nonce] = nc
        return username

    def __call__(self, environ):
        """This function takes a WSGI environment and authenticates
        the request returning authenticated user or error.
        """
        method = environ['REQUEST_METHOD']
        fullpath = environ['SCRIPT_NAME'] + environ['PATH_INFO']
        authorization = environ.get('HTTP_AUTHORIZATION')
        if authorization is None:
            return self.response()
        (authmeth, auth) = authorization.split(' ', 1)
        if 'digest' != authmeth.lower():
            return self.response()
        amap = dict()
        for itm in auth.split(', '):
            (k, v) = [ s.strip() for s in itm.split('=', 1) ]
            amap[k] = v.replace('"', '')

        try:
            username = amap['username']
            authpath = amap['uri']
            nonce = amap['nonce']
            realm = amap['realm']
            response = amap['response']
            assert authpath.split('?', 1)[0] in fullpath
            assert realm == self.realm
            qop = amap.get('qop', '')
            cnonce = amap.get('cnonce', '')
            nc = amap.get('nc', '00000000')
            if qop:
                assert 'auth' == qop
                assert nonce and nc
        except:
            return self.response()

        ha1 = self.authfunc(environ, realm, username)
        return self.compute(ha1, username, response, method, authpath, nonce, nc, cnonce, qop)