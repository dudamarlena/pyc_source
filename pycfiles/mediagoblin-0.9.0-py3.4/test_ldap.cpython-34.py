# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_ldap.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 4729 bytes
import pkg_resources, pytest, six
try:
    import mock
except ImportError:
    import unittest.mock as mock

import six.moves.urllib.parse as urlparse
from mediagoblin import mg_globals
from mediagoblin.db.base import Session
from mediagoblin.db.models import LocalUser
from mediagoblin.tests.tools import get_app
from mediagoblin.tools import template
pytest.importorskip('ldap')

@pytest.fixture()
def ldap_plugin_app(request):
    return get_app(request, mgoblin_config=pkg_resources.resource_filename('mediagoblin.tests.auth_configs', 'ldap_appconfig.ini'))


def return_value():
    return ('chris', 'chris@example.com')


def test_ldap_plugin(ldap_plugin_app):
    res = ldap_plugin_app.get('/auth/login/')
    assert urlparse.urlsplit(res.location)[2] == '/auth/ldap/login/'
    res = ldap_plugin_app.get('/auth/register/')
    assert urlparse.urlsplit(res.location)[2] == '/auth/ldap/register/'
    res = ldap_plugin_app.get('/auth/ldap/register/')
    assert urlparse.urlsplit(res.location)[2] == '/auth/ldap/login/'
    template.clear_test_template_context()
    res = ldap_plugin_app.post('/auth/ldap/login/', {})
    context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/login.html']
    form = context['login_form']
    assert form.username.errors == ['This field is required.']
    assert form.password.errors == ['This field is required.']

    @mock.patch('mediagoblin.plugins.ldap.tools.LDAP.login', mock.Mock(return_value=return_value()))
    def _test_authentication():
        template.clear_test_template_context()
        res = ldap_plugin_app.post('/auth/ldap/login/', {'username': 'chris',  'password': 'toast'})
        context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/register.html']
        register_form = context['register_form']
        assert register_form.username.data == 'chris'
        assert register_form.email.data == 'chris@example.com'
        template.clear_test_template_context()
        res = ldap_plugin_app.post('/auth/ldap/register/', {'username': 'chris',  'email': 'chris@example.com'})
        res.follow()
        assert urlparse.urlsplit(res.location)[2] == '/u/chris/'
        assert 'mediagoblin/user_pages/user_nonactive.html' in template.TEMPLATE_TEST_CONTEXT
        template.clear_test_template_context()
        res = ldap_plugin_app.post('/auth/ldap/register/', {'username': 'chris',  'email': 'chris@example.com'})
        context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/register.html']
        register_form = context['register_form']
        assert register_form.email.errors == [
         'Sorry, a user with that email address already exists.']
        assert register_form.username.errors == [
         'Sorry, a user with that name already exists.']
        ldap_plugin_app.get('/auth/logout/')
        test_user = mg_globals.database.LocalUser.query.filter(LocalUser.username == 'chris').first()
        Session.expunge(test_user)
        template.clear_test_template_context()
        res = ldap_plugin_app.post('/auth/ldap/login/', {'username': 'chris',  'password': 'toast'})
        res.follow()
        assert urlparse.urlsplit(res.location)[2] == '/'
        assert 'mediagoblin/root.html' in template.TEMPLATE_TEST_CONTEXT
        context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/root.html']
        session = context['request'].session
        assert session['user_id'] == six.text_type(test_user.id)

    _test_authentication()