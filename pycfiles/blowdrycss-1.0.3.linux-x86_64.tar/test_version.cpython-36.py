# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/unit_tests/test_version.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 561 bytes
from __future__ import absolute_import
from unittest import TestCase, main
import version
__author__ = 'chad nelson'
__project__ = 'blowdrycss'

class TestTiming(TestCase):

    def test_author(self):
        self.assertIsNotNone(version.__author__)

    def test_project(self):
        self.assertIsNotNone(version.__project__)

    def test_version(self):
        self.assertIsNotNone(version.__version__)

    def test_release(self):
        self.assertIsNotNone(version.__release__)


if __name__ == '__main__':
    main()