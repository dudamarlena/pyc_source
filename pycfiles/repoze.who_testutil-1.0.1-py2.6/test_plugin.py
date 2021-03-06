# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_plugin.py
# Compiled at: 2010-02-22 17:28:42
"""Test suite for the test utilities for repoze.who-powered applications."""
from os import path
from unittest import TestCase
from zope.interface.verify import verifyClass
from paste.httpexceptions import HTTPUnauthorized
from paste.deploy import appconfig
from repoze.who.middleware import PluggableAuthenticationMiddleware
from repoze.who.interfaces import IIdentifier, IAuthenticator, IChallenger, IMetadataProvider
from repoze.who.plugins.auth_tkt import AuthTktCookiePlugin
from repoze.who.plugins.form import RedirectingFormPlugin
from repoze.who.plugins.testutil import AuthenticationForgerPlugin, AuthenticationForgerMiddleware, make_middleware, make_middleware_with_config
HERE = path.abspath(path.dirname(__file__))
FIXTURE = path.join(HERE, 'fixture')

class TestAuthenticationForgerPlugin(TestCase):
    """Tests for ``AuthenticationForgerPlugin``"""

    def test_implements(self):
        verifyClass(IIdentifier, AuthenticationForgerPlugin)
        verifyClass(IAuthenticator, AuthenticationForgerPlugin)
        verifyClass(IChallenger, AuthenticationForgerPlugin)

    def test_constructor_with_arguments(self):
        p = AuthenticationForgerPlugin()
        self.assertEqual(p.fake_user_key, 'REMOTE_USER')
        self.assertEqual(p.remote_user_key, 'repoze.who.testutil.userid')

    def test_constructor_without_arguments(self):
        p = AuthenticationForgerPlugin('anotherkey', 'yetanotherkey')
        self.assertEqual(p.fake_user_key, 'anotherkey')
        self.assertEqual(p.remote_user_key, 'yetanotherkey')

    def test_identifier_with_forged_userid(self):
        environ = {'REMOTE_USER': 'gustavo'}
        p = AuthenticationForgerPlugin()
        identity = p.identify(environ)
        self.assertEqual(identity, {'fake-userid': 'gustavo'})

    def test_identifier_without_forged_userid(self):
        environ = {}
        p = AuthenticationForgerPlugin()
        identity = p.identify(environ)
        self.assertEqual(identity, None)
        return

    def test_rememberer(self):
        p = AuthenticationForgerPlugin()
        self.assertEqual(p.remember({}, {}), None)
        return

    def test_forgeter(self):
        p = AuthenticationForgerPlugin()
        self.assertEqual(p.forget({}, {}), None)
        return

    def test_authenticator_with_forged_userid(self):
        environ = {}
        identity = {'fake-userid': 'gustavo'}
        p = AuthenticationForgerPlugin()
        userid = p.authenticate(environ, identity)
        self.assertEqual(1, len(environ))
        self.assertEqual(0, len(identity))
        assert environ['repoze.who.testutil.userid'] == userid == 'gustavo'

    def test_authenticator_without_forged_userid(self):
        environ = {}
        identity = {}
        p = AuthenticationForgerPlugin()
        userid = p.authenticate(environ, identity)
        self.assertEqual(userid, None)
        self.assertEquals(identity, environ, {})
        return

    def test_challenger(self):
        p = AuthenticationForgerPlugin()
        app = p.challenge(None, '', [], [])
        assert isinstance(app, HTTPUnauthorized)
        self.assertEqual(app.code, 401)
        self.assertEqual(app.title, 'HTTP Unauthorized')
        self.assertEqual(app.headers, tuple())
        return

    def test_challenger_doesnt_ignore_original_headers(self):
        p = AuthenticationForgerPlugin()
        status = '401 You cannot be here'
        app_headers = [('X-App-Header', 'foo')]
        forget_headers = [('X-Forget-Header', 'baz')]
        final_headers = app_headers + forget_headers
        app = p.challenge(None, status, app_headers, forget_headers)
        assert isinstance(app, HTTPUnauthorized)
        self.assertEqual(app.code, 401)
        self.assertEqual(app.title, 'You cannot be here')
        self.assertEqual(app.headers, final_headers)
        return

    def test_challenger_with_unicode_message_and_custom_code(self):
        p = AuthenticationForgerPlugin()
        status = '403 Tú no puedes estar aquí'
        app_headers = [('X-App-Header', 'foo')]
        forget_headers = [('X-Forget-Header', 'baz')]
        final_headers = app_headers + forget_headers
        app = p.challenge(None, status, app_headers, forget_headers)
        assert isinstance(app, HTTPUnauthorized)
        self.assertEqual(app.code, 403)
        self.assertEqual(app.title, 'Tú no puedes estar aquí')
        self.assertEqual(app.headers, final_headers)
        return

    def test_challenger_and_content_length(self):
        """Content-Length must be removed from the response."""
        p = AuthenticationForgerPlugin()
        status = '401 You cannot be here'
        app_headers = [('X-App-Header', 'foo'), ('Content-Length', '10')]
        forget_headers = [('X-Forget-Header', 'baz')]
        app = p.challenge(None, status, app_headers, forget_headers)
        self.assertEqual(len(app.headers), 2)
        self.assert_(('X-App-Header', 'foo') in app.headers)
        self.assert_(('X-Forget-Header', 'baz') in app.headers)
        return


