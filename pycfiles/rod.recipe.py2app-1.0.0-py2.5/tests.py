# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/rod/recipe/py2app/tests.py
# Compiled at: 2008-02-04 15:19:34
"""Testing.

All of the tests can be found in the README.txt file.
"""
__docformat__ = 'restructuredtext'
import unittest, doctest, zope.testing

def setUp(test):
    pass


def tearDown(test):
    pass


def test_suite():
    return unittest.TestSuite((
     doctest.DocFileSuite('README.txt', setUp=setUp, tearDown=tearDown, optionflags=doctest.ELLIPSIS),))