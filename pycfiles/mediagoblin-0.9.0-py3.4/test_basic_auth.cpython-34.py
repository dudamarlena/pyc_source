# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_basic_auth.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 3809 bytes
import six.moves.urllib.parse as urlparse
from mediagoblin.db.models import User, LocalUser
from mediagoblin.plugins.basic_auth import tools as auth_tools
from mediagoblin.tests.tools import fixture_add_user
from mediagoblin.tools import template
from mediagoblin.tools.testing import _activate_testing
_activate_testing()

def test_bcrypt_check_password():
    assert auth_tools.bcrypt_check_password('lollerskates', '$2a$12$PXU03zfrVCujBhVeICTwtOaHTUs5FFwsscvSSTJkqx/2RQ0Lhy/nO')
    assert not auth_tools.bcrypt_check_password('notthepassword', '$2a$12$PXU03zfrVCujBhVeICTwtOaHTUs5FFwsscvSSTJkqx/2RQ0Lhy/nO')
    assert not auth_tools.bcrypt_check_password('notthepassword', '$2a$12$ELVlnw3z1FMu6CEGs/L8XO8vl0BuWSlUHgh0rUrry9DUXGMUNWwl6', '3><7R45417')


def test_bcrypt_gen_password_hash():
    pw = 'youwillneverguessthis'
    hashed_pw = auth_tools.bcrypt_gen_password_hash(pw)
    assert auth_tools.bcrypt_check_password(pw, hashed_pw)
    assert not auth_tools.bcrypt_check_password('notthepassword', hashed_pw)
    hashed_pw = auth_tools.bcrypt_gen_password_hash(pw, '3><7R45417')
    assert auth_tools.bcrypt_check_password(pw, hashed_pw, '3><7R45417')
    assert not auth_tools.bcrypt_check_password('notthepassword', hashed_pw, '3><7R45417')


def test_change_password(test_app):
    """Test changing password correctly and incorrectly"""
    test_user = fixture_add_user(password='toast', privileges=[
     'active'])
    test_app.post('/auth/login/', {'username': 'chris', 
     'password': 'toast'})
    res = test_app.post('/edit/password/', {'old_password': 'toast', 
     'new_password': '123456'})
    res.follow()
    assert urlparse.urlsplit(res.location)[2] == '/edit/account/'
    test_user = LocalUser.query.filter(LocalUser.username == 'chris').first()
    assert auth_tools.bcrypt_check_password('123456', test_user.pw_hash)
    template.clear_test_template_context()
    test_app.post('/edit/password/', {'old_password': 'toast', 
     'new_password': '098765'})
    test_user = LocalUser.query.filter(LocalUser.username == 'chris').first()
    assert not auth_tools.bcrypt_check_password('098765', test_user.pw_hash)