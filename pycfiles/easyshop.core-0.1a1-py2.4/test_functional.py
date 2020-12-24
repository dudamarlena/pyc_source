# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_functional.py
# Compiled at: 2008-06-20 09:37:19
from Testing.ZopeTestCase import FunctionalDocFileSuite
from Globals import package_home
from base import EasyShopFunctionalTestCase
from unittest import TestSuite
from os.path import join, split
from os import walk
from re import compile
from sys import argv
if '-t' in argv:
    pattern = compile('.*\\.(txt|rst)$')
else:
    pattern = compile('(^test.*|/test[^/]*)\\.(txt|rst)$')
tests = []
docs = join(package_home(globals()), '../docs/')
for (path, dirs, files) in walk(docs, topdown=False):
    for name in files:
        relative = join(path, name)[len(docs):]
        if '.svn' not in split(path) and pattern.search(relative):
            tests.append(relative)

def test_suite():
    suite = TestSuite()
    for test in tests:
        suite.addTest(FunctionalDocFileSuite(test, package='easyshop.shop.docs', test_class=EasyShopFunctionalTestCase))

    return suite