# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\superpyTesting\unitTestsFromSrc.py
# Compiled at: 2010-06-04 07:07:10
"""Module to read in all the doctests from src that we want to test.

This module is designed so that "python setup.py test" can just look in
here and automatically suck in the other doctests from the source.
"""
import unittest, doctest, superpy
from superpy.core import Process, DataStructures
import _test

def MakeMainSuperpyDoctest():
    """Return a unittest.TestSuite object representing doctests from source code

>>> import unitTestsFromSrc
>>> t = unitTestsFromSrc.MakeMainSuperpyDoctest()
>>> t.debug()
    """
    suite = unittest.TestSuite()
    for t in [DataStructures, superpy, Process, _test]:
        testCase = doctest.DocTestSuite(t)
        suite.addTest(testCase)

    return suite


mainTestSuite = MakeMainSuperpyDoctest()