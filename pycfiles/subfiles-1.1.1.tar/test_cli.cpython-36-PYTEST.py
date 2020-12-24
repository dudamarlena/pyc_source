# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mindey/Projects/Development/subfiles/tests/test_cli.py
# Compiled at: 2018-10-30 20:55:29
# Size of source mod 2**32: 727 bytes
"""Tests for our main subfiles module."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from subprocess import PIPE, Popen as popen
from unittest import TestCase
from subfiles import __version__ as VERSION

class TestHelp(TestCase):

    def test_returns_usage_information(self):
        output = popen(['ftypes', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue(bytes('Usage:', 'utf-8') in output)
        output = popen(['ftypes', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue(bytes('Usage:', 'utf-8') in output)


class TestVersion(TestCase):

    def test_returns_version_information(self):
        output = popen(['ftypes', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), bytes(VERSION, 'utf-8'))