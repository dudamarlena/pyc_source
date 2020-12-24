# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/bytes/tests/test_bytes_tool.py
# Compiled at: 2020-01-01 15:08:00
# Size of source mod 2**32: 264 bytes
from unittest import TestCase
from foxylib.tools.bytes.bytes_tool import BytesTool

class TestBytesTool(TestCase):

    def test_01(self):
        bytes = b'abcde'
        hyp = BytesTool.bytes2utf8(bytes)
        ref = 'abcde'
        self.assertEqual(hyp, ref)