# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_openid.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 16210 bytes
import pkg_resources, pytest, six, six.moves.urllib.parse as urlparse
try:
    import mock
except ImportError:
    import unittest.mock as mock

openid_consumer = pytest.importorskip('openid.consumer.consumer')
from mediagoblin import mg_globals
from mediagoblin.db.base import Session
from mediagoblin.db.models import User, LocalUser
from mediagoblin.plugins.openid.models import OpenIDUserURL
from mediagoblin.tests.tools import get_app, fixture_add_user
from mediagoblin.tools import template

@pytest.fixture()
def openid_plugin_app(request):
    return get_app(request, mgoblin_config=pkg_resources.resource_filename('mediagoblin.tests.auth_configs', 'openid_appconfig.ini'))


class TestOpenIDPlugin(object):

    def _setup(self, openid_plugin_app, value=True, edit=False, delete=False):
        if value:
            response = openid_consumer.SuccessResponse(mock.Mock(), mock.Mock())
            if edit or delete:
                response.identity_url = 'http://add.myopenid.com'
            else:
                response.identity_url = 'http://real.myopenid.com'
            self._finish_verification = mock.Mock(return_value=response)
        else:
            self._finish_verification = mock.Mock(return_value=False)

        @mock.patch('mediagoblin.plugins.openid.views._response_email', mock.Mock(return_value=None))
        @mock.patch('mediagoblin.plugins.openid.views._response_nickname', mock.Mock(return_value=None))
        @mock.patch('mediagoblin.plugins.openid.views._finish_verification', self._finish_verification)
        def _setup_start(self, openid_plugin_app, edit, delete):
            if edit:
                self._start_verification = mock.Mock(return_value=openid_plugin_app.post('/edit/openid/finish/'))
            else:
                if delete:
                    self._start_verification = mock.Mock(return_value=openid_plugin_app.post('/edit/openid/delete/finish/'))
                else:
                    self._start_verification = mock.Mock(return_value=openid_plugin_app.post('/auth/openid/login/finish/'))

        _setup_start(self, openid_plugin_app, edit, delete)

    def test_bad_login(self, openid_plugin_app):
        """ Test that attempts to login with invalid paramaters"""
        res = openid_plugin_app.get('/auth/register/').follow()
        assert urlparse.urlsplit(res.location)[2] == '/auth/openid/login/'
        res = openid_plugin_app.get('/auth/login/')
        res.follow()
        assert urlparse.urlsplit(res.location)[2] == '/auth/openid/login/'
        res = openid_plugin_app.get('/auth/openid/register/')
        res.follow()
        assert urlparse.urlsplit(res.location)[2] == '/auth/openid/login/'
        res = openid_plugin_app.get('/auth/openid/login/finish/')
        res.follow()
        assert urlparse.urlsplit(res.location)[2] == '/auth/openid/login/'
        res = openid_plugin_app.get('/auth/openid/login/')
        assert 'mediagoblin/plugins/openid/login.html' in template.TEMPLATE_TEST_CONTEXT
        template.clear_test_template_context()
        openid_plugin_app.post('/auth/openid/login/', {})
        context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/plugins/openid/login.html']
        form = context['login_form']
        assert form.openid.errors == ['This field is required.']
        template.clear_test_template_context()
        openid_plugin_app.post('/auth/openid/login/', {'openid': 'not_a_url.com'})
        context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/plugins/openid/login.html']
        form = context['login_form']
        assert form.openid.errors == ['Please enter a valid url.']
        assert User.query.count() == 0
        template.clear_test_template_context()
        openid_plugin_app.post('/auth/openid/login/', {'openid': 'http://phoney.myopenid.com/'})
        context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/plugins/openid/login.html']
        form = context['login_form']
        assert form.openid.errors == ['Sorry, the OpenID server could not be found']

    def test_login(self, openid_plugin_app):
        """Tests that test login and registion with openid"""
        self._setup(openid_plugin_app, False)

        @mock.patch('mediagoblin.plugins.openid.views._finish_verification', self._finish_verification)
        @mock.patch('mediagoblin.plugins.openid.views._start_verification', self._start_verification)
        def _test_non_response():
            template.clear_test_template_context()
            res = openid_plugin_app.post('/auth/openid/login/', {'openid': 'http://phoney.myopenid.com/'})
            res.follow()
            assert urlparse.urlsplit(res.location)[2] == '/auth/openid/login/'
            assert 'mediagoblin/plugins/openid/login.html' in template.TEMPLATE_TEST_CONTEXT

        _test_non_response()
        template.clear_test_template_context()
        self._setup(openid_plugin_app)

        @mock.patch('mediagoblin.plugins.openid.views._finish_verification', self._finish_verification)
        @mock.patch('mediagoblin.plugins.openid.views._start_verification', self._start_verification)
        def _test_new_user():
            openid_plugin_app.post('/auth/openid/login/', {'openid': 'http://real.myopenid.com'})
            assert 'mediagoblin/auth/register.html' in template.TEMPLATE_TEST_CONTEXT
            context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/register.html']
            register_form = context['register_form']
            res = openid_plugin_app.post('/auth/openid/register/', {'openid': register_form.openid.data, 
             'username': 'chris', 
             'email': 'chris@example.com'})
            res.follow()
            assert urlparse.urlsplit(res.location)[2] == '/u/chris/'
            assert 'mediagoblin/user_pages/user_nonactive.html' in template.TEMPLATE_TEST_CONTEXT
            openid_plugin_app.get('/auth/logout')
            test_user = mg_globals.database.LocalUser.query.filter(LocalUser.username == 'chris').first()
            Session.expunge(test_user)
            template.clear_test_template_context()
            res = openid_plugin_app.post('/auth/openid/login/finish/', {'openid': 'http://real.myopenid.com'})
            res.follow()
            assert urlparse.urlsplit(res.location)[2] == '/'
            assert 'mediagoblin/root.html' in template.TEMPLATE_TEST_CONTEXT
            context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/root.html']
            session = context['request'].session
            assert session['user_id'] == six.text_type(test_user.id)

        _test_new_user()
        template.clear_test_template_context()
        openid_plugin_app.post('/auth/openid/register/', {})
        context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/register.html']
        register_form = context['register_form']
        assert register_form.openid.errors == ['This field is required.']
        assert register_form.email.errors == ['This field is required.']
        assert register_form.username.errors == ['This field is required.']
        template.clear_test_template_context()
        openid_plugin_app.post('/auth/openid/register/', {'openid': 'http://real.myopenid.com', 
         'email': 'chris@example.com', 
         'username': 'chris'})
        context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/register.html']
        register_form = context['register_form']
        assert register_form.username.errors == ['Sorry, a user with that name already exists.']
        assert register_form.email.errors == ['Sorry, a user with that email address already exists.']
        assert register_form.openid.errors == ['Sorry, an account is already registered to that OpenID.']

    def test_add_delete(self, openid_plugin_app):
        """Test adding and deleting openids"""
        test_user = fixture_add_user(password='', privileges=['active'])
        openid = OpenIDUserURL()
        openid.openid_url = 'http://real.myopenid.com'
        openid.user_id = test_user.id
        openid.save()
        template.clear_test_template_context()
        self._setup(openid_plugin_app)

        @mock.patch('mediagoblin.plugins.openid.views._finish_verification', self._finish_verification)
        @mock.patch('mediagoblin.plugins.openid.views._start_verification', self._start_verification)
        def _login_user():
            openid_plugin_app.post('/auth/openid/login/finish/', {'openid': 'http://real.myopenid.com'})

        _login_user()
        template.clear_test_template_context()
        res = openid_plugin_app.post('/edit/openid/delete/', {'openid': 'http://real.myopenid.com'})
        assert 'mediagoblin/plugins/openid/delete.html' in template.TEMPLATE_TEST_CONTEXT
        template.clear_test_template_context()
        res = openid_plugin_app.post('/edit/openid/', {})
        context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/plugins/openid/add.html']
        form = context['form']
        assert form.openid.errors == ['This field is required.']
        template.clear_test_template_context()
        openid_plugin_app.post('/edit/openid/', {'openid': 'not_a_url.com'})
        context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/plugins/openid/add.html']
        form = context['form']
        assert form.openid.errors == ['Please enter a valid url.']
        template.clear_test_template_context()
        openid_plugin_app.post('/edit/openid/', {'openid': 'http://real.myopenid.com'})
        context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/plugins/openid/add.html']
        form = context['form']
        assert form.openid.errors == ['Sorry, an account is already registered to that OpenID.']
        template.clear_test_template_context()
        self._setup(openid_plugin_app, edit=True)
        openid = OpenIDUserURL.query.filter_by(openid_url='http://add.myopenid.com')
        openid.delete()

        @mock.patch('mediagoblin.plugins.openid.views._finish_verification', self._finish_verification)
        @mock.patch('mediagoblin.plugins.openid.views._start_verification', self._start_verification)
        def _test_add():
            template.clear_test_template_context()
            res = openid_plugin_app.post('/edit/openid/', {'openid': 'http://add.myopenid.com'})
            res.follow()
            assert urlparse.urlsplit(res.location)[2] == '/edit/account/'
            assert 'mediagoblin/edit/edit_account.html' in template.TEMPLATE_TEST_CONTEXT
            new_openid = mg_globals.database.OpenIDUserURL.query.filter_by(openid_url='http://add.myopenid.com').first()
            assert new_openid

        _test_add()
        template.clear_test_template_context()
        self._setup(openid_plugin_app, delete=True)
        openid = OpenIDUserURL()
        openid.openid_url = 'http://add.myopenid.com'
        openid.user_id = test_user.id
        openid.save()

        @mock.patch('mediagoblin.plugins.openid.views._finish_verification', self._finish_verification)
        @mock.patch('mediagoblin.plugins.openid.views._start_verification', self._start_verification)
        def _test_delete(self, test_user):
            new_user = fixture_add_user(username='newman')
            openid = OpenIDUserURL()
            openid.openid_url = 'http://realfake.myopenid.com/'
            openid.user_id = new_user.id
            openid.save()
            template.clear_test_template_context()
            res = openid_plugin_app.post('/edit/openid/delete/', {'openid': 'http://realfake.myopenid.com/'})
            context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/plugins/openid/delete.html']
            form = context['form']
            assert form.openid.errors == ['That OpenID is not registered to this account.']
            template.clear_test_template_context()
            res = openid_plugin_app.post('/edit/openid/delete/finish/', {'openid': 'http://add.myopenid.com'})
            res.follow()
            assert urlparse.urlsplit(res.location)[2] == '/edit/account/'
            assert 'mediagoblin/edit/edit_account.html' in template.TEMPLATE_TEST_CONTEXT
            new_openid = mg_globals.database.OpenIDUserURL.query.filter_by(openid_url='http://add.myopenid.com').first()
            assert not new_openid

        _test_delete(self, test_user)