# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/tests/test_agent.py
# Compiled at: 2010-02-09 00:00:15
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import unittest
from pyogp.lib.client.agent import Agent, Home
from pyogp.lib.client.login import LegacyLoginParams, OGPLoginParams
from pyogp.lib.client.exc import LoginError
from pyogp.lib.base.tests.mock_xmlrpc import MockXMLRPC
from pyogp.lib.base.tests.base import MockXMLRPCLogin, MockAgentDomainLogin
from pyogp.lib.base.network.tests.mockup_client import MockupClient
import pyogp.lib.base.tests.config

class TestAgent(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.legacy_loginuri = 'http://localhost:12345/cgi-bin/login.cgi'
        self.ogp_loginuri = 'http://localhost:12345/auth.cgi'
        self.firstname = 'firstname'
        self.lastname = 'lastname'
        self.password = 'secret'
        self.client = Agent()

    def tearDown(self):
        pass

    def test_agent_legacy_login_via_variables(self):
        self.loginhandler = MockXMLRPC(MockXMLRPCLogin(), self.legacy_loginuri)
        self.client.login(self.legacy_loginuri, self.firstname, self.lastname, self.password, start_location='start', handler=self.loginhandler, connect_region=False)
        self.assertEquals(self.client.login_response, {'region_y': '256', 'region_x': '256', 'first_name': '"first"', 'secure_session_id': '00000000-0000-0000-0000-000000000000', 'sim_ip': '127.0.0.1', 'agent_access': 'M', 'circuit_code': '600000000', 'look_at': '[r0.9963859999999999939,r-0.084939700000000006863,r0]', 'session_id': '00000000-0000-0000-0000-000000000000', 'udp_blacklist': 'EnableSimulator,TeleportFinish,CrossedRegion', 'seed_capability': 'https://somesim:12043/cap/00000000-0000-0000-0000-000000000000', 'agent_id': '00000000-0000-0000-0000-000000000000', 'last_name': 'last', 'inventory_host': 'someinvhost', 'start_location': 'last', 'sim_port': '13001', 'message': 'message', 'login': 'true', 'seconds_since_epoch': '1234567890'})

    def test_agent_legacy_login_via_params(self):
        self.loginhandler = MockXMLRPC(MockXMLRPCLogin(), self.legacy_loginuri)
        login_params = LegacyLoginParams(self.firstname, self.lastname, self.password)
        self.client.login(self.legacy_loginuri, login_params=login_params, start_location='start', handler=self.loginhandler, connect_region=False)
        self.assertEquals(self.client.login_response, {'region_y': '256', 'region_x': '256', 'first_name': '"first"', 'secure_session_id': '00000000-0000-0000-0000-000000000000', 'sim_ip': '127.0.0.1', 'agent_access': 'M', 'circuit_code': '600000000', 'look_at': '[r0.9963859999999999939,r-0.084939700000000006863,r0]', 'session_id': '00000000-0000-0000-0000-000000000000', 'udp_blacklist': 'EnableSimulator,TeleportFinish,CrossedRegion', 'seed_capability': 'https://somesim:12043/cap/00000000-0000-0000-0000-000000000000', 'agent_id': '00000000-0000-0000-0000-000000000000', 'last_name': 'last', 'inventory_host': 'someinvhost', 'start_location': 'last', 'sim_port': '13001', 'message': 'message', 'login': 'true', 'seconds_since_epoch': '1234567890'})

    def test_agent_ogp_login_via_variables(self):
        self.loginhandler = MockupClient(MockAgentDomainLogin())
        self.client.login(self.ogp_loginuri, self.firstname, self.lastname, self.password, start_location='start', handler=self.loginhandler, connect_region=False)
        self.assertEquals(self.client.login_response, {'agent_seed_capability': 'http://127.0.0.1:12345/seed_cap', 'authenticated': True})

    def test_agent_ogp_login_via_params(self):
        self.loginhandler = MockupClient(MockAgentDomainLogin())
        login_params = OGPLoginParams(self.firstname, self.lastname, self.password)
        self.client.login(self.ogp_loginuri, self.firstname, self.lastname, self.password, start_location='start', handler=self.loginhandler, connect_region=False)
        self.assertEquals(self.client.login_response, {'agent_seed_capability': 'http://127.0.0.1:12345/seed_cap', 'authenticated': True})

    def test_agent_login_no_account_info(self):
        self.assertRaises(LoginError, self.client.login, self.ogp_loginuri)

    def test_legacy_get_login_params(self):
        self.client.grid_type = 'Legacy'
        params = self.client._get_login_params(self.firstname, self.lastname, self.password)
        self.assertEquals(type(params), type(LegacyLoginParams(self.firstname, self.lastname, self.password)))

    def test_ogp_get_login_params(self):
        self.client.grid_type = 'OGP'
        params = self.client._get_login_params(self.firstname, self.lastname, self.password)
        self.assertEquals(type(params), type(OGPLoginParams(self.firstname, self.lastname, self.password)))

    def test_agent_home_class(self):
        home_string = "{'region_handle':[r261120, r247040], 'position':[r171.622, r148.26, r79.3938], 'look_at':[r0, r1, r0]}"
        home = Home(home_string)
        self.assertEquals(home.region_handle, [261120, 247040])
        self.assertEquals(home.position.X, 171.622)
        self.assertEquals(home.position.Y, 148.26)
        self.assertEquals(home.position.Z, 79.3938)
        self.assertEquals(home.look_at.X, 0)
        self.assertEquals(home.look_at.Y, 1)
        self.assertEquals(home.look_at.Z, 0)
        self.assertEquals(home.global_x, 261120)
        self.assertEquals(home.global_y, 247040)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestAgent))
    return suite