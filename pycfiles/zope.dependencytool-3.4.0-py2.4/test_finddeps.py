# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zope/dependencytool/tests/test_finddeps.py
# Compiled at: 2007-09-21 15:26:02
"""Tests for zope.dependencytool.finddeps.

$Id: test_finddeps.py 27164 2004-08-17 11:16:39Z hdima $
"""
import unittest
from zope.dependencytool import finddeps

class HelperFunctionTestCase(unittest.TestCase):
    __module__ = __name__

    def test_makeDottedName(self):
        self.assertEqual(finddeps.makeDottedName(__file__), __name__)


def test_suite():
    return unittest.makeSuite(HelperFunctionTestCase)