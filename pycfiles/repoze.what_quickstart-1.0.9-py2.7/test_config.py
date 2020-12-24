# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_config.py
# Compiled at: 2011-11-29 15:47:41
"""
Tests for the configuration files supported by the repoze.what SQL quickstart
plugin.

"""
import os
from unittest import TestCase
from repoze.who.plugins.auth_tkt import AuthTktCookiePlugin
from repoze.who.plugins.sa import SQLAlchemyAuthenticatorPlugin, SQLAlchemyUserMDPlugin
from repoze.who.plugins.friendlyform import FriendlyFormPlugin
from repoze.who.plugins.testutil import AuthenticationForgerMiddleware
from repoze.what.middleware import AuthorizationMetadata
from repoze.who.utils import resolveDotted
from repoze.what.plugins.quickstart import add_auth_from_config, MissingOptionError, BadOptionError
from tests import databasesetup
from tests.fixture.model import User, Group, Permission, DBSession
from tests.fixture.misc_config import form_plugin
from tests import MockApplication, FIXTURE_DIR
DEFAULT_OPTIONS = {'form_plugin': None, 
   'form_identifies': True, 
   'cookie_secret': 'secret', 
   'cookie_name': 'authtkt', 
   'cookie_timeout': None, 
   'cookie_reissue_time': None, 
   'login_url': '/login', 
   'login_handler': '/login_handler', 
   'post_login_url': None, 
   'logout_handler': '/logout_handler', 
   'post_logout_url': None, 
   'login_counter_name': '__logins', 
   'charset': 'iso-8859-1'}
DEFAULT_TRANSLATIONS = {'users': 'users', 
   'user_name': 'user_name', 
   'groups': 'groups', 
   'group_name': 'group_name', 
   'permissions': 'permissions', 
   'permission_name': 'permission_name', 
   'validate_password': 'validate_password', 
   'dummy_validate_password': None}

class TestConfig(TestCase):
    """Tests for the setup_sql_auth() function"""

    def setUp(self):
        super(TestConfig, self).setUp()
        databasesetup.setup_database()

    def tearDown(self):
        super(TestConfig, self).tearDown()
        databasesetup.teardownDatabase()

    def _in_registry--- This code section failed: ---

 L.  86         0  LOAD_FAST             2  'registry_key'
                3  LOAD_FAST             1  'app'
                6  LOAD_ATTR             0  'name_registry'
                9  COMPARE_OP            6  in
               12  POP_JUMP_IF_TRUE     28  'to 28'
               15  LOAD_ASSERT              AssertionError
               18  LOAD_CONST               'Key "%s" not in registry'

 L.  87        21  LOAD_FAST             2  'registry_key'
               24  BINARY_MODULO    
               25  RAISE_VARARGS_2       2  None

 L.  88        28  LOAD_GLOBAL           2  'isinstance'
               31  LOAD_FAST             1  'app'
               34  LOAD_ATTR             0  'name_registry'
               37  LOAD_FAST             2  'registry_key'
               40  BINARY_SUBSCR    
               41  LOAD_FAST             3  'registry_type'
               44  CALL_FUNCTION_2       2  None
               47  POP_JUMP_IF_TRUE     88  'to 88'
               50  LOAD_ASSERT              AssertionError

 L.  89        53  LOAD_CONST               'Registry key "%s" is of type "%s" (not "%s")'

 L.  90        56  LOAD_FAST             2  'registry_key'
               59  LOAD_FAST             1  'app'
               62  LOAD_ATTR             0  'name_registry'
               65  LOAD_FAST             2  'registry_key'
               68  BINARY_SUBSCR    
               69  LOAD_ATTR             3  '__class__'
               72  LOAD_ATTR             4  '__name__'

 L.  91        75  LOAD_FAST             3  'registry_type'
               78  LOAD_ATTR             4  '__name__'
               81  BUILD_TUPLE_3         3 
               84  BINARY_MODULO    
               85  RAISE_VARARGS_2       2  None

