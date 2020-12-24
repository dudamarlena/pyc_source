# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/zeg/tests/test_http.py
# Compiled at: 2020-04-09 06:21:18
# Size of source mod 2**32: 990 bytes
"""HTTP tests."""
import unittest, requests
from .. import http

class Fake204(object):
    status_code = 204
    content = b''


class Fake201(object):
    status_code = 201
    content = b''


class ErrorHandlingTestCase(unittest.TestCase):

    def test_handle_response_204(self):
        out = http.handle_response(Fake204)
        self.assertIs(out, None)

    def test_handle_empty_response_200(self):
        resp = requests.Response()
        resp._content = b''
        resp.status_code = 200
        out = http.handle_response(resp)
        self.assertIs(out, None)

    def test_handle_response_201(self):
        out = http.handle_response(Fake201)
        self.assertIs(out, None)

    def test_provide_azure_headers(self):
        url = 'https://fake.blob.core.windows.net/container/blob123'
        headers = http.get_platform_headers(url)
        self.assertEqual(headers, {'x-ms-blob-type': 'BlockBlob'})