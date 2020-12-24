# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/tests/test_ogp_login.py
# Compiled at: 2010-02-09 00:00:15
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import unittest
from pyogp.lib.client.login import Login, OGPLoginParams
from pyogp.lib.base.exc import *
from pyogp.lib.base.tests.base import MockAgentDomainLogin
from pyogp.lib.base.network.tests.mockup_client import MockupClient
import pyogp.lib.base.tests.config

class TestOGPLogin(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.ogp_loginuri = 'http://localhost:12345/auth.cgi'
        self.login_params = OGPLoginParams('firstname', 'lastname', 'secret')
        self.login = Login()
        self.loginhandler = MockupClient(MockAgentDomainLogin())

    def tearDown(self):
        pass

    def test_OGPLogin(self):
        response = self.login.login(self.ogp_loginuri, self.login_params, 'region', handler=self.loginhandler)
        self.assertEquals(response, {'authenticated': True, 'agent_seed_capability': 'http://127.0.0.1:12345/seed_cap'})
        self.assertEquals(self.login.response['authenticated'], True)
        self.assertEquals(self.login.response['agent_seed_capability'], 'http://127.0.0.1:12345/seed_cap')

    def test_ogp_login_return(self):
        result = self.login.login(self.ogp_loginuri, self.login_params, 'start_location', handler=self.loginhandler)
        self.assertEquals(self.login.response, result, 'Login.login should return response in the result set')

    def test_OGPParams(self):
        login_params = OGPLoginParams('first', 'last', 'password')
        self.assertEquals(login_params.firstname, 'first')
        self.assertEquals(login_params.lastname, 'last')
        self.assertEquals(login_params.password, 'password')
        serialized = login_params.serialize()
        self.assertEquals(serialized, '<?xml version="1.0" ?><llsd><map><key>lastname</key><string>last</string><key>password</key><string>password</string><key>firstname</key><string>first</string></map></llsd>')

    def test_failed_ogp_login(self):
        self.login_params.password = 'badpassword'
        self.assertRaises(ResourceError, self.login.login, self.ogp_loginuri, self.login_params, 'start_location', handler=self.loginhandler)

    def test_login_attributes(self):
        self.login.login(self.ogp_loginuri, self.login_params, 'start_location', handler=self.loginhandler)
        self.assertEquals(self.login_params.serialize(), self.login.login_params)
        self.assertEquals(self.login.type, 'ogp')
        self.assertEquals(self.login.transform_response, None)
        self.assertEquals(self.login.response, {'agent_seed_capability': 'http://127.0.0.1:12345/seed_cap', 'authenticated': True})
        return

    def test_unknown_loginuri(self):
        self.fake_loginuri = 'http://localhost:12345/fake.cgi'
        self.assertRaises(LoginError, self.login.login, self.fake_loginuri, self.login_params, 'start_location', handler=self.loginhandler)

    def test_init_ogp_login_params(self):
        loginuri = 'http://localhost:12345/login.cgi'
        start_location = 'region'
        self.login._init_ogp_login_params(loginuri, self.login_params, start_location)
        self.assertEquals(self.login.loginuri, loginuri)
        self.assertEquals(self.login.start_location, 'region')
        self.assertEquals(self.login.login_params, '<?xml version="1.0" ?><llsd><map><key>lastname</key><string>lastname</string><key>password</key><string>secret</string><key>firstname</key><string>firstname</string></map></llsd>')

    def test_preserved_login_input_params(self):
        result = self.login.login(self.ogp_loginuri, self.login_params, 'start_location', handler=self.loginhandler)
        self.assertEquals('firstname', self.login.input_params['firstname'])
        self.assertEquals('lastname', self.login.input_params['lastname'])
        self.assertEquals('secret', self.login.input_params['password'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestOGPLogin))
    return suite