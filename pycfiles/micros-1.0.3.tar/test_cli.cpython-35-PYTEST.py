# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/martijn/Projects/micros-cli/tests/test_cli.py
# Compiled at: 2017-03-21 06:04:08
# Size of source mod 2**32: 591 bytes
"""Tests for our main micros CLI module."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from subprocess import getoutput
from unittest import TestCase
from micros import __version__ as VERSION

class TestHelp(TestCase):

    def test_returns_usage_information(self):
        output = getoutput('micros -h')
        self.assertTrue('Usage:' in str(output))
        output = getoutput('micros --help')
        self.assertTrue('Usage:' in str(output))


class TestVersion(TestCase):

    def test_returns_version_information(self):
        output = getoutput('micros --version')
        self.assertEqual(str(output.strip()), VERSION)