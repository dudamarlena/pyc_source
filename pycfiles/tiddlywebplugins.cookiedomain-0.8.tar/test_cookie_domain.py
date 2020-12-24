# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.cookiedomain/test/test_cookie_domain.py
# Compiled at: 2011-11-12 12:05:47
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2
from tiddlyweb.store import Store
from tiddlyweb.model.user import User
from tiddlywebplugins.utils import get_store
import os, shutil

def setup_module(module):
    if os.path.exists('store'):
        shutil.rmtree('store')
    from tiddlyweb.config import config
    from tiddlyweb.web import serve

    def app_fn():
        return serve.load_app()

    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    module.store = get_store(config)
    user = User('cdent')
    user.set_password('cow')
    module.store.put(user)


def test_check_cookie():
    http = httplib2.Http()
    response, content = http.request('http://0.0.0.0:8080/challenge/cookie_form', body='user=%s&password=%s' % ('cdent',
                                                                                                                'cow'), method='POST', headers={'Content-Type': 'application/x-www-form-urlencoded'})
    assert response.previous['status'] == '303'
    user_cookie = response.previous['set-cookie']
    assert 'cdent:' in user_cookie
    assert 'tiddlyweb_user' in user_cookie
    assert 'Domain=0.0.0.0' in user_cookie
    assert 'httponly' in user_cookie