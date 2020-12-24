# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_persona.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 8887 bytes
import pkg_resources, pytest, six
try:
    import mock
except ImportError:
    import unittest.mock as mock

import six.moves.urllib.parse as urlparse
pytest.importorskip('requests')
from mediagoblin import mg_globals
from mediagoblin.db.base import Session
from mediagoblin.db.models import Privilege, LocalUser
from mediagoblin.tests.tools import get_app
from mediagoblin.tools import template

@pytest.fixture()
def persona_plugin_app(request):
    return get_app(request, mgoblin_config=pkg_resources.resource_filename('mediagoblin.tests.auth_configs', 'persona_appconfig.ini'))


class TestPersonaPlugin(object):

    def test_authentication_views(self, persona_plugin_app):
        res = persona_plugin_app.get('/auth/login/')
        assert urlparse.urlsplit(res.location)[2] == '/'
        res = persona_plugin_app.get('/auth/register/')
        assert urlparse.urlsplit(res.location)[2] == '/'
        res = persona_plugin_app.get('/auth/persona/login/')
        assert urlparse.urlsplit(res.location)[2] == '/auth/login/'
        res = persona_plugin_app.get('/auth/persona/register/')
        assert urlparse.urlsplit(res.location)[2] == '/auth/login/'

        @mock.patch('mediagoblin.plugins.persona.views._get_response', mock.Mock(return_value='test@example.com'))
        def _test_registration():
            template.clear_test_template_context()
            res = persona_plugin_app.post('/auth/persona/login/', {})
            assert 'mediagoblin/auth/register.html' in template.TEMPLATE_TEST_CONTEXT
            context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/register.html']
            register_form = context['register_form']
            assert register_form.email.data == 'test@example.com'
            assert register_form.persona_email.data == 'test@example.com'
            template.clear_test_template_context()
            res = persona_plugin_app.post('/auth/persona/register/', {})
            assert 'mediagoblin/auth/register.html' in template.TEMPLATE_TEST_CONTEXT
            context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/register.html']
            register_form = context['register_form']
            assert register_form.username.errors == ['This field is required.']
            assert register_form.email.errors == ['This field is required.']
            assert register_form.persona_email.errors == ['This field is required.']
            template.clear_test_template_context()
            res = persona_plugin_app.post('/auth/persona/register/', {'username': 'chris',  'email': 'chris@example.com', 
             'persona_email': 'test@example.com'})
            res.follow()
            assert urlparse.urlsplit(res.location)[2] == '/u/chris/'
            assert 'mediagoblin/user_pages/user_nonactive.html' in template.TEMPLATE_TEST_CONTEXT
            template.clear_test_template_context()
            res = persona_plugin_app.post('/auth/persona/register/', {'username': 'chris1',  'email': 'chris1@example.com', 
             'persona_email': 'test@example.com'})
            assert 'mediagoblin/auth/register.html' in template.TEMPLATE_TEST_CONTEXT
            context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/register.html']
            register_form = context['register_form']
            assert register_form.persona_email.errors == ['Sorry, an account is already registered to that Persona email.']
            persona_plugin_app.get('/auth/logout/')
            test_user = mg_globals.database.LocalUser.query.filter(LocalUser.username == 'chris').first()
            active_privilege = Privilege.query.filter(Privilege.privilege_name == 'active').first()
            test_user.all_privileges.append(active_privilege)
            test_user.save()
            test_user = mg_globals.database.LocalUser.query.filter(LocalUser.username == 'chris').first()
            Session.expunge(test_user)
            persona_plugin_app.post('/auth/persona/register/', {'username': 'chris1',  'email': 'chris1@example.com', 
             'persona_email': 'test1@example.com'})
            template.clear_test_template_context()
            res = persona_plugin_app.post('/auth/persona/login/')
            res.follow()
            assert urlparse.urlsplit(res.location)[2] == '/'
            assert 'mediagoblin/root.html' in template.TEMPLATE_TEST_CONTEXT
            context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/root.html']
            session = context['request'].session
            assert session['user_id'] == six.text_type(test_user.id)

        _test_registration()

        @mock.patch('mediagoblin.plugins.persona.views._get_response', mock.Mock(return_value='new@example.com'))
        def _test_edit_persona():
            template.clear_test_template_context()
            res = persona_plugin_app.post('/edit/persona/', {'email': 'test@example.com'})
            assert 'mediagoblin/plugins/persona/edit.html' in template.TEMPLATE_TEST_CONTEXT
            context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/plugins/persona/edit.html']
            form = context['form']
            assert form.email.errors == ["You can't delete your only Persona email address unless you have a password set."]
            template.clear_test_template_context()
            res = persona_plugin_app.post('/edit/persona/', {})
            assert 'mediagoblin/plugins/persona/edit.html' in template.TEMPLATE_TEST_CONTEXT
            context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/plugins/persona/edit.html']
            form = context['form']
            assert form.email.errors == ['This field is required.']
            template.clear_test_template_context()
            res = persona_plugin_app.post('/edit/persona/', {'email': 'test1@example.com'})
            assert 'mediagoblin/plugins/persona/edit.html' in template.TEMPLATE_TEST_CONTEXT
            context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/plugins/persona/edit.html']
            form = context['form']
            assert form.email.errors == ['That Persona email address is not registered to this account.']
            res = persona_plugin_app.get('/edit/persona/add/')
            assert urlparse.urlsplit(res.location)[2] == '/edit/persona/'
            template.clear_test_template_context()
            res = persona_plugin_app.post('/edit/persona/add/')
            res.follow()
            assert urlparse.urlsplit(res.location)[2] == '/edit/account/'
            res = persona_plugin_app.post('/edit/persona/', {'email': 'test@example.com'})
            res.follow()
            assert urlparse.urlsplit(res.location)[2] == '/edit/account/'

        _test_edit_persona()

        @mock.patch('mediagoblin.plugins.persona.views._get_response', mock.Mock(return_value='test1@example.com'))
        def _test_add_existing():
            template.clear_test_template_context()
            res = persona_plugin_app.post('/edit/persona/add/')
            res.follow()
            assert urlparse.urlsplit(res.location)[2] == '/edit/persona/'

        _test_add_existing()