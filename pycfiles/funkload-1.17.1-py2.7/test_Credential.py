# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/demo/xmlrpc/test_Credential.py
# Compiled at: 2015-05-06 05:03:08
"""Simple FunkLoad test

$Id$
"""
import unittest
from random import random
from funkload.FunkLoadTestCase import FunkLoadTestCase

class Credential(FunkLoadTestCase):
    """This test use a configuration file Credential.conf."""

    def setUp(self):
        """Setting up test."""
        self.logd('setUp')
        self.server_url = self.conf_get('main', 'url')

    def test_credential(self):
        server_url = self.server_url
        ret = self.xmlrpc(server_url, 'getStatus', description='Check getStatus')
        self.assert_('running' in ret, 'Server is down %s' % ret)
        self.logd('ret %s' % ret)
        ret = self.xmlrpc(server_url, 'getCredential', description='Get a credential from a file')
        self.logd('ret %s' % ret)
        self.assertEquals(len(ret), 2, 'Invalid return %s' % ret)
        ret = self.xmlrpc(server_url, 'listGroups', description='list groups from the group file')
        self.logd('ret %s' % ret)
        a_group = ret[0]
        ret = self.xmlrpc(server_url, 'listCredentials', description='list all credential of the file')
        self.logd('ret %s' % ret)
        ret = self.xmlrpc(server_url, 'listCredentials', (a_group,), description='list credentials of group ' + a_group)
        self.logd('ret %s' % ret)

    def tearDown(self):
        """Setting up test."""
        self.logd('tearDown.\n')


if __name__ in ('main', '__main__'):
    unittest.main()