# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiauth\openID.py
# Compiled at: 2006-10-30 14:23:34
"""OpenID Authentication (Consumer)

OpenID is a distributed authentication system for single sign-on:

    http://openid.net/

This module is based on the consumer.py example that comes with the Python
OpenID library 1.1+.
"""
import cgi, urlparse, sys
from Cookie import SimpleCookie
try:
    import openid
except ImportError:
    print >> sys.stderr, "Failed to import the OpenID library.\nIn order to use this example, you must either install the library\n(see INSTALL in the root of the distribution) or else add the\nlibrary to python's import path (the PYTHONPATH environment variable).\n\nFor more information, see the README in the root of the library\ndistribution or http://www.openidenabled.com/\n"
    sys.exit(1)

from openid.store import filestore
from openid.consumer import consumer
from openid.oidutil import appendArgs
from openid.cryptutil import randomString
from yadis.discover import DiscoveryFailure
from urljr.fetchers import HTTPFetchingError
from wsgiauth.util import geturl, getpath, Redirect, Response
from wsgiauth.cookie import Cookie
__all__ = ['OpenID', 'openid']

def quote(s):
    """Quotes URLs passed as query parameters."""
    return '"%s"' % cgi.escape(s, 1)


def openid(store, **kw):
    """Decorator for OpenID authorized middleware."""

    def decorator(application):
        return OpenID(application, store, **kw)

    return decorator


_tracker = {}
TEMPLATE = '<html>\n  <head><title>OpenID Form</title></head>\n  <body>\n    <h1>%s</h1>\n    <p>Enter your OpenID identity URL:</p>\n      <form method="get" action=%s>\n        Identity&nbsp;URL:\n        <input type="text" name="openid_url" value=%s />\n        <input type="submit" value="Verify" />\n      </form>\n    </div>\n  </body>\n</html>'

class OpenID(Cookie):
    __module__ = __name__

    def __init__(self, app, store, **kw):
        auth = OpenIDAuth(store, **kw)
        super(OpenID, self).__init__(app, auth, **kw)
        self.authorize = auth

    def initial(self, environ, start_response):
        """Initial response to a request."""

        def cookie_response(status, headers, exc_info=None):
            headers.append(('Set-Cookie', self.generate(environ)))
            return start_response(status, headers, exc_info)

        redirect = Redirect(environ['openid.redirect'])
        return redirect(environ, cookie_response)


class OpenIDAuth(object):
    """Authenticates a URL against an OpenID Server."""
    __module__ = __name__
    cname = '_OIDA_'

    def __init__(self, store, **kw):
        self.store = filestore.FileOpenIDStore(store)
        self.tracker = kw.get('tracker', _tracker)
        self.template = kw.get('template', TEMPLATE)

    def __call__(self, environ):
        environ['openid.baseurl'] = geturl(environ, False, False)
        environ['openid.query'] = dict(cgi.parse_qsl(environ['QUERY_STRING']))
        path = getpath(environ)
        if path == '/verify':
            return self.verify(environ)
        elif path == '/process':
            return self.process(environ)
        else:
            message = 'Enter an OpenID Identifier to verify.'
            return self.response(message, environ)

    def verify(self, environ):
        """Process the form submission, initating OpenID verification."""
        openid_url = environ['openid.query'].get('openid_url')
        if not openid_url:
            message = 'Enter an OpenID Identifier to verify.'
            return self.response(message, environ)
        oidconsumer = self.getconsumer(environ)
        try:
            request = oidconsumer.begin(openid_url)
        except HTTPFetchingError, exc:
            message = 'Error in discovery: %s' % cgi.escape(str(exc.why))
            return self.response(message, environ, openid_url)
        except DiscoveryFailure, exc:
            message = 'Error in discovery: %s' % cgi.escape(str(exc[0]))
            return self.response(message, environ, openid_url)
        else:
            if request is None:
                fmt = 'No OpenID services found for %s'
                return self.response(fmt % cgi.escape(openid_url), environ)
            else:
                return self.redirect(environ, request)

        return

    def process(self, environ):
        """Handle redirect from the OpenID server."""
        oidconsumer, openid_url = self.getconsumer(environ), ''
        info = oidconsumer.complete(environ['openid.query'])
        if info.status == consumer.SUCCESS:
            redirecturl = self.tracker[self.getsid(environ)]['redirect']
            environ['openid.redirect'] = redirecturl
            if info.endpoint.canonicalID:
                return info.endpoint.canonicalID
            else:
                return info.identity_url
        elif info.status == consumer.FAILURE and info.identity_url:
            openid_url = info.identity_url
            message = 'Verification of %s failed.' % cgi.escape(openid_url)
        elif info.status == consumer.CANCEL:
            message = 'Verification cancelled'
        else:
            message = 'Verification failed.'
        return self.response(message, environ, openid_url)

    def buildurl(self, environ, action, **query):
        """Build a URL relative to the server base url, with the given
        query parameters added."""
        base = urlparse.urljoin(environ['openid.baseurl'], action)
        return appendArgs(base, query)

    def getconsumer(self, environ):
        """Get an OpenID consumer with session."""
        return consumer.Consumer(self.getsession(environ), self.store)

    def response(self, message, env, url=''):
        """Default response."""
        hdrs = [
         (
          'Set-Cookie', self.setsession(env))]
        cmessage = (
         message, quote(self.buildurl(env, 'verify')), quote(url))
        return Response(cmessage, template=self.template, headers=hdrs)

    def redirect(self, environ, request):
        """Redirect response."""
        hdrs = [
         (
          'Set-Cookie', self.setsession(environ))]
        trust_root = environ['openid.baseurl']
        return_to = self.buildurl(environ, 'process')
        redirect_url = request.redirectURL(trust_root, return_to)
        return Redirect(redirect_url, headers=hdrs)

    def getsession(self, environ):
        """Return the existing session or a new session"""
        sid = self.getsid(environ)
        if sid is None:
            sid = randomString(16, '0123456789abcdef')
            session = None
        else:
            session = self.tracker.get(sid)
        if session is None:
            session = self.tracker[sid] = {}
            session['redirect'] = geturl(environ)
        session['id'] = sid
        return session

    def getsid(self, environ):
        """Returns a session identifier."""
        cookie_str = environ.get('HTTP_COOKIE')
        if cookie_str:
            cookie_obj = SimpleCookie(cookie_str)
            sid_morsel = cookie_obj.get(self.cname, None)
            if sid_morsel is not None:
                sid = sid_morsel.value
            else:
                sid = None
        else:
            sid = None
        return sid

    def setsession(self, environ):
        """Returns a session identifier."""
        sid = self.getsession(environ)['id']
        return '%s=%s;' % (self.cname, sid)