# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_quickstart.py
# Compiled at: 2011-11-29 15:47:41
"""
Tests for the repoze.what SQL quickstart.

"""
from os import path
import sys
from unittest import TestCase
from repoze.who.interfaces import IAuthenticator
from repoze.who.plugins.basicauth import BasicAuthPlugin
from repoze.who.plugins.auth_tkt import AuthTktCookiePlugin
from repoze.who.plugins.sa import SQLAlchemyAuthenticatorPlugin, SQLAlchemyUserMDPlugin
from repoze.who.plugins.friendlyform import FriendlyFormPlugin
from repoze.what.middleware import AuthorizationMetadata
from repoze.what.plugins.quickstart import setup_sql_auth, find_plugin_translations
from repoze.who.utils import resolveDotted
from zope.interface import implements
from tests import databasesetup
from tests.fixture.model import User, Group, Permission, DBSession
from tests import MockApplication, FIXTURE_DIR

class TestSetupAuth(TestCase):
    """Tests for the setup_sql_auth() function"""

    def setUp(self):
        super(TestSetupAuth, self).setUp()
        databasesetup.setup_database()

    def tearDown(self):
        super(TestSetupAuth, self).tearDown()
        databasesetup.teardownDatabase()

    def _in_registry--- This code section failed: ---

 L.  54         0  LOAD_FAST             2  'registry_key'
                3  LOAD_FAST             1  'app'
                6  LOAD_ATTR             0  'name_registry'
                9  COMPARE_OP            6  in
               12  POP_JUMP_IF_TRUE     28  'to 28'
               15  LOAD_ASSERT              AssertionError
               18  LOAD_CONST               'Key "%s" not in registry'

 L.  55        21  LOAD_FAST             2  'registry_key'
               24  BINARY_MODULO    
               25  RAISE_VARARGS_2       2  None

 L.  56        28  LOAD_GLOBAL           2  'isinstance'
               31  LOAD_FAST             1  'app'
               34  LOAD_ATTR             0  'name_registry'
               37  LOAD_FAST             2  'registry_key'
               40  BINARY_SUBSCR    
               41  LOAD_FAST             3  'registry_type'
               44  CALL_FUNCTION_2       2  None
               47  POP_JUMP_IF_TRUE     88  'to 88'
               50  LOAD_ASSERT              AssertionError

 L.  57        53  LOAD_CONST               'Registry key "%s" is of type "%s" (not "%s")'

 L.  58        56  LOAD_FAST             2  'registry_key'
               59  LOAD_FAST             1  'app'
               62  LOAD_ATTR             0  'name_registry'
               65  LOAD_FAST             2  'registry_key'
               68  BINARY_SUBSCR    
               69  LOAD_ATTR             3  '__class__'
               72  LOAD_ATTR             4  '__name__'

 L.  59        75  LOAD_FAST             3  'registry_type'
               78  LOAD_ATTR             4  '__name__'
               81  BUILD_TUPLE_3         3 
               84  BINARY_MODULO    
               85  RAISE_VARARGS_2       2  None

