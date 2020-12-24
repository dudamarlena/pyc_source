# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/views/test_logout.py
# Compiled at: 2017-02-24 16:57:38
__doc__ = 'Logout related tests.'
import time
from tests.tools import authenticate, is_user_logged

def test_logout(active_user, extended_app):
    """Check logout action."""
    authenticate(extended_app)
    assert is_user_logged(extended_app) is True
    extended_app.get('/logout', status=303)
    assert is_user_logged(extended_app) is False
    res = extended_app.get('/secret', status=302)
    assert res.status_code == 302


def test_logout_login(active_user, extended_config, extended_app):
    """Check logout action with configured logout redirection."""
    extended_config.registry['config'].fullauth.redirects.logout = 'login'
    authenticate(extended_app)
    assert is_user_logged(extended_app) is True
    res = extended_app.get('/logout', status=303)
    assert is_user_logged(extended_app) is False
    assert '/login' in res.location
    res = extended_app.get('/secret', status=302)
    assert res.status_code == 302


def test_automatic_logout(active_user, short_config, short_app):
    """Test automatic logout."""
    timeout = short_config.registry['config']['fullauth']['AuthTkt']['timeout'] + 1
    authenticate(short_app)
    time.sleep(timeout)
    res = short_app.get('/email/change')
    assert res.headers['Location'] == 'http://localhost/login?after=%2Femail%2Fchange'
    res = res.follow()
    assert res.form