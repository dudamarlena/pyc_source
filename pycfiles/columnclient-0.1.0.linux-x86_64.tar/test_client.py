# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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