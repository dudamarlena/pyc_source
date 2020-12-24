# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/featureflow/test_datawriter.py
# Compiled at: 2019-03-01 22:03:23
# Size of source mod 2**32: 511 bytes
import unittest2
from .datawriter import BytesIODataWriter
from .encoder import IdentityEncoder

class StringIODataWriterTests(unittest2.TestCase):

    def test_overflow(self):
        buffer_size_limit = 128
        writer = BytesIODataWriter(needs=(IdentityEncoder()),
          buffer_size_limit=buffer_size_limit)
        data = b'a' * buffer_size_limit
        list(writer._process(data))
        writer._stream.seek(0)
        retrieved = writer._stream.read()
        self.assertEqual(data, retrieved)