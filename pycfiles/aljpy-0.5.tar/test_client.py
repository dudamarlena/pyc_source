# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/opensearchsdk/tests/test_client.py
# Compiled at: 2015-11-19 10:03:29
from opensearchsdk import client
from opensearchsdk.tests import base
URL = 'http://www.aliyun.com'
KEY = 'KEY'
KEY_ID = 'KEY_ID'

class ClientTest(base.TestCase):

    def test_passing_property(self):
        c = client.Client(URL, KEY, KEY_ID)
        self.assertEqual(KEY, c.key)
        self.assertEqual(URL, c.http_client.base_url)
        self.assertEqual(client.APP_URL, c.app.resource_url)
        self.assertEqual(c, c.app.api)