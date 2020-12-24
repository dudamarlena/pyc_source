# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_auth.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 15508 bytes
import pkg_resources, pytest, six, six.moves.urllib.parse as urlparse
from mediagoblin import mg_globals
from mediagoblin.db.models import User, LocalUser
from mediagoblin.tests.tools import get_app, fixture_add_user
from mediagoblin.tools import template, mail
from mediagoblin.auth import tools as auth_tools

def test_register_views(test_app):
    """
    Massive test function that all our registration-related views all work.
    """
    test_app.get('/auth/register/')
    assert 'mediagoblin/auth/register.html' in template.TEMPLATE_TEST_CONTEXT
    template.clear_test_template_context()
    test_app.post('/auth/register/', {})
    context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/register.html']
    form = context['register_form']
    assert form.username.errors == ['This field is required.']
    assert form.password.errors == ['This field is required.']
    assert form.email.errors == ['This field is required.']
    template.clear_test_template_context()
    test_app.post('/auth/register/', {'username': 'l', 
     'password': 'o', 
     'email': 'l'})
    context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/register.html']
    form = context['register_form']
    assert form.username.errors == ['Field must be between 3 and 30 characters long.']
    assert form.password.errors == ['Field must be between 5 and 1024 characters long.']
    template.clear_test_template_context()
    test_app.post('/auth/register/', {'username': '@_@', 
     'email': 'lollerskates'})
    context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/register.html']
    form = context['register_form']
    assert form.username.errors == ['This field does not take email addresses.']
    assert form.email.errors == ['This field requires an email address.']
    template.clear_test_template_context()
    test_app.post('/auth/register/', {'username': 'ampersand&invalid', 
     'email': 'easter@egg.com'})
    context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/register.html']
    form = context['register_form']
    assert form.username.errors == ['Invalid input.']
    assert User.query.count() == 0
    template.clear_test_template_context()
    test_app.post('/auth/register/', {'username': 'Jean-Louis1_Le-Chat', 
     'password': 'iamsohappy', 
     'email': 'easter@egg.com'})
    assert User.query.count() == 1
    template.clear_test_template_context()
    response = test_app.post('/auth/register/', {'username': 'angrygirl', 
     'password': 'iamsoangry', 
     'email': 'angrygrrl@example.org'})
    response.follow()
    assert urlparse.urlsplit(response.location)[2] == '/u/angrygirl/'
    assert 'mediagoblin/user_pages/user_nonactive.html' in template.TEMPLATE_TEST_CONTEXT
    new_user = mg_globals.database.LocalUser.query.filter(LocalUser.username == 'angrygirl').first()
    assert new_user
    assert new_user.has_privilege('commenter')
    assert new_user.has_privilege('uploader')
    assert new_user.has_privilege('reporter')
    assert not new_user.has_privilege('active')
    request = template.TEMPLATE_TEST_CONTEXT['mediagoblin/user_pages/user_nonactive.html']['request']
    assert request.session['user_id'] == six.text_type(new_user.id)
    assert len(mail.EMAIL_TEST_INBOX) == 2
    message = mail.EMAIL_TEST_INBOX.pop()
    assert message['To'] == 'angrygrrl@example.org'
    email_context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/verification_email.txt']
    assert email_context['verification_url'].encode('ascii') in message.get_payload(decode=True)
    path = urlparse.urlsplit(email_context['verification_url'])[2]
    get_params = urlparse.urlsplit(email_context['verification_url'])[3]
    assert path == '/auth/verify_email/'
    parsed_get_params = urlparse.parse_qs(get_params)
    template.clear_test_template_context()
    response = test_app.get('/auth/verify_email/?token=total_bs')
    response.follow()
    assert urlparse.urlsplit(response.location)[2] == '/'
    new_user = mg_globals.database.LocalUser.query.filter(LocalUser.username == 'angrygirl').first()
    assert new_user
    template.clear_test_template_context()
    response = test_app.get('%s?%s' % (path, get_params))
    response.follow()
    context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/user_pages/user.html']
    new_user = mg_globals.database.LocalUser.query.filter(LocalUser.username == 'angrygirl').first()
    assert new_user
    template.clear_test_template_context()
    response = test_app.post('/auth/register/', {'username': 'angrygirl', 
     'password': 'iamsoangry2', 
     'email': 'angrygrrl2@example.org'})
    context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/register.html']
    form = context['register_form']
    assert form.username.errors == [
     'Sorry, a user with that name already exists.']
    template.clear_test_template_context()
    response = test_app.post('/auth/forgot_password/', {'username': 'angrygirl'})
    response.follow()
    assert urlparse.urlsplit(response.location)[2] == '/auth/login/'
    assert 'mediagoblin/auth/login.html' in template.TEMPLATE_TEST_CONTEXT
    assert len(mail.EMAIL_TEST_INBOX) == 2
    message = mail.EMAIL_TEST_INBOX.pop()
    assert message['To'] == 'angrygrrl@example.org'
    email_context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/plugins/basic_auth/fp_verification_email.txt']
    assert email_context['verification_url'].encode('ascii') in message.get_payload(decode=True)
    path = urlparse.urlsplit(email_context['verification_url'])[2]
    get_params = urlparse.urlsplit(email_context['verification_url'])[3]
    parsed_get_params = urlparse.parse_qs(get_params)
    assert path == '/auth/forgot_password/verify/'
    template.clear_test_template_context()
    response = test_app.get('/auth/forgot_password/verify/?token=total_bs')
    response.follow()
    assert urlparse.urlsplit(response.location)[2] == '/'
    template.clear_test_template_context()
    response = test_app.get('%s?%s' % (path, get_params))
    assert 'mediagoblin/plugins/basic_auth/change_fp.html' in template.TEMPLATE_TEST_CONTEXT
    template.clear_test_template_context()
    response = test_app.post('/auth/forgot_password/verify/', {'password': 'iamveryveryangry', 
     'token': parsed_get_params['token']})
    response.follow()
    assert 'mediagoblin/auth/login.html' in template.TEMPLATE_TEST_CONTEXT
    template.clear_test_template_context()
    response = test_app.post('/auth/login/', {'username': 'angrygirl', 
     'password': 'iamveryveryangry'})
    response.follow()
    assert urlparse.urlsplit(response.location)[2] == '/'
    assert 'mediagoblin/root.html' in template.TEMPLATE_TEST_CONTEXT


