# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/test_agi_bitfield.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 4550 bytes
from __future__ import print_function, with_statement, division, absolute_import
import io, logging, unittest
from struct import pack
import numpy as np
from fabio.compression import agi_bitfield
logger = logging.getLogger(__name__)

class TestUtil(unittest.TestCase):

    def test_get_fieldsize(self):
        test_cases = [
         (
          np.zeros(8, dtype='int32'), 1),
         (
          np.array([1024] * 8, dtype='int32'), 8),
         (
          np.arange(0, 7, dtype='int32'), 4),
         (
          np.array([-1, -2, 2, 1] * 2, dtype='int32'), 3)]
        for array, result in test_cases:
            fs = agi_bitfield.get_fieldsize(array)
            self.assertEqual(result, fs)

    def test_compress_decode_field_overflow(self):
        data = np.array([1, 2, 3, 4, 255, 40000, -4, 2], dtype='int32')
        fs = agi_bitfield.get_fieldsize(data)
        oft = io.BytesIO()
        cf = agi_bitfield.compress_field(data, fs, oft)
        self.assertEqual(pack('h', 255) + pack('i', 40000), oft.getvalue())
        mask_ = agi_bitfield.mask(fs)
        dec = agi_bitfield.decode_field(cf)
        self.assertEqual([128, 129, 130, 131, 254 & mask_, 255 & mask_, 123, 129], dec)

    def test_compress_decompress_field_small(self):
        data = np.array([1, 0] * 4, dtype='int32')
        fs = agi_bitfield.get_fieldsize(data)
        oft = io.BytesIO()
        cf = agi_bitfield.compress_field(data, fs, oft)
        self.assertEqual(b'', oft.getvalue())
        conv_ = agi_bitfield.conv(fs)
        dec = agi_bitfield.decode_field(cf[:fs])
        self.assertEqual([1 + conv_, 0 + conv_] * 4, dec)

    def test_full_compress_decompress_field(self):
        data = np.array([1, 2, 3, 4, 255, -40000, -4, 2], dtype='int32')
        fs = agi_bitfield.get_fieldsize(data)
        oft = io.BytesIO()
        cf = agi_bitfield.compress_field(data, fs, oft)
        oft = io.BytesIO(oft.getvalue())
        field = agi_bitfield.decode_field(cf[:fs])
        agi_bitfield.undo_escapes(field, fs, oft)
        self.assertEqual(list(data), field)

    def test_mask_conv(self):
        mask_cases = [
         (1, 1),
         (4, 15),
         (8, 255)]
        for len, msk in mask_cases:
            self.assertEqual(msk, agi_bitfield.mask(len))

        conv_cases = [(1, 0),
         (4, 7),
         (8, 127)]
        for len, cnv in conv_cases:
            self.assertEqual(cnv, agi_bitfield.conv(len))


class TestRow(unittest.TestCase):

    def test_compress_row_zero(self):
        data = np.zeros(256, dtype='int32')
        buffer = io.BytesIO()
        agi_bitfield.compress_row(data, buffer)
        buffer.seek(0)
        decompressed = agi_bitfield.decompress_row(buffer, 256)
        decompressed = np.array(decompressed, dtype='int32').cumsum()
        self.assertTrue(np.array_equal(decompressed, data))

    def test_compress_row_small(self):
        data = np.random.randint(0, 5, 256, dtype='int32')
        buffer = io.BytesIO()
        agi_bitfield.compress_row(data, buffer)
        buffer.seek(0)
        decompressed = agi_bitfield.decompress_row(buffer, 256)
        decompressed = np.array(decompressed, dtype='int32').cumsum()
        self.assertTrue(np.array_equal(decompressed, data))

    def compress_row_overflows(self):
        data = np.random.randint(-255, 255, 256, dtype='int32')
        buffer = io.BytesIO()
        agi_bitfield.compress_row(data, buffer)
        buffer.seek(0)
        decompressed = agi_bitfield.decompress_row(buffer, 256)
        decompressed = np.array(decompressed, dtype='int32').cumsum()
        self.assertTrue(np.array_equal(decompressed, data))


class TestCompression(unittest.TestCase):

    def test_full_rand(self):
        data = np.random.randint(-255, 255, (256, 256))
        compressed = agi_bitfield.compress(data)
        uncompressed = agi_bitfield.decompress(compressed, data.shape)
        self.assertTrue(np.array_equal(data, uncompressed))


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestUtil))
    testsuite.addTest(loadTests(TestRow))
    testsuite.addTest(loadTests(TestCompression))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())