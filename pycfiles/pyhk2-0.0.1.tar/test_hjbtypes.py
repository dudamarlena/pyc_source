# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/hjb/test/test_hjbtypes.py
# Compiled at: 2006-06-04 03:22:01
__doc__ = '\nTest Cases for the encode and decode methods in hjbmessages.py\n'
import unittest
from unittest import makeSuite as make_suite
from hjb.hjbtypes import hjbencode, hjbdecode
__docformat__ = 'restructuredtext en'
test_values = {'float': {'ok-untidy': ['(float 1.00)', '(float 0.3457)', '(float 7.7e11)', '(float\t\t9.999)', '(float\t\t\t11000.0f)', '(float      -15.85e-12)'], 'ok-pristine': ['(float 1)', '(float 0.3457)', '(float 7.7E+011)', '(float 9.999)', '(float 11000)', '(float -1.585E-011)'], 'not-ok': ['anything', 'boolean 1)', 'btit 3', '(short 5)', '(int 7)'], 'decoded': [(1.0, 'float'), (0.3457, 'float'), (770000000000.0, 'float'), (9.999, 'float'), (11000.0, 'float'), (-1.585e-11, 'float')]}, 'double': {'ok-untidy': ['(double 1.00)', '(double 0.3457)', '(double 7.7e11)', '(double\t\t9.999)', '(double\t\t\t11000.0f)', '(double      -15.85e-12)'], 'ok-pristine': ['(double 1)', '(double 0.3457)', '(double 7.7E+011)', '(double 9.999)', '(double 11000)', '(double -1.585E-011)'], 'not-ok': ['anything', 'boolean 1)', 'btit 3', '(short 5)', '(int 7)'], 'decoded': [(1.0, 'double'), (0.3457, 'double'), (770000000000.0, 'double'), (9.999, 'double'), (11000.0, 'double'), (-1.585e-11, 'double')]}, 'char': {'ok-untidy': ['(char \\u61)', '(char \\u0AA)', '(char    \\u0009)', '(char  \\u2620)', '(char   \\u18FF)'], 'ok-pristine': ['(char \\u0061)', '(char \\u00AA)', '(char \\u0009)', '(char \\u2620)', '(char \\u18FF)'], 'not-ok': ['anything', 'boolean 1)', 'btit 3', '(short 5)', '(int 7)'], 'decoded': [('a', 'char'), ('ª', 'char'), ('\t', 'char'), ('☠', 'char'), ('\u18ff', 'char')]}, 'base64': {'ok-untidy': ['(base64 VEVTVA==)', '(base64 QU5PVEhFUlRFU1Q=)', '(base64\tWUVUQU5PVEhFUlRFU1Q=)', '(base64\t\tRE9FU0FOWU9ORUZBTkNZQU5PVEhFUlRFU1Q=)'], 'ok-pristine': ['(base64 VEVTVA==)', '(base64 QU5PVEhFUlRFU1Q=)', '(base64 WUVUQU5PVEhFUlRFU1Q=)', '(base64 RE9FU0FOWU9ORUZBTkNZQU5PVEhFUlRFU1Q=)'], 'not-ok': ['anything', 'base64 1)', 'btit 3', '(short 5)'], 'decoded': [('TEST', 'byte_array'), ('ANOTHERTEST', 'byte_array'), ('YETANOTHERTEST', 'byte_array'), ('DOESANYONEFANCYANOTHERTEST', 'byte_array')]}, 'boolean': {'ok-untidy': ['(boolean true)', '(boolean True)', '(boolean   F)', '(boolean\t\tFalse)', '(boolean t)', '(boolean 1)'], 'ok-pristine': ['(boolean True)', '(boolean True)', '(boolean False)', '(boolean False)', '(boolean False)', '(boolean False)'], 'not-ok': ['anything', 'boolean 1)', 'btit 3', '(short 5)', '(int 7)', '(long 9)'], 'decoded': [(True, 'boolean'), (True, 'boolean'), (False, 'boolean'), (False, 'boolean'), (False, 'boolean'), (False, 'boolean')]}, 'byte': {'ok-untidy': ['(byte 1)', '(byte 3)', '(byte   7)', '(byte\t\t9)', '(byte 11)', '(byte -1)'], 'ok-pristine': ['(byte 1)', '(byte 3)', '(byte 7)', '(byte 9)', '(byte 11)', '(byte -1)'], 'not-ok': ['anything', 'byte 1)', 'btit 3', '(short 5)', '(int 7)', '(long 9)'], 'decoded': [(1, 'byte'), (3, 'byte'), (7, 'byte'), (9, 'byte'), (11, 'byte'), (-1, 'byte')]}, 'short': {'ok-untidy': ['(short 20)', '(short 347)', '(short 1978)', '(short\t\t9)', '(short -678)', '(short -20000)'], 'ok-pristine': ['(short 20)', '(short 347)', '(short 1978)', '(short 9)', '(short -678)', '(short -20000)'], 'not-ok': ['anything', 'byte 1)', 'btit 3', '(byte 5)', '(int 7)', '(long 9)'], 'decoded': [(20, 'short'), (347, 'short'), (1978, 'short'), (9, 'short'), (-678, 'short'), (-20000, 'short')]}, 'int': {'ok-untidy': ['(int 15)', '(int 347)', '(int 1978)', '(int\t\t9)', '(int +64444)', '(int -200000)'], 'ok-pristine': ['(int 15)', '(int 347)', '(int 1978)', '(int 9)', '(int 64444)', '(int -200000)'], 'not-ok': ['anything', 'byte 1)', 'btit 3', '(byte 5)', '(short 7)', '(long 9)'], 'decoded': [(15, 'int'), (347, 'int'), (1978, 'int'), (9, 'int'), (64444, 'int'), (-200000, 'int')]}, 'long': {'ok-untidy': ['(long 15)', '(long 347)', '(long 1978)', '(long\t\t9)', '(long +644444)', '(long -20000000)'], 'ok-pristine': ['(long 15)', '(long 347)', '(long 1978)', '(long 9)', '(long 644444)', '(long -20000000)'], 'not-ok': ['anything', 'byte 1)', 'btit 3', '(byte 5)', '(short 7)', '(double 9)'], 'decoded': [(15, 'long'), (347, 'long'), (1978, 'long'), (9, 'long'), (644444, 'long'), (-20000000, 'long')]}}

