# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hpppm/test/demand_management_tests.py
# Compiled at: 2012-12-19 03:59:47
import unittest, os, sys
from hpppm.demand_management import *

class T(unittest.TestCase):
    __module__ = __name__
    inp = {'requestType': ['A'], 'fields': ['REQ.VP.APP', 'ART', 'REQ.VP.ID', 'xyz1'], 'serviceUrl': ['http://python.org']}
    req = None

    def setUp(self):
        self.dm = DemandManagement()
        self.dm.data['CURRENT_OPERATION'] = 'createRequest'
        self.dm.data['OPS_INPUTS_REQD'] = {'createRequest': ['serviceUrl', 'requestType']}
        self.dm.data['OPS_INPUTS'] = {'createRequest': ['serviceUrl', 'requestType', 'fields', 'references', 'notes']}

    def test_create_request(self):
        T.req = self.dm.create_request(T.inp)
        self.assert_(T.req is not None)
        return

    def test_post_request(self):
        res = hasattr(self.dm, 'post_request')
        self.assert_(res is not None)
        return


if __name__ == '__main__':
    unittest.main()