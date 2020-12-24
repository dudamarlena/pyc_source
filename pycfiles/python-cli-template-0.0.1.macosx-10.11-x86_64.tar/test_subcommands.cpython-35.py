# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sotetsuk/.pyenv/versions/3.5.1/lib/python3.5/site-packages/somecommand/tests/test_subcommands.py
# Compiled at: 2016-07-23 06:37:08
# Size of source mod 2**32: 237 bytes
import unittest
from somecommand.subcommands import foo, bar

class TestFooBar(unittest.TestCase):

    def test_foo(self):
        foo()
        self.assertTrue(True)

    def test_bar(self):
        bar()
        self.assertTrue(True)