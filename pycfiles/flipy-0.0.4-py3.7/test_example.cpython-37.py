# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/test_example.py
# Compiled at: 2020-03-04 21:41:25
# Size of source mod 2**32: 148 bytes
import flipy, unittest

class TestExample(unittest.TestCase):

    def test_example(self):
        self.assertIsInstance(flipy.version, str)