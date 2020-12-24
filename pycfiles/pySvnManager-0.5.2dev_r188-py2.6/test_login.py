# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/tests/functional/test_login.py
# Compiled at: 2010-08-08 03:18:44
from pysvnmanager.tests import *
import pylons.test

class TestLoginController(TestController):

    def test_login_logout(self):
        wsgiapp = pylons.test.pylonsapp
        config = wsgiapp.config
        params = {}
        params['username'] = 'root'
        d = eval(config.get('test_users', {}))
        password = d.get(params['username'], '')
        params['password'] = password
        res = self.app.get(url(controller='security', action='submit'), params)
        self.assert_(res.status == '302 Found', res.status)
        self.assert_(res.location == '/' or res.location == 'http://localhost/', res.location)
        self.assert_(res.session['user'] == 'root', res.session)
        res = self.app.get(url(controller='security', action='index'))
        self.assert_('<h2>Login</h2>' in res.body, res.body)
        self.assert_(res.session['user'] == 'root', res.session)
        params['username'] = 'root'
        params['password'] = 'wrong_passwd'
        res = self.app.get(url(controller='security', action='submit'), params)
        self.assert_(res.status == '200 OK', res.status)
        self.assert_('Login failed for user: root' in res.body, res.body)
        self.assert_(res.session.get('user') == None, res.session.get('user'))
        self.login('jiangxin')
        res = self.app.get(url(controller='security', action='index'))
        self.assert_(res.session.get('user') == 'jiangxin', res.session)
        res = self.app.get(url(controller='security', action='logout'))
        self.assert_(res.status == '302 Found', res.status)
        self.assert_(res.location == '/login' or res.location == 'http://localhost/login', res.location)
        self.assert_(res.session.get('user') == None, res.session.get('user'))
        return