# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/opensearchsdk/tests/v2/test_search.py
# Compiled at: 2015-12-05 11:03:46
import mock
from opensearchsdk.apiclient.api_base import Manager
from opensearchsdk.tests import base
from opensearchsdk.v2.search import SearchManager

class AppTest(base.TestCase):

    def setUp(self):
        super(AppTest, self).setUp()
        self.search_manager = SearchManager('', '')
        mock_send = mock.Mock()
        Manager.send_get = Manager.send_post = mock_send

    def test_search(self):
        self.search_manager.search('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        body = dict(query='a', index_name='b', fetch_fields='c', qp='d', disable='e', first_formula_name='f', formula_name='g', summary='h')
        Manager.send_get.assert_called_with(body)
        body['scroll'] = '1h'
        body['search_type'] = 'scan'
        self.search_manager.search('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', '1h', 'scan')
        Manager.send_get.assert_called_with(body)
        body = dict(scroll='1h', scroll_id='i')
        self.search_manager.search(**body)
        Manager.send_get.assert_called_with(body)