# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_simplejson/tests/test_scanstring.py
# Compiled at: 2011-01-13 01:48:00
import sys, decimal
from unittest import TestCase
import simplejson as json, simplejson.decoder

class TestScanString(TestCase):

    def test_py_scanstring(self):
        self._test_scanstring(simplejson.decoder.py_scanstring)

    def test_c_scanstring(self):
        if not simplejson.decoder.c_scanstring:
            return
        self._test_scanstring(simplejson.decoder.c_scanstring)

    def _test_scanstring(self, scanstring):
        self.assertEquals(scanstring('"z\\ud834\\udd20x"', 1, None, True), ('z𝄠x',
                                                                            16))
        if sys.maxunicode == 65535:
            self.assertEquals(scanstring('"z𝄠x"', 1, None, True), ('z𝄠x', 6))
        else:
            self.assertEquals(scanstring('"z𝄠x"', 1, None, True), ('z𝄠x', 5))
        self.assertEquals(scanstring('"\\u007b"', 1, None, True), ('{', 8))
        self.assertEquals(scanstring('"A JSON payload should be an object or array, not a string."', 1, None, True), ('A JSON payload should be an object or array, not a string.',
                                                                                                                      60))
        self.assertEquals(scanstring('["Unclosed array"', 2, None, True), ('Unclosed array',
                                                                           17))
        self.assertEquals(scanstring('["extra comma",]', 2, None, True), ('extra comma',
                                                                          14))
        self.assertEquals(scanstring('["double extra comma",,]', 2, None, True), ('double extra comma',
                                                                                  21))
        self.assertEquals(scanstring('["Comma after the close"],', 2, None, True), ('Comma after the close',
                                                                                    24))
        self.assertEquals(scanstring('["Extra close"]]', 2, None, True), ('Extra close',
                                                                          14))
        self.assertEquals(scanstring('{"Extra comma": true,}', 2, None, True), ('Extra comma',
                                                                                14))
        self.assertEquals(scanstring('{"Extra value after close": true} "misplaced quoted value"', 2, None, True), ('Extra value after close',
                                                                                                                    26))
        self.assertEquals(scanstring('{"Illegal expression": 1 + 2}', 2, None, True), ('Illegal expression',
                                                                                       21))
        self.assertEquals(scanstring('{"Illegal invocation": alert()}', 2, None, True), ('Illegal invocation',
                                                                                         21))
        self.assertEquals(scanstring('{"Numbers cannot have leading zeroes": 013}', 2, None, True), ('Numbers cannot have leading zeroes',
                                                                                                     37))
        self.assertEquals(scanstring('{"Numbers cannot be hex": 0x14}', 2, None, True), ('Numbers cannot be hex',
                                                                                         24))
        self.assertEquals(scanstring('[[[[[[[[[[[[[[[[[[[["Too deep"]]]]]]]]]]]]]]]]]]]]', 21, None, True), ('Too deep',
                                                                                                             30))
        self.assertEquals(scanstring('{"Missing colon" null}', 2, None, True), ('Missing colon',
                                                                                16))
        self.assertEquals(scanstring('{"Double colon":: null}', 2, None, True), ('Double colon',
                                                                                 15))
        self.assertEquals(scanstring('{"Comma instead of colon", null}', 2, None, True), ('Comma instead of colon',
                                                                                          25))
        self.assertEquals(scanstring('["Colon instead of comma": false]', 2, None, True), ('Colon instead of comma',
                                                                                           25))
        self.assertEquals(scanstring('["Bad value", truth]', 2, None, True), ('Bad value',
                                                                              12))
        return

    def test_issue3623(self):
        self.assertRaises(ValueError, json.decoder.scanstring, 'xxx', 1, 'xxx')
        self.assertRaises(UnicodeDecodeError, json.encoder.encode_basestring_ascii, b'xx\xff')