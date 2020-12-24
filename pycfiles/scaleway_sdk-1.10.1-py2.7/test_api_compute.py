# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/scaleway/tests/apis/test_api_compute.py
# Compiled at: 2019-12-16 08:49:55
import unittest
from scaleway.apis.api_compute import REGIONS, ComputeAPI

class TestComputeAPI(unittest.TestCase):

    def test_set_region(self):
        self.assertEqual(ComputeAPI().base_url, 'https://cp-par1.scaleway.com/')
        self.assertEqual(ComputeAPI(region='par1').base_url, 'https://cp-par1.scaleway.com/')
        self.assertEqual(ComputeAPI(region='ams1').base_url, 'https://cp-ams1.scaleway.com/')
        self.assertEqual(ComputeAPI(base_url='http://whatever').base_url, 'http://whatever')
        self.assertRaises(AssertionError, ComputeAPI, region='par1', base_url='http://whatever')