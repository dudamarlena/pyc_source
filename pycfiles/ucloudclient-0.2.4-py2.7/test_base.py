# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ucloudclient/tests/utils/test_base.py
# Compiled at: 2015-11-11 06:54:58
import mock
from testtools import TestCase
from ucloudclient.utils import base
from ucloudclient import client

class HTTPClientTest(TestCase):

    @mock.patch('ucloudclient.utils.base.HTTPClient')
    def test_contextmanager(self, mock_http_client):
        client.Client('base_url', 'public_key', 'private_key')
        assert mock_http_client.called

    def test_url(self):
        cs = base.HTTPClient(base_url='test_url')
        self.assertIsNone(cs.debug)
        self.assertIsNone(cs.timing)
        self.assertEqual('test_url', cs.base_url)