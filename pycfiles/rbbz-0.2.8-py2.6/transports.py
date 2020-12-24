# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rbbz/transports.py
# Compiled at: 2015-01-16 23:47:47
import urlparse, xmlrpclib

class CookieTransportMixin:
    """A Transport request method that retains cookies over its lifetime.

    Adapted directly from http://www.lunch.org.uk/wiki/xmlrpccookies with
    permission from the author.

    The regular xmlrpclib transports ignore cookies, which causes
    a bit of a problem when you need a cookie-based login, as with
    the Bugzilla XMLRPC interface.

    So this is a helper for defining a Transport which looks for
    cookies being set in responses and saves them to add to all future
    requests.
    """
    cookies = []

    def send_cookies(self, connection):
        if self.cookies:
            for cookie in self.cookies:
                connection.putheader('Cookie', cookie)

    def request(self, host, handler, request_body, verbose=0):
        self.verbose = verbose
        h = self.make_connection(host)
        if verbose:
            h.set_debuglevel(1)
        self.send_request(h, handler, request_body)
        self.send_host(h, host)
        self.send_cookies(h)
        self.send_user_agent(h)
        self.send_content(h, request_body)
        try:
            response = h.getresponse()
        except AttributeError:
            response = h._conn.getresponse()

        for header in response.msg.getallmatchingheaders('Set-Cookie'):
            val = header.split(': ', 1)[1]
            cookie = val.split(';', 1)[0]
            self.cookies.append(cookie)

        if response.status != 200:
            raise xmlrpclib.ProtocolError(host + handler, response.status, response.reason, response.msg.headers)
        return self.parse_response(response)


class BugzillaTransportMixin(CookieTransportMixin):
    LOGIN = 'Bugzilla_login'
    LOGIN_COOKIE = 'Bugzilla_logincookie'

    def remove_bugzilla_cookies(self):
        self.cookies = [ x for x in self.cookies if not x.startswith('%s=' % self.LOGIN) if not x.startswith('%s=' % self.LOGIN_COOKIE)
                       ]

    def set_bugzilla_cookies(self, login, login_cookie):
        self.remove_bugzilla_cookies()
        self.cookies.append('%s=%s' % (self.LOGIN, login))
        self.cookies.append('%s=%s' % (self.LOGIN_COOKIE, login_cookie))

    def bugzilla_cookies(self):
        login = ''
        login_cookie = ''
        for c in self.cookies:
            (name, _, val) = c.partition('=')
            if name == self.LOGIN:
                login = val
            elif name == self.LOGIN_COOKIE:
                login_cookie = val

        return (
         login, login_cookie)


class BugzillaTransport(BugzillaTransportMixin, xmlrpclib.Transport):
    pass


class BugzillaSafeTransport(BugzillaTransportMixin, xmlrpclib.SafeTransport):
    pass


def bugzilla_transport(uri):
    """Return an appropriate Transport for the URI.

    If the URI type is https, return a CookieSafeTransport.
    If the type is http, return a CookieTransport.
    """
    if urlparse.urlparse(uri, 'http')[0] == 'https':
        return BugzillaSafeTransport()
    return BugzillaTransport()