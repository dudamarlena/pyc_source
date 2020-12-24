# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x/code/OONI/ooni-probe/docs/source/../../ooni/nettests/examples/example_http_checksum.py
# Compiled at: 2016-03-17 16:00:08
from ooni.utils import log
from ooni.templates import httpt
from hashlib import sha256

class SHA256HTTPBodyTest(httpt.HTTPTest):
    name = 'ChecksumHTTPBodyTest'
    author = 'Aaron Gibson'
    version = 0.1
    inputFile = [
     'file', 'f', None,
     'List of URLS to perform GET requests to']

    def test_http(self):
        if self.input:
            url = self.input
            return self.doRequest(url)
        raise Exception('No input specified')

    def processResponseBody(self, body):
        body_sha256sum = sha256(body).digest()
        self.report['checksum'] = body_sha256sum