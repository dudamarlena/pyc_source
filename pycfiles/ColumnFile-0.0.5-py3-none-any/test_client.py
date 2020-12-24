# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tests/test_client.py
# Compiled at: 2017-08-21 17:07:37
from mock import patch
import testtools
from columnclient import client

class TestClient(testtools.TestCase):

    def setUp(self):
        super(TestClient, self).setUp()

    def tearDown(self):
        super(TestClient, self).tearDown()

    @patch('requests.session')
    def test_init(self, mock_session):
        col_client = client.Client()
        self.assertEqual('http://127.0.0.1:48620', col_client.base_url)