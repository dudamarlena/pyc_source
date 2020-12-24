# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/opensearchsdk/tests/v2/test_index.py
# Compiled at: 2015-12-03 09:18:41
import mock
from opensearchsdk.apiclient.api_base import Manager
from opensearchsdk.tests import base
from opensearchsdk.v2.index import IndexManager

class AppTest(base.TestCase):

    def setUp(self):
        super(AppTest, self).setUp()
        self.index_manager = IndexManager('', '')
        mock_send = mock.Mock()
        Manager.send_get = Manager.send_post = mock_send

    def test_refactor_without_data(self):
        self.index_manager.refactor('a')
        body = dict(action='createtask')
        spec_url = '/a'
        Manager.send_post.assert_called_with(body, spec_url)

    def test_refactor_with_data(self):
        self.index_manager.refactor('a', 'b', 'c')
        body = dict(action='createtask', operate='import', table_name='c')
        spec_url = '/a'
        Manager.send_post.assert_called_with(body, spec_url)