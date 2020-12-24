# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mindey/Projects/Development/subfiles/tests/commands/test_hello.py
# Compiled at: 2018-10-30 20:55:29
# Size of source mod 2**32: 362 bytes
"""Tests for our `subfiles hello` subcommand."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from subprocess import PIPE, Popen as popen
from unittest import TestCase

class TestHello(TestCase):

    def test_returns_multiple_lines(self):
        output = popen(['ftypes', 'schema'], stdout=PIPE).communicate()[0]
        lines = str(output, 'utf-8').split('\n')
        self.assertTrue(len(lines) == 1)