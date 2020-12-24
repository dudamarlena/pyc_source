# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_csrf_middleware.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 3620 bytes
from mediagoblin import mg_globals

def test_csrf_cookie_set(test_app):
    cookie_name = mg_globals.app_config['csrf_cookie_name']
    response = test_app.get('/auth/login/')
    assert 'Set-Cookie' in response.headers
    assert cookie_name in test_app.cookies
    assert response.headers.get('Vary', False) == 'Cookie'


def test_csrf_token_must_match(test_app):
    assert test_app.post('/auth/login/', extra_environ={'gmg.verify_csrf': True}, expect_errors=True).status_int == 403
    assert test_app.post('/auth/login/', headers={'Cookie': str('%s=foo' % mg_globals.app_config['csrf_cookie_name'])}, extra_environ={'gmg.verify_csrf': True}, expect_errors=True).status_int == 403
    assert test_app.post('/auth/login/', {'csrf_token': 'blarf'}, headers={'Cookie': str('%s=foo' % mg_globals.app_config['csrf_cookie_name'])}, extra_environ={'gmg.verify_csrf': True}, expect_errors=True).status_int == 403
    assert test_app.post('/auth/login/', {'csrf_token': 'foo'}, headers={'Cookie': str('%s=foo' % mg_globals.app_config['csrf_cookie_name'])}, extra_environ={'gmg.verify_csrf': True}).status_int == 200


def test_csrf_exempt(test_app):
    import mediagoblin.auth.views
    from mediagoblin.meddleware.csrf import csrf_exempt
    mediagoblin.auth.views.login = csrf_exempt(mediagoblin.auth.views.login)
    assert test_app.post('/auth/login/', extra_environ={'gmg.verify_csrf': True}, expect_errors=False).status_int == 200
    mediagoblin.auth.views.login.csrf_enabled = True