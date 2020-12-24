# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/tests/functional/test_authentication.py
# Compiled at: 2010-10-13 09:43:04
"""
Integration tests for the :mod:`repoze.who`-powered authentication sub-system.

As pyf.services grows and the authentication method changes, only these tests
should be updated.

"""
from pyf.services.tests import TestController

class TestAuthentication(TestController):
    """
    Tests for the default authentication setup.
    
    By default in TurboGears 2, :mod:`repoze.who` is configured with the same
    plugins specified by repoze.what-quickstart (which are listed in
    http://code.gustavonarea.net/repoze.what-quickstart/#repoze.what.plugins.quickstart.setup_sql_auth).
    
    As the settings for those plugins change, or the plugins are replaced,
    these tests should be updated.
    
    """
    application_under_test = 'main'

    def test_forced_login(self):
        """
        Anonymous users must be redirected to the login form when authorization
        is denied.
        
        Next, upon successful login they should be redirected to the initially
        requested page.
        
        """
        resp = self.app.get('/users/', status=302)
        assert resp.location.startswith('http://localhost/login')
        resp = resp.follow(status=200)
        form = resp.form
        form['login'] = 'manager'
        form['password'] = 'managepass'
        post_login = form.submit(status=302)
        assert post_login.location.startswith('http://localhost/post_login')
        initial_page = post_login.follow(status=302)
        assert 'authtkt' in initial_page.request.cookies, "Session cookie wasn't defined: %s" % initial_page.request.cookies
        assert initial_page.location.startswith('http://localhost/users/'), initial_page.location

    def test_voluntary_login(self):
        """Voluntary logins must work correctly"""
        resp = self.app.get('/login', status=200)
        form = resp.form
        form['login'] = 'manager'
        form['password'] = 'managepass'
        post_login = form.submit(status=302)
        assert post_login.location.startswith('http://localhost/post_login')
        home_page = post_login.follow(status=302)
        assert 'authtkt' in home_page.request.cookies, 'Session cookie was not defined: %s' % home_page.request.cookies
        assert home_page.location == 'http://localhost/'

    def test_logout(self):
        """Logouts must work correctly"""
        resp = self.app.get('/login_handler?login=manager&password=managepass', status=302)
        resp = resp.follow(status=302)
        assert 'authtkt' in resp.request.cookies, 'Session cookie was not defined: %s' % resp.request.cookies
        resp = self.app.get('/logout_handler', status=302)
        assert resp.location.startswith('http://localhost/post_logout')
        home_page = resp.follow(status=302)
        assert home_page.request.cookies.get('authtkt') == '', 'Session cookie was not deleted: %s' % home_page.request.cookies
        assert home_page.location == 'http://localhost/', home_page.location