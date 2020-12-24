# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_login.py
# Compiled at: 2016-09-19 13:27:02
import logging, simplejson as json
from onlinelinguisticdatabase.tests import TestController, url
from nose.tools import nottest
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
log = logging.getLogger(__name__)

class TestLoginController(TestController):

    @nottest
    def test_authenticate(self):
        """Tests that POST /login/authenticate correctly handles authentication attempts."""
        params = json.dumps({'username': 'x', 'password': 'x'})
        response = self.app.post(url(controller='login', action='authenticate'), params, self.json_headers, status=401)
        resp = json.loads(response.body)
        assert resp['error'] == 'The username and password provided are not valid.'
        assert response.content_type == 'application/json'
        params = json.dumps({'username': 'admin', 'password': 'adminA_1'})
        response = self.app.post(url(controller='login', action='authenticate'), params, self.json_headers)
        resp = json.loads(response.body)
        assert resp['authenticated'] == True
        assert response.content_type == 'application/json'
        params = json.dumps({'usernamex': 'admin', 'password': 'admin'})
        response = self.app.post(url(controller='login', action='authenticate'), params, self.json_headers, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['username'] == 'Missing value'
        assert response.content_type == 'application/json'

    @nottest
    def test_logout(self):
        """Tests that GET /login/logout logs the user out."""
        response = self.app.get(url(controller='login', action='logout'), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['authenticated'] == False
        assert response.content_type == 'application/json'
        response = self.app.get(url(controller='login', action='logout'), headers=self.json_headers, status=401)
        resp = json.loads(response.body)
        assert resp['error'] == 'Authentication is required to access this resource.'
        assert response.content_type == 'application/json'

    @nottest
    def test_email_reset_password(self):
        """Tests that POST /login/email_reset_password sends a user a newly generated password.

        I gave up trying to get Python's smtplib to work on Mac OS X.  The email
        functionality in this controller action appears to work on my Debian
        production system.  See the links below for some Mac head-bashing:

        http://pivotallabs.com/users/chad/blog/articles/507-enabling-the-postfix-mail-daemon-on-leopard
        http://webcache.googleusercontent.com/search?q=cache:http://blog.subtlecoolness.com/2009/06/enabling-postfix-sendmail-on-mac-os-x.html
        http://www.agileapproach.com/blog-entry/how-enable-local-smtp-server-postfix-os-x-leopard.
        """
        application_settings = h.generate_default_application_settings()
        Session.add(application_settings)
        Session.commit()
        contributor = Session.query(model.User).filter(model.User.username == 'contributor').first()
        contributor_email = contributor.email
        params = json.dumps({'username': 'contributor', 'password': 'contributorC_1'})
        response = self.app.post(url(controller='login', action='authenticate'), params, self.json_headers)
        resp = json.loads(response.body)
        assert resp['authenticated'] == True
        assert response.content_type == 'application/json'
        config = h.get_config(config_filename='test.ini')
        password_reset_smtp_server = config.get('password_reset_smtp_server')
        test_email_to = config.get('test_email_to')
        to_address = test_email_to or contributor_email
        params = json.dumps({'username': 'contributor'})
        response = self.app.post(url(controller='login', action='email_reset_password'), params, self.json_headers, status=[200, 500])
        resp = json.loads(response.body)
        assert response.status_int == 200 and resp['valid_username'] == True and resp['password_reset'] == True or response.status_int == 500 and resp['error'] == 'The server is unable to send email.'
        assert response.content_type == 'application/json'
        if response.status_int == 200:
            new_password = resp['new_password']
            if password_reset_smtp_server == 'smtp.gmail.com':
                log.info('A new password was emailed via Gmail to %s.' % to_address)
            else:
                log.info('A new password was emailed from localhost to %s.' % to_address)
            params = json.dumps({'username': 'contributor', 'password': 'contributorC_1'})
            response = self.app.post(url(controller='login', action='authenticate'), params, self.json_headers, status=401)
            resp = json.loads(response.body)
            assert resp['error'] == 'The username and password provided are not valid.'
            assert response.content_type == 'application/json'
            params = json.dumps({'username': 'contributor', 'password': new_password})
            response = self.app.post(url(controller='login', action='authenticate'), params, self.json_headers)
            resp = json.loads(response.body)
            assert resp['authenticated'] == True
            assert response.content_type == 'application/json'
        else:
            log.info('localhost was unable to send email.')
            params = json.dumps({'username': 'contributor', 'password': 'contributorC_1'})
            response = self.app.post(url(controller='login', action='authenticate'), params, self.json_headers)
            resp = json.loads(response.body)
            assert resp['authenticated'] == True
            assert response.content_type == 'application/json'
        params = json.dumps({'username': 'badusername'})
        response = self.app.post(url(controller='login', action='email_reset_password'), params, self.json_headers, status=400)
        resp = json.loads(response.body)
        resp['error'] == 'The username provided is not valid.'
        assert response.content_type == 'application/json'
        params = json.dumps({'badparam': 'irrelevant'})
        response = self.app.post(url(controller='login', action='email_reset_password'), params, self.json_headers, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['username'] == 'Missing value'
        assert response.content_type == 'application/json'