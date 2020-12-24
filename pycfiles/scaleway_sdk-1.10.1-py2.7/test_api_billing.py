# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/scaleway/tests/apis/test_api_billing.py
# Compiled at: 2019-12-16 08:49:55
import unittest
from scaleway.apis.api_billing import BillingAPI

class TestBillingAPI(unittest.TestCase):

    def test_valid_endpoint(self):
        self.assertEqual(BillingAPI().base_url, 'https://billing.scaleway.com')