class TestAuthenticationForgerMiddleware(TestCase):
    """Tests for ``AuthenticationForgerMiddleware``"""

    def test_inheritance(self):
        assert issubclass(AuthenticationForgerMiddleware, PluggableAuthenticationMiddleware)

    def test_it(self):
        identifiers = [
         (
          'cookie', AuthTktCookiePlugin('something'))]
        authenticators = challengers = mdproviders = []
        mw = AuthenticationForgerMiddleware(None, identifiers, authenticators, challengers, mdproviders, None, None)
        assert isinstance(mw, AuthenticationForgerMiddleware)
        final_identifiers = mw.registry[IIdentifier]
        self.assertEqual(2, len(final_identifiers))
        assert isinstance(final_identifiers[0], AuthenticationForgerPlugin)
        assert isinstance(final_identifiers[1], AuthTktCookiePlugin)
        auth_forger = final_identifiers[0]
        self.assertEqual([auth_forger], mw.registry[IAuthenticator])
        self.assertEqual([auth_forger], mw.registry[IChallenger])
        assert IMetadataProvider not in mw.registry
        self.assertEqual(mw.remote_user_key, 'repoze.who.testutil.userid')
        self.assertEqual(mw.actual_remote_user_key, 'REMOTE_USER')
        self.assertEqual(auth_forger.fake_user_key, 'REMOTE_USER')
        self.assertEqual(auth_forger.remote_user_key, 'repoze.who.testutil.userid')
        return

    def test_it_with_fake_user_key(self):
        identifiers = [('cookie', AuthTktCookiePlugin('something'))]
        authenticators = challengers = mdproviders = []
        mw = AuthenticationForgerMiddleware(None, identifiers, authenticators, challengers, mdproviders, None, None, remote_user_key='userid')
        assert isinstance(mw, AuthenticationForgerMiddleware)
        final_identifiers = mw.registry[IIdentifier]
        auth_forger = final_identifiers[0]
        self.assertEqual(mw.remote_user_key, 'repoze.who.testutil.userid')
        self.assertEqual(mw.actual_remote_user_key, 'userid')
        self.assertEqual(auth_forger.fake_user_key, 'userid')
        self.assertEqual(auth_forger.remote_user_key, 'repoze.who.testutil.userid')
        return


class TestMiddlewareMaker(TestCase):
    """Tests for :func:`make_middleware`"""

    def test_skipping_authentication(self):
        identifiers = [
         (
          'cookie', AuthTktCookiePlugin('something'))]
        authenticators = challengers = mdproviders = []
        mw = make_middleware(True, None, identifiers, authenticators, challengers, mdproviders, None, None)
        assert isinstance(mw, AuthenticationForgerMiddleware)
        final_identifiers = mw.registry[IIdentifier]
        self.assertEqual(2, len(final_identifiers))
        assert isinstance(final_identifiers[0], AuthenticationForgerPlugin)
        assert isinstance(final_identifiers[1], AuthTktCookiePlugin)
        auth_forger = final_identifiers[0]
        self.assertEqual([auth_forger], mw.registry[IAuthenticator])
        self.assertEqual([auth_forger], mw.registry[IChallenger])
        assert IMetadataProvider not in mw.registry
        self.assertEqual(mw.remote_user_key, 'repoze.who.testutil.userid')
        self.assertEqual(mw.actual_remote_user_key, 'REMOTE_USER')
        self.assertEqual(auth_forger.fake_user_key, 'REMOTE_USER')
        self.assertEqual(auth_forger.remote_user_key, 'repoze.who.testutil.userid')
        return

    def test_without_skipping_authentication(self):
        identifiers = [('cookie', AuthTktCookiePlugin('something'))]
        authenticators = challengers = mdproviders = []
        mw = make_middleware(False, None, identifiers, authenticators, challengers, mdproviders, None, None)
        assert isinstance(mw, PluggableAuthenticationMiddleware)
        final_identifiers = mw.registry[IIdentifier]
        self.assertEqual(1, len(final_identifiers))
        assert isinstance(final_identifiers[0], AuthTktCookiePlugin)
        assert IAuthenticator not in mw.registry
        assert IChallenger not in mw.registry
        assert IMetadataProvider not in mw.registry
        self.assertEqual(mw.remote_user_key, 'REMOTE_USER')
        return

    def test_skip_authentication_is_not_boolean(self):
        identifiers = [('cookie', AuthTktCookiePlugin('something'))]
        authenticators = challengers = mdproviders = []
        mw = make_middleware('True', None, identifiers, authenticators, challengers, mdproviders, None, None)
        self.assertEqual(mw.__class__, AuthenticationForgerMiddleware)
        mw = make_middleware('False', None, identifiers, authenticators, challengers, mdproviders, None, None)
        self.assertEqual(mw.__class__, PluggableAuthenticationMiddleware)
        mw = make_middleware(None, None, identifiers, authenticators, challengers, mdproviders, None, None)
        self.assertEqual(mw.__class__, PluggableAuthenticationMiddleware)
        return