Parse error at or near `BINARY_MODULO' instruction at offset 84

    def _check_auth(self, app, options):
        """
        Check that the ``app`` is secured with Repoze auth using the expected
        ``options``.
        
        """
        main_identifier = app.name_registry.get('main_identifier')
        challenger = app.name_registry['form']
        if not (options['form_identifies'] and main_identifier == challenger):
            raise AssertionError, 'The form identifies too'
        if options.get('form_plugin'):
            self.assertEqual(form_plugin, main_identifier)
        else:
            self._in_registry(app, 'form', FriendlyFormPlugin)
            self.assertEqual(challenger.login_form_url, options['login_url'])
            self.assertEqual(challenger.login_handler_path, options['login_handler'])
            self.assertEqual(challenger.post_login_url, options['post_login_url'])
            self.assertEqual(challenger.logout_handler_path, options['logout_handler'])
            self.assertEqual(challenger.post_logout_url, options['post_logout_url'])
            self.assertEqual(challenger.login_counter_name, options['login_counter_name'])
            self.assertEqual(challenger.charset, options['charset'])
        self._in_registry(app, 'sqlauth', SQLAlchemyAuthenticatorPlugin)
        authenticator = app.name_registry['sqlauth']
        self.assertEqual(authenticator.user_class, options['user_class'])
        self.assertEqual(authenticator.translations['user_name'], options['translations']['user_name'])
        self.assertEqual(authenticator.translations['validate_password'], options['translations']['validate_password'])
        dummy_fn = options['translations']['dummy_validate_password']
        if dummy_fn is not None:
            dummy_fn = resolveDotted(dummy_fn)
        self.assertEqual(authenticator.translations['dummy_validate_password'], dummy_fn)
        self.assertEqual(authenticator.dbsession, options['dbsession'])
        self._in_registry(app, 'sql_user_md', SQLAlchemyUserMDPlugin)
        mdprovider = app.name_registry['sql_user_md']
        self.assertEqual(mdprovider.user_class, options['user_class'])
        self.assertEqual(mdprovider.translations['user_name'], options['translations']['user_name'])
        self.assertEqual(mdprovider.dbsession, options['dbsession'])
        self._in_registry(app, 'cookie', AuthTktCookiePlugin)
        cookie = app.name_registry['cookie']
        self.assertEqual(cookie.cookie_name, options['cookie_name'])
        self.assertEqual(cookie.secret, options['cookie_secret'])
        self.assertEqual(cookie.timeout, options['cookie_timeout'])
        self.assertEqual(cookie.reissue_time, options['cookie_reissue_time'])
        self._in_registry(app, 'authorization_md', AuthorizationMetadata)
        authz_md = app.name_registry['authorization_md']
        group_adapters = authz_md.group_adapters
        permission_adapters = authz_md.permission_adapters
        if options['group_class'] and options['permission_class']:
            sql_groups = group_adapters['sql_auth']
            sql_permissions = permission_adapters['sql_auth']
            self.assertEquals(sql_groups.children_class, options['user_class'])
            self.assertEquals(sql_groups.parent_class, sql_permissions.children_class, options['group_class'])
            self.assertEquals(sql_permissions.parent_class, options['permission_class'])
            self.assertEquals(options['dbsession'], sql_groups.dbsession, sql_permissions.dbsession)
            self.assertEqual(sql_groups.translations['items'], options['translations']['users'])
            self.assertEqual(sql_groups.translations['item_name'], options['translations']['user_name'])
            self.assertEquals(sql_groups.translations['sections'], sql_permissions.translations['items'], options['translations']['groups'])
            self.assertEquals(sql_groups.translations['section_name'], sql_permissions.translations['item_name'], options['translations']['group_name'])
            self.assertEqual(sql_permissions.translations['sections'], options['translations']['permissions'])
            self.assertEqual(sql_permissions.translations['section_name'], options['translations']['permission_name'])
        else:
            self.assertEquals(permission_adapters, group_adapters, None)
        return

    def test_full_config(self):
        """A config file with all the known options."""
        app = make_app('full-config')
        translations = {'validate_password': 'check_it', 
           'users': 'members', 
           'user_name': 'member_name', 
           'groups': 'team', 
           'group_name': 'group_name', 
           'permissions': 'perms', 
           'permission_name': 'perm_name', 
           'dummy_validate_password': 'tests.fixture.model:dummy_validate_password'}
        expected_options = make_options(user_class=User, group_class=Group, permission_class=Permission, dbsession=DBSession, form_plugin=form_plugin, form_identifies=True, cookie_name='authntkt', cookie_secret='you cannot see this', login_url='/log-me-in', login_handler='/handle-login', post_login_url='/do-something-after-login', logout_handle='/log-me-out', post_logout_url='/do-something-after-logout', login_counter_name='login_attempts', translations=translations, cookie_timeout=3600, cookie_reissue_time=1800)
        self._check_auth(app, expected_options)

    def test_minimal_config(self):
        """A config file with only the minimum options."""
        app = make_app('minimal-config')
        expected_options = make_options(user_class=User, group_class=Group, permission_class=Permission, dbsession=DBSession)
        self._check_auth(app, expected_options)

    def test_charset_config(self):
        """Custom charsets may be specified in config files."""
        app = make_app('custom-charset')
        expected_options = make_options(user_class=User, group_class=Group, permission_class=Permission, dbsession=DBSession, charset='us-ascii')
        self._check_auth(app, expected_options)

    def test_logging_config(self):
        """A config file with logging options."""
        app = make_app('logging-config')
        logger = app.logger
        self.assertEqual(logger.level, 10)
        handler = app.logger.handlers[0]
        self.assertEqual(handler.stream.name, os.path.join(FIXTURE_DIR, 'file.log'))

    def test_skip_authentication_config(self):
        """A config file with skip authentication options."""
        no_authn_app = make_app('skip-authentication-enabled-config')
        self.assertTrue(isinstance(no_authn_app, AuthenticationForgerMiddleware))
        authn_app = make_app('skip-authentication-disabled-config')
        self.assertFalse(isinstance(authn_app, AuthenticationForgerMiddleware))

    def test_missing_options(self):
        """Configuration files with missing mandatory options."""
        self.assertRaises(MissingOptionError, make_app, 'missing-dbsession-config')
        self.assertRaises(MissingOptionError, make_app, 'missing-user-config')
        self.assertRaises(MissingOptionError, make_app, 'missing-group-config')
        self.assertRaises(MissingOptionError, make_app, 'missing-permission-config')

    def test_bad_form_identifies(self):
        """
        Check that the value of ``form_identifies`` is a valid boolean.
        
        """
        self.assertRaises(BadOptionError, make_app, 'bad-boolean-config')

    def test_bad_integers(self):
        """
        Check that the value for ``cookie_timeout`` and ``cookie_reissue_time``
        are valid integers.
        
        """
        self.assertRaises(BadOptionError, make_app, 'bad-cookie-timeout-config')
        self.assertRaises(BadOptionError, make_app, 'bad-cookie-reissue-config')

    def test_non_existing_python_objects(self):
        """
        Check that the Python objects to be resolved exist.
        
        """
        self.assertRaises(BadOptionError, make_app, 'no-dbsession-config')
        self.assertRaises(BadOptionError, make_app, 'no-user-config')
        self.assertRaises(BadOptionError, make_app, 'no-group-config')
        self.assertRaises(BadOptionError, make_app, 'no-permission-config')
        self.assertRaises(BadOptionError, make_app, 'no-form-config')

    def test_invalid_python_objects(self):
        """
        Invalid Python objects that can't be resolved should cause the right
        exception to be raised.
        
        """
        self.assertRaises(BadOptionError, make_app, 'bad-dbsession-config')
        self.assertRaises(BadOptionError, make_app, 'bad-user-config')
        self.assertRaises(BadOptionError, make_app, 'bad-group-config')
        self.assertRaises(BadOptionError, make_app, 'bad-permission-config')
        self.assertRaises(BadOptionError, make_app, 'bad-form-config')


def make_app(config_file):
    """
    Make a WSGI application and wrap it around the auth middleware described
    in ``config_file``.
    
    """
    config_file = os.path.join(FIXTURE_DIR, config_file + '.ini')
    app = add_auth_from_config(MockApplication(), {}, config_file)
    return app


def make_options(translations={}, **options):
    """
    Make an options dictionary for the setup_sql_auth() function.
    
    The options and translations missing in ``translations`` and ``options``
    will be taken from the relevant constants.
    
    """
    final_options = DEFAULT_OPTIONS.copy()
    final_translations = DEFAULT_TRANSLATIONS.copy()
    final_options.update(options)
    final_translations.update(translations)
    final_options['translations'] = final_translations
    return final_options