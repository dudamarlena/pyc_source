# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tests/unit/test_client.py
# Compiled at: 2015-12-08 14:33:04
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from pypermedia.client import HypermediaClient, ConnectError
import mock, requests, unittest2

class TestClient(unittest2.TestCase):
    """
    This is kinda shit since it really
    needs to be integration tested.
    """

    def test_connect(self):
        builder = mock.MagicMock()
        request_factory = mock.MagicMock()
        session = mock.MagicMock()
        resp = HypermediaClient.connect(b'blah', session=session, request_factory=request_factory, builder=builder)
        self.assertEqual(builder.return_value.from_api_response.return_value.as_python_object.return_value, resp)

    def test_send_and_construct(self):
        builder = mock.MagicMock()
        request_factory = mock.MagicMock()
        session = mock.MagicMock()
        request = mock.Mock(url=b'url')
        resp = HypermediaClient.send_and_construct(request, session=session, request_factory=request_factory, builder=builder)
        self.assertEqual(builder.return_value.from_api_response.return_value.as_python_object.return_value, resp)

    def test_send_and_construct_error(self):
        request = mock.Mock(url=b'url')
        session = mock.Mock(send=mock.Mock(side_effect=requests.exceptions.ConnectionError))
        self.assertRaises(ConnectError, HypermediaClient.send_and_construct, request, session=session)