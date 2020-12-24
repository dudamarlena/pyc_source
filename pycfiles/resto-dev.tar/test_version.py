# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rafael/code/resto/tests/test_version.py
# Compiled at: 2014-06-05 22:50:37
import unittest, resto
from pkg_resources import parse_version

class TestVersion(unittest.TestCase):
    """Checks package `__version__` access."""

    def test_version_access(self):
        """Resto package version access."""
        this = parse_version(resto.__version__)
        dev = parse_version('dev')
        self.assertTrue(this >= dev)