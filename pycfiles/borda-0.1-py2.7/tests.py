# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/borda/tests.py
# Compiled at: 2013-08-05 13:27:40
"""
Module: tests.py

This module holds all tests for the borda application

Author: Luis Osa <luis.osa.gdc@gmail.com>
"""
import doctest

def test_suite():
    """Return all doctests as a test suite, required by zope.testrunner"""
    return doctest.DocFileSuite('../README.rst', 'server.rst', 'client.rst', optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)