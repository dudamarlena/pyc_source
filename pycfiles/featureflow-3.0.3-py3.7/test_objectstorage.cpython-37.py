# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/featureflow/test_objectstorage.py
# Compiled at: 2019-03-01 22:03:23
# Size of source mod 2**32: 702 bytes
import unittest2
from .objectstore import WriteStream
import http.client
from collections import namedtuple

class WriteStreamTests(unittest2.TestCase):

    def test_write_stream_does_not_put_zero_bytes(self):

        class TestWriteStream(WriteStream):

            def __init__(self):
                super(TestWriteStream, self).__init__(None, None, None, None)
                self._put_count = 0

            def _put(self):
                self._put_count += 1
                response_cls = namedtuple('Response', 'status_code')
                return response_cls(status_code=(http.client.NO_CONTENT))

        ws = TestWriteStream()
        ws.close()
        self.assertEqual(0, ws._put_count)