def test_authentication_views(test_app):
    """
    Test logging in and logging out
    """
    test_user = fixture_add_user()
    test_app.get('/auth/login/')
    assert 'mediagoblin/auth/login.html' in template.TEMPLATE_TEST_CONTEXT
    template.clear_test_template_context()
    response = test_app.post('/auth/login/')
    context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/login.html']
    form = context['login_form']
    assert form.username.errors == ['This field is required.']
    template.clear_test_template_context()
    response = test_app.post('/auth/login/', {'password': 'toast'})
    context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/login.html']
    form = context['login_form']
    assert form.username.errors == ['This field is required.']
    template.clear_test_template_context()
    response = test_app.post('/auth/login/', {'username': 'chris'})
    assert 'mediagoblin/auth/login.html' in template.TEMPLATE_TEST_CONTEXT
    template.clear_test_template_context()
    response = test_app.post('/auth/login/', {'username': 'steve', 
     'password': 'toast'})
    context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/login.html']
    assert context['login_failed']
    template.clear_test_template_context()
    response = test_app.post('/auth/login/', {'username': 'chris', 
     'password': 'jam_and_ham'})
    context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/login.html']
    assert context['login_failed']
    template.clear_test_template_context()
    response = test_app.post('/auth/login/', {'username': 'chris', 
     'password': 'toast'})
    response.follow()
    assert urlparse.urlsplit(response.location)[2] == '/'
    assert 'mediagoblin/root.html' in template.TEMPLATE_TEST_CONTEXT
    context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/root.html']
    session = context['request'].session
    assert session['user_id'] == six.text_type(test_user.id)
    template.clear_test_template_context()
    response = test_app.get('/auth/logout/')
    response.follow()
    assert urlparse.urlsplit(response.location)[2] == '/'
    assert 'mediagoblin/root.html' in template.TEMPLATE_TEST_CONTEXT
    context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/root.html']
    session = context['request'].session
    assert 'user_id' not in session
    template.clear_test_template_context()
    response = test_app.post('/auth/login/', {'username': 'chris', 
     'password': 'toast', 
     'next': '/u/chris/'})
    assert urlparse.urlsplit(response.location)[2] == '/u/chris/'
    template.clear_test_template_context()
    response = test_app.post('/auth/login/', {'username': 'ANDREW', 
     'password': 'fuselage'})
    context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/auth/login.html']
    form = context['login_form']
    assert not form.username.data == 'ANDREW'
    assert form.username.data == 'andrew'


@pytest.fixture()
def authentication_disabled_app(request):
    return get_app(request, mgoblin_config=pkg_resources.resource_filename('mediagoblin.tests.auth_configs', 'authentication_disabled_appconfig.ini'))


def test_authentication_disabled_app(authentication_disabled_app):
    assert mg_globals
    assert mg_globals.app.auth is False
    template.clear_test_template_context()
    response = authentication_disabled_app.get('/auth/register/')
    response.follow()
    assert urlparse.urlsplit(response.location)[2] == '/'
    assert 'mediagoblin/root.html' in template.TEMPLATE_TEST_CONTEXT
    template.clear_test_template_context()
    response = authentication_disabled_app.get('/auth/login/')
    response.follow()
    assert urlparse.urlsplit(response.location)[2] == '/'
    assert 'mediagoblin/root.html' in template.TEMPLATE_TEST_CONTEXT
    assert auth_tools.check_login_simple('test', 'simple') is None
    template.clear_test_template_context()
    response = authentication_disabled_app.get('/auth/register/')
    response.follow()
    assert urlparse.urlsplit(response.location)[2] == '/'
    assert 'mediagoblin/root.html' in template.TEMPLATE_TEST_CONTEXT