class TestMiddlewareMakerFromConfig(TestCase):
    """Tests for make_middleware_with_config"""

    def _parse_config(self, config_name):
        return appconfig('config:%s' % config_name, relative_to=FIXTURE)

    def test_with_unspecified_authentication(self):
        """
        The middleware must not be replaced if ``skip_authentication`` is not
        defined.
        
        """
        config = self._parse_config('config.ini')
        local_conf = config.local_conf
        mw = make_middleware_with_config(None, config.global_conf, local_conf['who.config_file'], local_conf['who.log_file'], local_conf['who.log_level'])
        assert isinstance(mw, PluggableAuthenticationMiddleware)
        return

    def test_with_authentication(self):
        """
        The middleware must not be replaced if ``skip_authentication`` is False
        
        """
        config = self._parse_config('config.ini')
        local_conf = config.local_conf
        mw = make_middleware_with_config(None, config.global_conf, local_conf['who.config_file'], local_conf['who.log_file'], local_conf['who.log_level'], skip_authentication=False)
        assert isinstance(mw, PluggableAuthenticationMiddleware)
        return

    def test_without_authentication(self):
        """
        The middleware must be replaced if ``skip_authentication`` is True.
        
        """
        config = self._parse_config('config.ini')
        local_conf = config.local_conf
        mw = make_middleware_with_config(None, config.global_conf, local_conf['who.config_file'], local_conf['who.log_file'], local_conf['who.log_level'], skip_authentication=True)
        assert isinstance(mw, AuthenticationForgerMiddleware)
        final_identifiers = mw.registry[IIdentifier]
        self.assertEqual(3, len(final_identifiers))
        assert isinstance(final_identifiers[0], AuthenticationForgerPlugin)
        assert isinstance(final_identifiers[1], RedirectingFormPlugin)
        assert isinstance(final_identifiers[2], AuthTktCookiePlugin)
        auth_forger = final_identifiers[0]
        self.assertEqual([auth_forger], mw.registry[IAuthenticator])
        self.assertEqual([auth_forger], mw.registry[IChallenger])
        assert IMetadataProvider not in mw.registry
        self.assertEqual(mw.remote_user_key, 'repoze.who.testutil.userid')
        self.assertEqual(mw.actual_remote_user_key, 'REMOTE_USER')
        self.assertEqual(auth_forger.fake_user_key, 'REMOTE_USER')
        self.assertEqual(auth_forger.remote_user_key, 'repoze.who.testutil.userid')
        return

    def test_skip_authentication_is_not_boolean(self):
        config = self._parse_config('config.ini')
        local_conf = config.local_conf
        mw = make_middleware_with_config(None, config.global_conf, local_conf['who.config_file'], local_conf['who.log_file'], local_conf['who.log_level'], skip_authentication='True')
        assert isinstance(mw, AuthenticationForgerMiddleware)
        mw = make_middleware_with_config(None, config.global_conf, local_conf['who.config_file'], local_conf['who.log_file'], local_conf['who.log_level'], skip_authentication='False')
        assert isinstance(mw, PluggableAuthenticationMiddleware)
        return


class DummyApp:

    def __init__(self, status, headers):
        pass

    def __call__(self, environ, start_response):
        pass


def dummy_app_factory(global_config, **local_conf):
    return DummyApp


class DummyAuthenticator(object):

    def authenticate(self, environ, identity):
        return