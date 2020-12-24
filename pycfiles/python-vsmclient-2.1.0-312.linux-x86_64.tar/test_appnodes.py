# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/tests/unit/v1/test_appnodes.py
# Compiled at: 2016-06-13 14:11:03
from vsmclient.v1 import appnodes
from vsmclient.tests.unit import utils
from vsmclient.tests.unit.v1 import fakes
cs = fakes.FakeClient()

class AppnodesTest(utils.TestCase):

    def test_create_appnode(self):
        cs.appnodes.create({'os_username': 'admin', 
           'os_password': 'admin', 
           'os_tenant_name': 'admin', 
           'os_auth_url': 'http://192.168.100.100:5000/v2.0', 
           'os_region_name': 'RegionOne', 
           'ssh_user': 'root'})
        cs.assert_called('POST', '/appnodes')

    def test_list_appnodes(self):
        ans = cs.appnodes.list()
        cs.assert_called('GET', '/appnodes')
        for an in ans:
            self.assertIsInstance(an, appnodes.AppNode)