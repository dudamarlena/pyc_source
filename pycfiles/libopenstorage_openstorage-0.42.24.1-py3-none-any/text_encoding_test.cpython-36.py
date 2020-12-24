# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/internal/text_encoding_test.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 2903 bytes
"""Tests for google.protobuf.text_encoding."""
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from google.protobuf import text_encoding
TEST_VALUES = [
 ('foo\\rbar\\nbaz\\t', 'foo\\rbar\\nbaz\\t', b'foo\rbar\nbaz\t'),
 ('\\\'full of \\"sound\\" and \\"fury\\"\\\'', '\\\'full of \\"sound\\" and \\"fury\\"\\\'',
 b'\'full of "sound" and "fury"\''),
 ('signi\\\\fying\\\\ nothing\\\\', 'signi\\\\fying\\\\ nothing\\\\', b'signi\\fying\\ nothing\\'),
 ('\\010\\t\\n\\013\\014\\r', '\x08\\t\\n\x0b\x0c\\r', b'\x08\t\n\x0b\x0c\r')]

class TextEncodingTestCase(unittest.TestCase):

    def testCEscape(self):
        for escaped, escaped_utf8, unescaped in TEST_VALUES:
            self.assertEqual(escaped, text_encoding.CEscape(unescaped, as_utf8=False))
            self.assertEqual(escaped_utf8, text_encoding.CEscape(unescaped, as_utf8=True))

    def testCUnescape(self):
        for escaped, escaped_utf8, unescaped in TEST_VALUES:
            self.assertEqual(unescaped, text_encoding.CUnescape(escaped))
            self.assertEqual(unescaped, text_encoding.CUnescape(escaped_utf8))


if __name__ == '__main__':
    unittest.main()