# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/rdflib_django/tests.py
# Compiled at: 2012-10-06 02:43:50
"""
Unittests and doctests for the rdflib_django app.
"""
import doctest
from django.utils import unittest
import rdflib_django
from rdflib_django import store, test_store, test_rdflib, test_seq, test_namespaces

def suite():
    """
    Generate the test suite.
    """
    s = unittest.TestSuite()
    s.addTest(doctest.DocTestSuite(rdflib_django))
    s.addTest(doctest.DocTestSuite(store))
    s.addTest(unittest.findTestCases(test_store))
    s.addTest(unittest.findTestCases(test_rdflib))
    s.addTest(unittest.findTestCases(test_seq))
    s.addTest(unittest.findTestCases(test_namespaces))
    return s