class CodecTest(unittest.TestCase):
    __module__ = __name__

    def _decode_test(self, test_values):
        encoded = test_values['ok-untidy']
        wrong = test_values['not-ok']
        decoded = [ v[0] for v in test_values['decoded'] ]
        [ self.assertEquals(d, hjbdecode(e)) for (d, e) in zip(decoded, encoded) ]
        [ self.assertNotEquals(d, hjbdecode(w)) for (d, w) in zip(decoded, wrong) ]

    def _encode_test(self, test_values):
        pristine_encoded = test_values['ok-pristine']
        to_be_encoded = test_values['decoded']
        [ self.assertEquals(e, hjbencode(d[1], d[0])) for (e, d) in zip(pristine_encoded, to_be_encoded) ]


class ByteCodecTest(CodecTest):
    __module__ = __name__

    def test_values_are_decoded_correctly(self):
        self._decode_test(test_values['byte'])

    def test_values_are_encoded_correctly(self):
        self._encode_test(test_values['byte'])


class ShortCodecTest(CodecTest):
    __module__ = __name__

    def test_values_are_decoded_correctly(self):
        self._decode_test(test_values['short'])

    def test_values_are_encoded_correctly(self):
        self._encode_test(test_values['short'])


class IntCodecTest(CodecTest):
    __module__ = __name__

    def test_values_are_decoded_correctly(self):
        self._decode_test(test_values['int'])

    def test_values_are_encoded_correctly(self):
        self._encode_test(test_values['int'])


class LongCodecTest(CodecTest):
    __module__ = __name__

    def test_values_are_decoded_correctly(self):
        self._decode_test(test_values['long'])

    def test_values_are_encoded_correctly(self):
        self._encode_test(test_values['long'])


class BooleanCodecTest(CodecTest):
    __module__ = __name__

    def test_values_are_decoded_correctly(self):
        self._decode_test(test_values['boolean'])

    def test_values_are_encoded_correctly(self):
        self._encode_test(test_values['boolean'])


class ByteArrayCodecTest(CodecTest):
    __module__ = __name__

    def test_values_are_decoded_correctly(self):
        self._decode_test(test_values['base64'])

    def test_values_are_encoded_correctly(self):
        self._encode_test(test_values['base64'])


class CharCodecTest(CodecTest):
    __module__ = __name__

    def test_values_are_decoded_correctly(self):
        self._decode_test(test_values['char'])

    def test_values_are_encoded_correctly(self):
        self._encode_test(test_values['char'])


class FloatCodecTest(CodecTest):
    __module__ = __name__

    def test_values_are_decoded_correctly(self):
        self._decode_test(test_values['float'])

    def test_values_are_encoded_correctly(self):
        self._encode_test(test_values['float'])


class DoubleCodecTest(CodecTest):
    __module__ = __name__

    def test_values_are_decoded_correctly(self):
        self._decode_test(test_values['double'])

    def test_values_are_encoded_correctly(self):
        self._encode_test(test_values['double'])


def test_suite():
    return unittest.TestSuite(tuple([ make_suite(s) for s in [ByteCodecTest, ShortCodecTest, IntCodecTest, LongCodecTest, BooleanCodecTest, ByteArrayCodecTest, CharCodecTest, FloatCodecTest, DoubleCodecTest] ]))


def main():
    unittest.TextTestRunner(verbosity=2).run(test_suite())


if __name__ == '__main__':
    main()