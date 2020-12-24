# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_encode_raw.py
# Compiled at: 2016-08-01 02:33:02
# Size of source mod 2**32: 471 bytes
import unittest
from pyqart.qr.data.raw import Raw

class TestRaw(unittest.TestCase):

    def test_raw(self):
        raw = Raw(b'Hello, world!', 8)
        self.assertEqual(raw.output.as_string, '01000000110101001000' + '01100101' + '01101100' + '01101100' + '01101111' + '00101100' + '00100000' + '01110111' + '01101111' + '01110010' + '01101100' + '01100100' + '00100001')