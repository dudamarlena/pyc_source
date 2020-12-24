# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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