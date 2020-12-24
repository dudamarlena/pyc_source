# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/pykafka/utils/test_compression.py
# Compiled at: 2018-07-24 12:58:48
# Size of source mod 2**32: 2253 bytes
import lz4f, platform, pytest, unittest2
from uuid import uuid4
from pykafka.utils import compression

class CompressionTests(unittest2.TestCase):
    __doc__ = 'Keeping these simple by verifying what goes in is what comes out.'
    text = b'The man in black fled across the desert, and the gunslinger followed.'

    def test_gzip(self):
        encoded = compression.encode_gzip(self.text)
        self.assertNotEqual(self.text, encoded)
        decoded = compression.decode_gzip(encoded)
        self.assertEqual(self.text, decoded)

    def test_snappy(self):
        encoded = compression.encode_snappy(self.text)
        self.assertNotEqual(self.text, encoded)
        decoded = compression.decode_snappy(encoded)
        self.assertEqual(self.text, decoded)

    def test_snappy_xerial(self):
        encoded = compression.encode_snappy((self.text), xerial_compatible=True)
        self.assertNotEqual(self.text, encoded)
        decoded = compression.decode_snappy(encoded)
        self.assertEqual(self.text, decoded)

    def test_snappy_large_payload(self):
        if platform.python_implementation() == 'PyPy':
            pytest.skip('PyPy fails to compress large messages with Snappy')
        payload = (b'').join([uuid4().bytes for i in range(10)])
        c = compression.encode_snappy(payload)
        self.assertEqual(compression.decode_snappy(c), payload)

    def test_lz4(self):
        encoded = compression.encode_lz4(self.text)
        self.assertNotEqual(self.text, encoded)
        decoded = compression.decode_lz4(encoded)
        self.assertEqual(self.text, decoded)

    def test_lz4f(self):
        if platform.python_implementation() == 'PyPy':
            pytest.skip('lz4f is currently unsupported with PyPy')
        encoded = lz4f.compressFrame(self.text)
        self.assertNotEqual(self.text, encoded)
        decoded = compression.decode_lz4f(encoded)
        self.assertEqual(self.text, decoded)

    def test_lz4_old_kafka(self):
        encoded = compression.encode_lz4_old_kafka(self.text)
        self.assertNotEqual(self.text, encoded)
        decoded = compression.decode_lz4_old_kafka(encoded)
        self.assertEqual(self.text, decoded)


if __name__ == '__main__':
    unittest2.main()