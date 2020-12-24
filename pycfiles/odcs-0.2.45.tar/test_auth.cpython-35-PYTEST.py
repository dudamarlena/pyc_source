# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/tests/test_auth.py
# Compiled at: 2017-09-21 02:38:08
# Size of source mod 2**32: 10607 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, flask, unittest
from mock import patch, Mock
import odcs.server.auth
from odcs.server.auth import load_krb_user_from_request
from odcs.server.auth import load_openidc_user
from odcs.server.auth import query_ldap_groups
from odcs.server.auth import init_auth
from odcs.server.errors import Unauthorized
from odcs.server import app, db
from odcs.server.models import User
from utils import ModelsBaseTest

class TestLoadKrbUserFromRequest(ModelsBaseTest):

    def setUp(self):
        super(TestLoadKrbUserFromRequest, self).setUp()
        self.user = User(username='tester1')
        db.session.add(self.user)
        db.session.commit()

    @patch('odcs.server.auth.query_ldap_groups')
    def test_create_new_user(self, query_ldap_groups):
        query_ldap_groups.return_value = ['devel', 'admins']
        environ_base = {'REMOTE_USER': 'newuser@EXAMPLE.COM'}
        with app.test_request_context(environ_base=environ_base):
            load_krb_user_from_request(flask.request)
            expected_user = db.session.query(User).filter(User.username == 'newuser')[0]
            self.assertEqual(expected_user.id, flask.g.user.id)
            self.assertEqual(expected_user.username, flask.g.user.username)
            self.assertEqual(2, len(flask.g.groups))
            self.assertEqual(['admins', 'devel'], sorted(flask.g.groups))

    @patch('odcs.server.auth.query_ldap_groups')
    def test_return_existing_user(self, query_ldap_groups):
        query_ldap_groups.return_value = ['devel', 'admins']
        original_users_count = db.session.query(User.id).count()
        environ_base = {'REMOTE_USER': '{0}@EXAMPLE.COM'.format(self.user.username)}
        with app.test_request_context(environ_base=environ_base):
            load_krb_user_from_request(flask.request)
            self.assertEqual(original_users_count, db.session.query(User.id).count())
            self.assertEqual(self.user.id, flask.g.user.id)
            self.assertEqual(self.user.username, flask.g.user.username)
            self.assertEqual(['admins', 'devel'], sorted(flask.g.groups))

    def test_401_if_remote_user_not_present(self):
        with app.test_request_context():
            with self.assertRaises(Unauthorized) as (ctx):
                load_krb_user_from_request(flask.request)
            self.assertTrue('REMOTE_USER is not present in request.' in ctx.exception.args)