Parse error at or near `BINARY_MODULO' instruction at offset 84

    def _makeApp(self, **who_args):
        app_with_auth = setup_sql_auth(MockApplication(), User, Group, Permission, DBSession, **who_args)
        return app_with_auth

    def test_no_extras(self):
        app = self._makeApp()
        self._in_registry(app, 'main_identifier', FriendlyFormPlugin)
        self._in_registry(app, 'authorization_md', AuthorizationMetadata)
        self._in_registry(app, 'sql_user_md', SQLAlchemyUserMDPlugin)
        self._in_registry(app, 'cookie', AuthTktCookiePlugin)
        self._in_registry(app, 'sqlauth', SQLAlchemyAuthenticatorPlugin)
        self._in_registry(app, 'form', FriendlyFormPlugin)

    def test_form_doesnt_identify(self):
        app = self._makeApp(form_identifies=False)
        assert 'main_identifier' not in app.name_registry

    def test_additional_identifiers(self):
        identifiers = [
         (
          'http_auth', BasicAuthPlugin('1+1=2'))]
        app = self._makeApp(identifiers=identifiers)
        self._in_registry(app, 'main_identifier', FriendlyFormPlugin)
        self._in_registry(app, 'http_auth', BasicAuthPlugin)

    def test_non_default_form_plugin(self):
        app = self._makeApp(form_plugin=BasicAuthPlugin('1+1=2'))
        self._in_registry(app, 'main_identifier', BasicAuthPlugin)

    def test_additional_authenticators(self):
        authenticators = [
         (
          'mock_auth', MockAuthenticator())]
        app = self._makeApp(authenticators=authenticators)
        self._in_registry(app, 'mock_auth', MockAuthenticator)
        self._in_registry(app, 'sqlauth', SQLAlchemyAuthenticatorPlugin)

    def test_no_default_authenticator(self):
        authenticators = [
         (
          'mock_auth', MockAuthenticator())]
        app = self._makeApp(authenticators=authenticators, use_default_authenticator=False)
        self._in_registry(app, 'mock_auth', MockAuthenticator)
        assert 'sqlauth' not in app.name_registry

    def test_custom_login_urls(self):
        login_url = '/myapp/login'
        login_handler = '/myapp/login_handler'
        post_login_url = '/myapp/welcome_back'
        logout_handler = '/myapp/logout'
        post_logout_url = '/myapp/see_you_later'
        login_counter_name = '__failed_logins'
        app = self._makeApp(login_url=login_url, login_handler=login_handler, logout_handler=logout_handler, post_login_url=post_login_url, post_logout_url=post_logout_url, login_counter_name=login_counter_name)
        form = app.name_registry['form']
        self.assertEqual(form.login_form_url, login_url)
        self.assertEqual(form.login_handler_path, login_handler)
        self.assertEqual(form.post_login_url, post_login_url)
        self.assertEqual(form.logout_handler_path, logout_handler)
        self.assertEqual(form.post_logout_url, post_logout_url)
        self.assertEqual(form.login_counter_name, login_counter_name)

    def test_stdout_logging(self):
        """Test using a stdout for logging"""
        log_level = 'debug'
        log_file = 'stdout'
        app = self._makeApp(log_level=log_level, log_file=log_file)
        logger = app.logger
        self.assertEqual(logger.level, 10)
        handler = app.logger.handlers[0]
        self.assertEqual(handler.stream, sys.stdout)

    def test_stderr_logging(self):
        """Test using a stderr for logging"""
        log_level = 'warning'
        log_file = 'stderr'
        app = self._makeApp(log_level=log_level, log_file=log_file)
        logger = app.logger
        self.assertEqual(logger.level, 30)
        handler = app.logger.handlers[0]
        self.assertEqual(handler.stream, sys.stderr)

    def test_file_logging(self):
        """Test using a log file for logging"""
        log_level = 'info'
        log_file = path.join(FIXTURE_DIR, 'file.log')
        app = self._makeApp(log_level=log_level, log_file=log_file)
        logger = app.logger
        self.assertEqual(logger.level, 20)
        handler = app.logger.handlers[0]
        self.assertEqual(handler.stream.name, log_file)

    def test_no_groups_or_permissions(self):
        """Groups and permissions must be optional"""
        app = setup_sql_auth(MockApplication(), User, None, None, DBSession)
        self._in_registry(app, 'authorization_md', AuthorizationMetadata)
        environ = {}
        identity = {'repoze.who.userid': 'rms'}
        md = app.name_registry['authorization_md']
        md.add_metadata(environ, identity)
        expected_credentials = {'repoze.what.userid': 'rms', 
           'groups': tuple(), 
           'permissions': tuple()}
        self.assertEqual(expected_credentials, environ['repoze.what.credentials'])
        return

    def test_timeout(self):
        """AuthTktCookiePlugin's timeout and reissue_time must be supported"""
        app = setup_sql_auth(MockApplication(), User, None, None, DBSession, cookie_timeout=2, cookie_reissue_time=1)
        self._in_registry(app, 'cookie', AuthTktCookiePlugin)
        identifier = app.name_registry['cookie']
        self.assertEqual(identifier.timeout, 2)
        self.assertEqual(identifier.reissue_time, 1)
        return

    def test_charset(self):
        """It should be possible to override the default character encoding."""
        charset = 'us-ascii'
        app = self._makeApp(charset=charset)
        form = app.name_registry['form']
        self.assertEqual(form.charset, charset)


class TestPluginTranslationsFinder(TestCase):

    def test_it(self):
        dummy_fn = 'tests.fixture.model:dummy_validate_password'
        translations = {'validate_password': 'pass_checker', 
           'user_name': 'member_name', 
           'users': 'members', 
           'group_name': 'team_name', 
           'groups': 'teams', 
           'permission_name': 'perm_name', 
           'permissions': 'perms', 
           'dummy_validate_password': dummy_fn}
        plugin_translations = find_plugin_translations(translations)
        group_translations = {'item_name': translations['user_name'], 
           'items': translations['users'], 
           'section_name': translations['group_name'], 
           'sections': translations['groups']}
        self.assertEqual(group_translations, plugin_translations['group_adapter'])
        perm_translations = {'item_name': translations['group_name'], 
           'items': translations['groups'], 
           'section_name': translations['permission_name'], 
           'sections': translations['permissions']}
        self.assertEqual(perm_translations, plugin_translations['permission_adapter'])
        auth_translations = {'user_name': translations['user_name'], 
           'validate_password': translations['validate_password'], 
           'dummy_validate_password': resolveDotted(dummy_fn)}
        self.assertEqual(auth_translations, plugin_translations['authenticator'])
        md_translations = {'user_name': translations['user_name']}
        self.assertEqual(md_translations, plugin_translations['mdprovider'])


class MockAuthenticator(object):
    """A repoze.who authenticator that does nothing."""
    implements(IAuthenticator)

    def authenticate(self, environ, identity):
        pass