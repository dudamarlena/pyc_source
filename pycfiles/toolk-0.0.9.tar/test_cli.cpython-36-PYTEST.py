# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/heinrich/Dropbox/Projects/toolk-cli/tests/test_cli.py
# Compiled at: 2017-07-17 16:37:55
# Size of source mod 2**32: 674 bytes
"""Tests for our main toolk CLI module."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from subprocess import PIPE, Popen as popen
from unittest import TestCase
from toolk import __version__ as VERSION

class TestHelp(TestCase):

    def test_returns_usage_information(self):
        output = popen(['toolk', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)
        output = popen(['toolk', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)


class TestVersion(TestCase):

    def test_returns_version_information(self):
        output = popen(['toolk', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), VERSION)