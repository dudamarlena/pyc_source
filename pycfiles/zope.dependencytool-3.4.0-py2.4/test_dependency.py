# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zope/dependencytool/tests/test_dependency.py
# Compiled at: 2007-09-21 15:26:02
"""Tests for zope.dependencytool.dependency.

$Id: test_dependency.py 27164 2004-08-17 11:16:39Z hdima $
"""
import unittest
from zope.dependencytool.dependency import Dependency

class DependencyTestCase(unittest.TestCase):
    __module__ = __name__

    def test_isSubPackageOf(self):
        d1 = Dependency('a.b.c', 'filename', 42)
        d2 = Dependency('a.b', 'filename', 42)
        d3 = Dependency('a.b.d', 'filename', 42)
        d4 = Dependency('a.b.c.d.e', 'filename', 42)
        self.assert_(d1.isSubPackageOf(d2))
        self.assert_(d4.isSubPackageOf(d1))
        self.assert_(d4.isSubPackageOf(d2))
        self.assert_(not d1.isSubPackageOf(d1))
        self.assert_(not d2.isSubPackageOf(d1))
        self.assert_(not d1.isSubPackageOf(d3))
        self.assert_(not d3.isSubPackageOf(d1))
        self.assert_(not d1.isSubPackageOf(d4))
        self.assert_(not d2.isSubPackageOf(d4))
        self.assert_(not d3.isSubPackageOf(d4))


def test_suite():
    return unittest.makeSuite(DependencyTestCase)