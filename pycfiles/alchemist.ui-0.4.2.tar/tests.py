# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/alchemist/traversal/tests.py
# Compiled at: 2008-09-24 15:09:06
import unittest, re
from zope.testing import doctest, renormalizing
from zope.app.testing import placelesssetup

def setUp(test):
    placelesssetup.setUp()


def tearDown(test):
    placelesssetup.tearDown


def test_suite():
    return unittest.TestSuite(doctest.DocFileSuite('readme.txt', setUp=setUp, tearDown=tearDown, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))