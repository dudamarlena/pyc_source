# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/opensearchsdk/tests/base.py
# Compiled at: 2015-12-03 07:22:29
import requests, unittest

class TestCase(unittest.TestCase):
    """wrap testtools.TestCase"""

    def setUp(self):
        super(TestCase, self).setUp()


class TestResponse(requests.Response):
    """wrap request.Response"""

    def __init__(self, data):
        super(TestResponse, self).__init__()
        self._text = None
        self.status_code = data.get('status_code')
        self.headers = data.get('headers')
        self._text = data.get('text')
        self.raise_e = data.get('raise_e', '')
        return

    def json(self):
        if self.raise_e:
            raise self.raise_e
        return self._text