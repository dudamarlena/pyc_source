# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiauth\base.py
# Compiled at: 2006-10-30 14:23:34
"""Base WSGI Authentication Classes."""
import os, sha, hmac, base64, time
from datetime import datetime
from wsgiauth.util import extract, getpath, Response
__all__ = [
 'BaseAuth', 'Scheme', 'HTTPAuth']
_chars = ('').join((chr(c) for c in range(0, 255)))
_cryptsize = len(hmac.new('x', 'x', sha).hexdigest())

def getsecret():
    """Returns a 64 byte secret."""
    return ('').join((_chars[(ord(i) % len(_chars))] for i in os.urandom(64)))


def gettime(date):
    """Returns a datetime object from a date string.

    @param date Date/time string
    """
    return datetime(*time.strptime(date)[0:7])


_secret = getsecret()
_tracker = dict()
TEMPLATE = '<html>\n <head><title>Please Login</title></head>\n <body>\n  <h1>Please Login</h1>\n  <form action="%s" method="post">\n   <dl>\n    <dt>Username:</dt>\n    <dd><input type="text" name="username"></dd>\n    <dt>Password:</dt>\n    <dd><input type="password" name="password"></dd>\n   </dl>\n   <input type="submit" name="authform" />\n   <hr />\n  </form>\n </body>\n</html>'

class BaseAuth(object):
    """Base class for authentication persistence."""
    __module__ = __name__
    _tokename = '_CA_'
    authtype = None

    def __init__(self, application, authfunc, **kw):
        self.application = application
        self.authfunc = authfunc
        self._secret = kw.get('secret', _secret)
        self.response = kw.get('response', Response(template=TEMPLATE))
        self.name = kw.get('name', self._tokename)
        self.store = kw.get('tracker', _tracker)
        self.authlevel = kw.get('authlevel', 1)
        self.timeout = kw.get('timeout', 3600)
        self.namevar = kw.get('namevar', 'username')

    def __call__(self, environ, start_response):
        if not self.authenticate(environ):
            result = self.authorize(environ)
            if hasattr(result, '__call__'):
                return result(environ, start_response)
            environ['REMOTE_USER'] = result
            environ['AUTH_TYPE'] = self.authtype
            environ['REQUEST_METHOD'] = 'GET'
            environ['CONTENT_LENGTH'] = ''
            environ['CONTENT_TYPE'] = ''
            return self.initial(environ, start_response)
        return self.application(environ, start_response)

    def authorize(self, environ):
        """Checks authorization credentials for a request."""
        if environ.get('REMOTE_USER') is not None:
            return environ.get('REMOTE_USER')
        elif environ['REQUEST_METHOD'] == 'POST':
            userdata = extract(environ)
            if self.authfunc(userdata):
                return userdata[self.namevar]
            return self.response
        return self.response

    def _authtoken(self, environ, token):
        """Authenticates tokens."""
        authtoken = base64.urlsafe_b64decode(token)
        current = authtoken[:_cryptsize]
        date = gettime(authtoken[_cryptsize:].decode('hex'))
        if date > datetime.now().replace(microsecond=0):
            once = self.store[token]
            user, path, nonce = once['user'], once['path'], once['nonce']
            if self.authlevel != 4:
                agent = environ['HTTP_USER_AGENT']
                raddr = environ['REMOTE_ADDR']
                server = environ['SERVER_NAME']
                newtoken = self.compute(user, raddr, server, path, agent, nonce)
                if newtoken != current:
                    return False
            environ['REMOTE_USER'] = user
            environ['AUTH_TYPE'] = self.authtype
            return True

    def compute(self, user, raddr, server, path, agent, nonce):
        """Computes an authentication token."""
        if self.authlevel == 3 or 4:
            key = self._secret.join([path, nonce, user])
        elif self.authlevel == 2:
            key = self._secret.join([user, path, nonce, server, agent])
        elif self.authlevel == 1:
            key = self._secret.join([raddr, user, server, nonce, agent, path])
        return hmac.new(self._secret, key, sha).hexdigest()

    def _gettoken(self, environ):
        """Generates authentication tokens."""
        user, path = environ['REMOTE_USER'], getpath(environ)
        agent = environ['HTTP_USER_AGENT']
        raddr, server = environ['REMOTE_ADDR'], environ['SERVER_NAME']
        nonce = getsecret()
        authtoken = self.compute(user, raddr, server, path, agent, nonce)
        timeout = datetime.fromtimestamp(time.time() + self.timeout).ctime()
        token = base64.urlsafe_b64encode(authtoken + timeout.encode('hex'))
        self.store[token] = {'user': user, 'path': path, 'nonce': nonce}
        return token

    def authenticate(self, environ):
        """"Interface" for subclasses."""
        raise NotImplementedError()

    def generate(self, environ):
        """"Interface" for subclasses."""
        raise NotImplementedError()

    def initial(self, environ, start_response):
        """"Interface" for subclasses."""
        raise NotImplementedError()


class Scheme(object):
    """HTTP Authentication Base."""
    __module__ = __name__
    _msg = 'This server could not verify that you are authorized to\r\naccess the document you requested.  Either you supplied the\r\nwrong credentials (e.g., bad password), or your browser\r\ndoes not understand how to supply the credentials required.'

    def __init__(self, realm, authfunc, **kw):
        self.realm, self.authfunc = realm, authfunc
        self.response = kw.get('response', self._response)
        self.message = kw.get('message', self._msg)

    def _response(self, environ, start_response):
        raise NotImplementedError()


class HTTPAuth(object):
    """HTTP authentication middleware."""
    __module__ = __name__

    def __init__(self, application, realm, authfunc, scheme, **kw):
        """
        @param application WSGI application.
        @param realm Identifier for authority requesting authorization.
        @param authfunc Mandatory user-defined function
        @param scheme HTTP authentication scheme            
        """
        self.application = application
        self.authenticate = scheme(realm, authfunc, **kw)
        self.scheme = scheme.authtype

    def __call__(self, environ, start_response):
        if environ.get('REMOTE_USER') is None:
            result = self.authenticate(environ)
            if not isinstance(result, str):
                return result(environ, start_response)
            environ['REMOTE_USER'] = result
            environ['AUTH_TYPE'] = self.scheme
        return self.application(environ, start_response)