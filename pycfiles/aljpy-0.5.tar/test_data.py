# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/opensearchsdk/tests/v2/test_data.py
# Compiled at: 2016-09-02 10:15:12
import mock
from opensearchsdk.apiclient.api_base import Manager
from opensearchsdk.tests import base
from opensearchsdk.v2.data import DataManager
FAKE_RESP = {'data': 'name'}

class AppTest(base.TestCase):

    def setUp(self):
        super(AppTest, self).setUp()
        self.data_manager = DataManager('', '')
        mock_send = mock.Mock(return_value=FAKE_RESP)
        Manager.send_get = Manager.send_post = mock_send

    def test_list(self):
        resp = self.data_manager.create('a', '1', '2')
        self.assertEqual(FAKE_RESP, resp)
        Manager.send_post.assert_called_with({'table_name': '1', 'items': '2'}, '/a')