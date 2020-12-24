# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_auth/tests/test_view.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 1898 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, re
from django.contrib.auth import get_user_model
from django.test import override_settings
from pytest_data import use_data

@use_data(user_data={'username': 'testuser', 'password': 'testpass'})
def test_login(client, user):
    res = client.post('/en/auth/login/', {'username': 'testuser', 'password': 'testpass'})
    @py_assert1 = res.status_code
    @py_assert4 = 302
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(res) if 'res' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(res) else 'res'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_register(mailoutbox, client):
    @py_assert2 = len(mailoutbox)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(mailoutbox) if 'mailoutbox' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mailoutbox) else 'mailoutbox', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = get_user_model()
    @py_assert3 = @py_assert1.objects
    @py_assert5 = @py_assert3.filter
    @py_assert7 = 'testuser'
    @py_assert9 = @py_assert5(username=@py_assert7)
    @py_assert11 = not @py_assert9
    if not @py_assert11:
        @py_format12 = ('' + 'assert not %(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s()\n}.objects\n}.filter\n}(username=%(py8)s)\n}') % {'py10': @pytest_ar._saferepr(@py_assert9), 'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py6': @pytest_ar._saferepr(@py_assert5), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(get_user_model) if 'get_user_model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_user_model) else 'get_user_model'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    user = _register_user(client)
    @py_assert1 = user.email
    @py_assert4 = 'testuser@example.com'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.email\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(user) if 'user' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(user) else 'user'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert2 = len(mailoutbox)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(mailoutbox) if 'mailoutbox' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mailoutbox) else 'mailoutbox', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    activation_mail = mailoutbox[0]
    @py_assert0 = 'activate'
    @py_assert4 = activation_mail.body
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.body\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(activation_mail) if 'activation_mail' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(activation_mail) else 'activation_mail', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'http'
    @py_assert4 = activation_mail.body
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.body\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(activation_mail) if 'activation_mail' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(activation_mail) else 'activation_mail', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@override_settings(AUTHENTICATION_BACKENDS=[
 'django.contrib.auth.backends.ModelBackend',
 'cms_qe_auth.tests.utils.TestAuthBackend'])
def test_activation_multiple_authentication_backends(client, mailoutbox):
    _test_activation(client, mailoutbox)


def test_activation(client, mailoutbox):
    _test_activation(client, mailoutbox)


def _test_activation(client, mailoutbox):
    user = _register_user(client)
    @py_assert1 = user.is_active
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.is_active\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(user) if 'user' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(user) else 'user'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    activation_mail = mailoutbox[0]
    activate_url_pattern = '(?P<url>https?://[^\\s]+/activate/[^\\s]+)'
    url = re.search(activate_url_pattern, activation_mail.body).group('url')
    response = client.get(url)
    user.refresh_from_db()
    @py_assert1 = user.is_active
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.is_active\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(user) if 'user' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(user) else 'user'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert0 = response.context['user']
    @py_assert2 = @py_assert0.is_authenticated
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py1)s.is_authenticated\n}') % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert0 = @py_assert2 = None


def _register_user(client):
    res = client.post('/en/auth/register/', {'username': 'testuser', 
     'password1': 'testpass', 
     'password2': 'testpass', 
     'email': 'testuser@example.com'})
    @py_assert1 = res.status_code
    @py_assert4 = 302
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(res) if 'res' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(res) else 'res'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return get_user_model().objects.get(username='testuser')