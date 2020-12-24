# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/opensearchsdk/tests/v2/test_suggest.py
# Compiled at: 2015-12-06 00:20:32
import mock
from opensearchsdk.apiclient.api_base import Manager
from opensearchsdk.tests import base
from opensearchsdk.v2.suggest import SuggestManager

class AppTest(base.TestCase):

    def setUp(self):
        super(AppTest, self).setUp()
        self.suggest_manager = SuggestManager('', '')
        mock_send = mock.Mock()
        Manager.send_get = Manager.send_post = mock_send

    def test_list(self):
        self.suggest_manager.suggest('a', 'b', 'c', 1)
        body = dict(query='a', index_name='b', suggest_name='c', hit='1')
        Manager.send_post.assert_called_with(body)