class TestLoadOpenIDCUserFromRequest(ModelsBaseTest):

    def setUp(self):
        super(TestLoadOpenIDCUserFromRequest, self).setUp()
        self.user = User(username='tester1')
        db.session.add(self.user)
        db.session.commit()

    @patch('odcs.server.auth.requests.get')
    def test_create_new_user(self, get):
        get.return_value.status_code = 200
        get.return_value.json.return_value = {'groups': ['tester', 'admin'], 
         'name': 'new_user'}
        environ_base = {'REMOTE_USER': 'new_user', 
         'OIDC_access_token': '39283', 
         'OIDC_CLAIM_iss': 'https://iddev.fedorainfracloud.org/openidc/', 
         'OIDC_CLAIM_scope': 'openid https://id.fedoraproject.org/scope/groups https://pagure.io/odcs/new-compose https://pagure.io/odcs/renew-compose https://pagure.io/odcs/delete-compose'}
        with app.test_request_context(environ_base=environ_base):
            load_openidc_user(flask.request)
            new_user = db.session.query(User).filter(User.username == 'new_user')[0]
            self.assertEqual(new_user, flask.g.user)
            self.assertEqual('new_user', flask.g.user.username)
            self.assertEqual(sorted(['admin', 'tester']), sorted(flask.g.groups))

    @patch('odcs.server.auth.requests.get')
    def test_return_existing_user(self, get):
        get.return_value.status_code = 200
        get.return_value.json.return_value = {'groups': ['testers', 'admins'], 
         'name': self.user.username}
        environ_base = {'REMOTE_USER': self.user.username, 
         'OIDC_access_token': '39283', 
         'OIDC_CLAIM_iss': 'https://iddev.fedorainfracloud.org/openidc/', 
         'OIDC_CLAIM_scope': 'openid https://id.fedoraproject.org/scope/groups https://pagure.io/odcs/new-compose https://pagure.io/odcs/renew-compose https://pagure.io/odcs/delete-compose'}
        with app.test_request_context(environ_base=environ_base):
            original_users_count = db.session.query(User.id).count()
            load_openidc_user(flask.request)
            users_count = db.session.query(User.id).count()
            self.assertEqual(original_users_count, users_count)
            self.assertEqual(self.user.id, flask.g.user.id)
            self.assertEqual(['admins', 'testers'], sorted(flask.g.groups))

    def test_401_if_remote_user_not_present(self):
        environ_base = {'OIDC_access_token': '39283', 
         'OIDC_CLAIM_iss': 'https://iddev.fedorainfracloud.org/openidc/', 
         'OIDC_CLAIM_scope': 'openid https://id.fedoraproject.org/scope/groups'}
        with app.test_request_context(environ_base=environ_base):
            self.assertRaises(Unauthorized, load_openidc_user, flask.request)

    def test_401_if_access_token_not_present(self):
        environ_base = {'REMOTE_USER': 'tester1', 
         'OIDC_CLAIM_iss': 'https://iddev.fedorainfracloud.org/openidc/', 
         'OIDC_CLAIM_scope': 'openid https://id.fedoraproject.org/scope/groups'}
        with app.test_request_context(environ_base=environ_base):
            self.assertRaises(Unauthorized, load_openidc_user, flask.request)

    def test_401_if_scope_not_present(self):
        environ_base = {'REMOTE_USER': 'tester1', 
         'OIDC_access_token': '39283', 
         'OIDC_CLAIM_iss': 'https://iddev.fedorainfracloud.org/openidc/'}
        with app.test_request_context(environ_base=environ_base):
            self.assertRaises(Unauthorized, load_openidc_user, flask.request)

    def test_401_if_required_scope_not_present_in_token_scope(self):
        environ_base = {'REMOTE_USER': 'new_user', 
         'OIDC_access_token': '39283', 
         'OIDC_CLAIM_iss': 'https://iddev.fedorainfracloud.org/openidc/', 
         'OIDC_CLAIM_scope': 'openid https://id.fedoraproject.org/scope/groups'}
        with patch.object(odcs.server.auth.conf, 'auth_openidc_required_scopes', ['new-compose']):
            with app.test_request_context(environ_base=environ_base):
                with self.assertRaises(Unauthorized) as (ctx):
                    load_openidc_user(flask.request)
                self.assertTrue('Required OIDC scope new-compose not present.' in ctx.exception.args)


class TestQueryLdapGroups(unittest.TestCase):
    __doc__ = 'Test auth.query_ldap_groups'

    @patch('odcs.server.auth.ldap.initialize')
    def test_get_groups(self, initialize):
        initialize.return_value.search_s.return_value = [
         (
          'cn=odcsdev,ou=Groups,dc=example,dc=com',
          {'gidNumber': ['5523'], 'cn': ['odcsdev']}),
         (
          'cn=freshmakerdev,ou=Groups,dc=example,dc=com',
          {'gidNumber': ['17861'], 'cn': ['freshmakerdev']}),
         (
          'cn=devel,ou=Groups,dc=example,dc=com',
          {'gidNumber': ['5781'], 'cn': ['devel']})]
        groups = query_ldap_groups('me')
        self.assertEqual(sorted(['odcsdev', 'freshmakerdev', 'devel']), sorted(groups))


class TestInitAuth(unittest.TestCase):
    __doc__ = 'Test init_auth'

    def setUp(self):
        self.login_manager = Mock()

    def test_select_kerberos_auth_backend(self):
        init_auth(self.login_manager, 'kerberos')
        self.login_manager.request_loader.assert_called_once_with(load_krb_user_from_request)

    def test_select_openidc_auth_backend(self):
        init_auth(self.login_manager, 'openidc')
        self.login_manager.request_loader.assert_called_once_with(load_openidc_user)

    def test_not_use_auth_backend(self):
        init_auth(self.login_manager, 'noauth')
        self.login_manager.request_loader.assert_not_called()

    def test_error_if_select_an_unknown_backend(self):
        self.assertRaises(ValueError, init_auth, self.login_manager, 'xxx')
        self.assertRaises(ValueError, init_auth, self.login_manager, '')
        self.assertRaises(ValueError, init_auth, self.login_manager, None)

    def test_init_auth_no_ldap_server(self):
        with patch.object(odcs.server.auth.conf, 'auth_ldap_server', ''):
            self.assertRaises(ValueError, init_auth, self.login_manager, 'kerberos')

    def test_init_auths_no_ldap_group_base(self):
        with patch.object(odcs.server.auth.conf, 'auth_ldap_group_base', ''):
            self.assertRaises(ValueError, init_auth, self.login_manager, 'kerberos')