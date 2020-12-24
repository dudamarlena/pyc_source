# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/django-smart-proxy/lib/python3.3/site-packages/smart_proxy/tests.py
# Compiled at: 2014-11-26 21:04:56
# Size of source mod 2**32: 291 bytes
from django.test import Client, TestCase

class SmartProxyTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_proxy_not_configured(self):
        response = self.client.get('/does_not_exist/')