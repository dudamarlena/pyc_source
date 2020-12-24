# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zope/dependencytool/tests/test_importfinder.py
# Compiled at: 2007-09-21 15:26:02
"""Tests for zope.dependencytool.importfinder.

$Id: test_importfinder.py 27164 2004-08-17 11:16:39Z hdima $
"""
import os, unittest
from zope.dependencytool import importfinder
here = os.path.dirname(__file__)
THIS_PACKAGE = __name__[:__name__.rfind('.')]

class ImportFinderTestCase(unittest.TestCase):
    __module__ = __name__

    def test_relative_imports(self):
        finder = importfinder.ImportFinder()
        path = os.path.join(here, 'sample.py')
        f = open(path, 'rU')
        try:
            finder.find_imports(f, path, THIS_PACKAGE)
        finally:
            f.close()
        imports = finder.get_imports()
        self.assertEqual(len(imports), 1)
        self.assertEqual(imports[0].name, '%s.pkg.module' % THIS_PACKAGE)

    def test_relative_imports_for_packages(self):
        finder = importfinder.ImportFinder(packages=True)
        path = os.path.join(here, 'sample.py')
        f = open(path, 'rU')
        try:
            finder.find_imports(f, path, THIS_PACKAGE)
        finally:
            f.close()
        imports = finder.get_imports()
        self.assertEqual(len(imports), 1)
        self.assertEqual(imports[0].name, '%s.pkg' % THIS_PACKAGE)

    def test_package_for_module(self):
        self.assertEqual(importfinder.package_for_module(__name__), THIS_PACKAGE)
        self.assertEqual(importfinder.package_for_module('os'), None)
        self.assertEqual(importfinder.package_for_module('distutils.sysconfig'), 'distutils')
        return

    def test_module_for_importable(self):
        clsname = __name__ + '.ImportFinderTestCase'
        self.assertEqual(importfinder.module_for_importable(clsname), __name__)
        self.assertEqual(importfinder.module_for_importable('os.path.isdir'), 'os.path')
        self.assertEqual(importfinder.module_for_importable(__name__), __name__)
        methodname = clsname + '.test_module_for_importable'
        self.assertEqual(importfinder.module_for_importable(methodname), __name__)


def test_suite():
    return unittest.makeSuite(ImportFinderTestCase)