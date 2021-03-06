# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/handlers/tests/test_handlers.py
# Compiled at: 2010-12-12 04:36:57
"""Unit tests for basic request handlers and helper functions."""
import google.appengine.ext.webapp, os, typhoonae.handlers.login, unittest, webob

class LoginHandlerTestCase(unittest.TestCase):
    """Testing login handler functions."""

    def testGetCookieName(self):
        """Retrieves a cookie name."""
        self.assertEqual('typhoonae_login', typhoonae.handlers.login.getCookieName())
        os.environ['HTTP_X_APPCFG_API_VERSION'] = '1'
        self.assertEqual('dev_appserver_login', typhoonae.handlers.login.getCookieName())

    def testGetUserInfo(self):
        """Retrieves user info triple."""
        if 'HTTP_X_APPCFG_API_VERSION' in os.environ:
            del os.environ['HTTP_X_APPCFG_API_VERSION']
        (email, admin, user_id) = typhoonae.handlers.login.getUserInfo('typhoonae_login="admin@typhoonae:True:120613712819802230111"')
        self.assertEqual('admin@typhoonae', email)
        self.assertEqual('120613712819802230111', user_id)
        self.assertTrue(admin)

    def testCreateLoginCookiePayload(self):
        """Creates login cookie paylad."""
        self.assertEqual('foo@bar:True:120416216492860175112', typhoonae.handlers.login.createLoginCookiePayload('foo@bar', True))
        self.assertEqual(':False:', typhoonae.handlers.login.createLoginCookiePayload('', False))

    def testCreateLoginCookie(self):
        """Creates a login cookie."""
        from cookielib import Cookie
        cookie = typhoonae.handlers.login.createLoginCookie('foo@bar', True)
        self.assertEqual(cookie.__class__, Cookie)

    def testAuthenticate(self):
        """Authenticates user."""
        typhoonae.handlers.login.authenticate('foo@bar')

    def testGetSetCookieHeaderValue(self):
        """Retrieves a set-cookie header value."""
        if 'HTTP_X_APPCFG_API_VERSION' in os.environ:
            del os.environ['HTTP_X_APPCFG_API_VERSION']
        self.assertEqual('typhoonae_login="foo@bar:False:120416216492860175112"; Path=/', typhoonae.handlers.login.getSetCookieHeaderValue('foo@bar'))

    def testLoginRequestHandler(self):
        """Tests the login request handler."""
        handler = typhoonae.handlers.login.LoginRequestHandler()
        handler.request = google.appengine.ext.webapp.Request({})
        handler.response = google.appengine.ext.webapp.Response()
        handler.get()
        self.assertEqual('<html><body>You\'re logged in as admin@typhoonae! This is a demo login handler.<br><a href="/">Continue</a></body></html>', handler.response.out.getvalue())

    def testLogoutRequestHandler(self):
        """Tests the logout request handler."""
        handler = typhoonae.handlers.login.LogoutRequestHandler()
        handler.request = google.appengine.ext.webapp.Request({'wsgi.url_scheme': 'http', 
           'SERVER_NAME': 'test', 
           'SERVER_PORT': '8080'})
        handler.response = google.appengine.ext.webapp.Response()
        handler.get()
        self.assertEqual('typhoonae_login=; Max-Age=0; Path=/', handler.response.headers.get('Set-Cookie'))