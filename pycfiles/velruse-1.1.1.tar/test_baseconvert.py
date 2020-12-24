# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/michael/work/oss/velruse/tests/units/test_app/test_baseconvert.py
# Compiled at: 2013-06-08 23:24:54
import unittest

class TestBaseEncoding(unittest.TestCase):

    def test_encode(self):
        from velruse.app.baseconvert import base_encode
        self.assertEqual(base_encode(42), 'L')
        self.assertEqual(base_encode(425242), '4rBC')
        self.assertEqual(base_encode(0), '2')

    def test_bad_encode(self):
        from velruse.app.baseconvert import base_encode
        self.assertRaises(TypeError, base_encode, 'fred')

    def test_decode(self):
        from velruse.app.baseconvert import base_decode
        self.assertEqual(base_decode('L'), 42)
        self.assertEqual(base_decode('4rBC'), 425242)
        self.assertEqual(base_decode('2'), 0)

    def test_bad_decode(self):
        from velruse.app.baseconvert import base_decode
        self.assertRaises(ValueError, base_decode, '381')