# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_encode_raw.py
# Compiled at: 2016-08-01 02:33:02
# Size of source mod 2**32: 471 bytes
import unittest
from pyqart.qr.data.raw import Raw

class TestRaw(unittest.TestCase):

    def test_raw(self):
        raw = Raw('Hello, world!', 8)
        self.assertEqual(raw.output.as_string, '01000000110101001000' + '01100101' + '01101100' + '01101100' + '01101111' + '00101100' + '00100000' + '01110111' + '01101111' + '01110010' + '01101100' + '01100100' + '00100001')