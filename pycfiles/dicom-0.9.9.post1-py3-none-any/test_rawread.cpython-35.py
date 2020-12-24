# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\test\test_rawread.py
# Compiled at: 2017-01-26 21:10:19
# Size of source mod 2**32: 14355 bytes
"""unittest tests for dicom.filereader module -- simple raw data elements"""
from io import BytesIO
import unittest
from dicom.filereader import data_element_generator
from dicom.values import convert_value
from dicom.sequence import Sequence
from dicom.util.hexutil import hex2bytes

class RawReaderExplVRTests(unittest.TestCase):

    def testExplVRLittleEndianLongLength(self):
        """Raw read: Explicit VR Little Endian long length......................"""
        infile = BytesIO(hex2bytes('02 00 01 00 4f 42 00 00 02 00 00 00 00 01'))
        expected = ((2, 1), 'OB', 2, b'\x00\x01', 12, False, True)
        de_gen = data_element_generator(infile, is_implicit_VR=False, is_little_endian=True)
        got = next(de_gen)
        msg_loc = "in read of Explicit VR='OB' data element (long length format)"
        self.assertEqual(got, expected, 'Expected: %r, got %r in %s' % (expected, got, msg_loc))

    def testExplVRLittleEndianShortLength(self):
        """Raw read: Explicit VR Little Endian short length....................."""
        infile = BytesIO(hex2bytes('08 00 2a 21 49 53 02 00 31 20'))
        expected = ((8, 8490), 'IS', 2, b'1 ', 8, False, True)
        de_gen = data_element_generator(infile, is_implicit_VR=False, is_little_endian=True)
        got = next(de_gen)
        msg_loc = "in read of Explicit VR='IS' data element (short length format)"
        self.assertEqual(got, expected, 'Expected: %r, got %r in %s' % (expected, got, msg_loc))

    def testExplVRLittleEndianUndefLength(self):
        """Raw read: Expl VR Little Endian with undefined length................"""
        hexstr1 = 'e0 7f 10 00 4f 42 00 00 ff ff ff ff'
        hexstr2 = ' 41 42 43 44 45 46 47 48 49 4a'
        hexstr3 = ' fe ff dd e0 00 00 00 00'
        hexstr = hexstr1 + hexstr2 + hexstr3
        infile = BytesIO(hex2bytes(hexstr))
        expected = ((32736, 16), 'OB', 4294967295, b'ABCDEFGHIJ', 12, False, True)
        de_gen = data_element_generator(infile, is_implicit_VR=False, is_little_endian=True)
        got = next(de_gen)
        msg_loc = "in read of undefined length Explicit VR ='OB' short value)"
        self.assertEqual(got, expected, 'Expected: %r, got %r in %s' % (expected, got, msg_loc))
        for multiplier in (116, 117, 118, 120):
            multiplier = 116
            hexstr2b = hexstr2 + ' 00' * multiplier
            hexstr = hexstr1 + hexstr2b + hexstr3
            infile = BytesIO(hex2bytes(hexstr))
            expected = len('ABCDEFGHIJ' + '\x00' * multiplier)
            de_gen = data_element_generator(infile, is_implicit_VR=False, is_little_endian=True)
            got = next(de_gen)
            got_len = len(got.value)
            msg_loc = "in read of undefined length Explicit VR ='OB' with 'multiplier' %d" % multiplier
            self.assertEqual(expected, got_len, 'Expected value length %d, got %d in %s' % (expected, got_len, msg_loc))
            msg = 'Unexpected value start with multiplier %d on Expl VR undefined length' % multiplier
            self.assertTrue(got.value.startswith(b'ABCDEFGHIJ\x00'), msg)


class RawReaderImplVRTests(unittest.TestCase):

    def testImplVRLittleEndian(self):
        """Raw read: Implicit VR Little Endian.................................."""
        infile = BytesIO(hex2bytes('08 00 2a 21 02 00 00 00 31 20'))
        expected = ((8, 8490), None, 2, b'1 ', 8, True, True)
        de_gen = data_element_generator(infile, is_implicit_VR=True, is_little_endian=True)
        got = next(de_gen)
        msg_loc = "in read of Implicit VR='IS' data element (short length format)"
        self.assertEqual(got, expected, 'Expected: %r, got %r in %s' % (expected, got, msg_loc))

    def testImplVRLittleEndianUndefLength(self):
        """Raw read: Impl VR Little Endian with undefined length................"""
        hexstr1 = 'e0 7f 10 00 ff ff ff ff'
        hexstr2 = ' 41 42 43 44 45 46 47 48 49 4a'
        hexstr3 = ' fe ff dd e0 00 00 00 00'
        hexstr = hexstr1 + hexstr2 + hexstr3
        infile = BytesIO(hex2bytes(hexstr))
        expected = ((32736, 16), 'OB or OW', 4294967295, b'ABCDEFGHIJ', 8, True, True)
        de_gen = data_element_generator(infile, is_implicit_VR=True, is_little_endian=True)
        got = next(de_gen)
        msg_loc = "in read of undefined length Implicit VR ='OB' short value)"
        self.assertEqual(got, expected, 'Expected: %r, got %r in %s' % (expected, got, msg_loc))
        for multiplier in (116, 117, 118, 120):
            multiplier = 116
            hexstr2b = hexstr2 + ' 00' * multiplier
            hexstr = hexstr1 + hexstr2b + hexstr3
            infile = BytesIO(hex2bytes(hexstr))
            expected = len('ABCDEFGHIJ' + '\x00' * multiplier)
            de_gen = data_element_generator(infile, is_implicit_VR=True, is_little_endian=True)
            got = next(de_gen)
            got_len = len(got.value)
            msg_loc = "in read of undefined length Implicit VR with 'multiplier' %d" % multiplier
            self.assertEqual(expected, got_len, 'Expected value length %d, got %d in %s' % (expected, got_len, msg_loc))
            msg = 'Unexpected value start with multiplier %d on Implicit VR undefined length' % multiplier
            self.assertTrue(got.value.startswith(b'ABCDEFGHIJ\x00'), msg)


