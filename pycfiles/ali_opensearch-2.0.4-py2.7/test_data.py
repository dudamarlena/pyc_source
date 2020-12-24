# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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