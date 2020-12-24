# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sotetsuk/.pyenv/versions/3.5.1/lib/python3.5/site-packages/somecommand/tests/test_main.py
# Compiled at: 2016-07-23 07:39:42
# Size of source mod 2**32: 181 bytes
import unittest
from somecommand.main import helloworld, main

class TestMain(unittest.TestCase):

    def test_helloworld(self):
        helloworld()
        self.assertTrue(True)