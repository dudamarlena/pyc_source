# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/heinrich/Dropbox/Projects/toolk-cli/tests/commands/test_hello.py
# Compiled at: 2017-07-17 16:38:59
# Size of source mod 2**32: 508 bytes
"""Tests for our `toolk hello` subcommand."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from subprocess import PIPE, Popen as popen
from unittest import TestCase

class TestHello(TestCase):

    def test_returns_multiple_lines(self):
        output = popen(['toolk', 'hello'], stdout=PIPE).communicate()[0]
        lines = output.split('\n')
        self.assertTrue(len(lines) != 1)

    def test_returns_hello_world(self):
        output = popen(['toolk', 'hello'], stdout=PIPE).communicate()[0]
        self.assertTrue('Hello, world!' in output)