class RawSequenceTests(unittest.TestCase):

    def testEmptyItem(self):
        """Read sequence with a single empty item..............................."""
        hexstr = '08 00 32 10 08 00 00 00 fe ff 00 e0 00 00 00 00' + ' 08 00 3e 10 0c 00 00 00 52 20 41 44 44 20 56 49 45 57 53 20'
        fp = BytesIO(hex2bytes(hexstr))
        gen = data_element_generator(fp, is_implicit_VR=True, is_little_endian=True)
        raw_seq = next(gen)
        seq = convert_value('SQ', raw_seq)
        self.assertTrue(isinstance(seq, Sequence), 'Did not get Sequence, got type {0}'.format(str(type(seq))))
        self.assertTrue(len(seq) == 1, 'Expected Sequence with single (empty) item, got {0:d} item(s)'.format(len(seq)))
        self.assertTrue(len(seq[0]) == 0, 'Expected the sequence item (dataset) to be empty')
        elem2 = next(gen)
        self.assertEqual(elem2.tag, 528446, 'Expected a data element after empty sequence item')

    def testImplVRLittleEndian_ExplicitLengthSeq(self):
        """Raw read: ImplVR Little Endian SQ with explicit lengths.............."""
        hexstr = '0a 30 B0 00 40 00 00 00 fe ff 00 e0 18 00 00 00 0a 30 c0 00 02 00 00 00 31 20 0a 30 c2 00 06 00 00 00 42 65 61 6d 20 31 fe ff 00 e0 18 00 00 00 0a 30 c0 00 02 00 00 00 32 20 0a 30 c2 00 06 00 00 00 42 65 61 6d 20 32'
        infile = BytesIO(hex2bytes(hexstr))
        de_gen = data_element_generator(infile, is_implicit_VR=True, is_little_endian=True)
        raw_seq = next(de_gen)
        seq = convert_value('SQ', raw_seq)
        got = seq[0].BeamNumber
        self.assertTrue(got == 1, 'Expected Beam Number 1, got {0!r}'.format(got))
        got = seq[1].BeamName
        self.assertTrue(got == 'Beam 2', "Expected Beam Name 'Beam 2', got {0:s}".format(got))

    def testImplVRBigEndian_ExplicitLengthSeq(self):
        """Raw read: ImplVR BigEndian SQ with explicit lengths.................."""
        hexstr = '30 0a 00 B0 00 00 00 40 ff fe e0 00 00 00 00 18 30 0a 00 c0 00 00 00 02 31 20 30 0a 00 c2 00 00 00 06 42 65 61 6d 20 31 ff fe e0 00 00 00 00 18 30 0a 00 c0 00 00 00 02 32 20 30 0a 00 c2 00 00 00 06 42 65 61 6d 20 32'
        infile = BytesIO(hex2bytes(hexstr))
        de_gen = data_element_generator(infile, is_implicit_VR=True, is_little_endian=False)
        raw_seq = next(de_gen)
        seq = convert_value('SQ', raw_seq)
        got = seq[0].BeamNumber
        self.assertTrue(got == 1, 'Expected Beam Number 1, got {0!r}'.format(got))
        got = seq[1].BeamName
        self.assertTrue(got == 'Beam 2', "Expected Beam Name 'Beam 2', got {0:s}".format(got))

    def testExplVRBigEndian_UndefinedLengthSeq(self):
        """Raw read: ExplVR BigEndian Undefined Length SQ......................."""
        hexstr = '30 0a 00 B0 53 51 00 00 ff ff ff ff ff fe e0 00 00 00 00 18 30 0a 00 c0 49 53 00 02 31 20 30 0a 00 c2 4c 4F 00 06 42 65 61 6d 20 31 ff fe e0 00 00 00 00 18 30 0a 00 c0 49 53 00 02 32 20 30 0a 00 c2 4C 4F 00 06 42 65 61 6d 20 32 ff fe E0 dd 00 00 00 00'
        infile = BytesIO(hex2bytes(hexstr))
        de_gen = data_element_generator(infile, is_implicit_VR=False, is_little_endian=False)
        seq = next(de_gen)
        got = seq[0].BeamNumber
        self.assertTrue(got == 1, 'Expected Beam Number 1, got {0!r}'.format(got))
        got = seq[1].BeamName
        self.assertTrue(got == 'Beam 2', "Expected Beam Name 'Beam 2', got {0:s}".format(got))


if __name__ == '__main__':
    unittest.main()