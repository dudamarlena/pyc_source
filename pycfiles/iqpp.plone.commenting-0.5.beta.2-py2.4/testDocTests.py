# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/tests/testDocTests.py
# Compiled at: 2007-10-07 06:52:18
from Testing.ZopeTestCase import FunctionalDocFileSuite
from Globals import package_home
from base import CommentingFunctionalTestCase
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
        suite.addTest(FunctionalDocFileSuite(test, package='iqpp.plone.commenting.docs', test_class=CommentingFunctionalTestCase))

    return suite