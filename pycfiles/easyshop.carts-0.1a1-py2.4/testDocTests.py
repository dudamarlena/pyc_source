# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/carts/tests/testDocTests.py
# Compiled at: 2008-06-20 09:34:52
from Testing.ZopeTestCase import FunctionalDocFileSuite
from zope.testing import doctest
from unittest import TestSuite
from os.path import join, split, abspath, dirname
from os import walk
from re import compile
from sys import argv
from easyshop.carts.tests.base import EasyShopCartsFunctionalTestCase
if '-t' in argv:
    pattern = compile('.*\\.(txt|rst)$')
else:
    pattern = compile('(^test.*|/test[^/]*)\\.(txt|rst)$')
tests = []
docs = join(abspath(dirname(__file__)), '../docs/')
for (path, dirs, files) in walk(docs, topdown=False):
    for name in files:
        relative = join(path, name)[len(docs):]
        if '.svn' not in split(path) and pattern.search(relative):
            tests.append(relative)

def test_suite():
    suite = TestSuite()
    for test in tests:
        suite.addTest(FunctionalDocFileSuite(test, optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE, package='easyshop.carts.docs', test_class=EasyShopCartsFunctionalTestCase))

    return suite