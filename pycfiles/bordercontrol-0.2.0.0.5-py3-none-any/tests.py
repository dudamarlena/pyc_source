# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/borda/tests.py
# Compiled at: 2013-08-05 13:27:40
__doc__ = '\nModule: tests.py\n\nThis module holds all tests for the borda application\n\nAuthor: Luis Osa <luis.osa.gdc@gmail.com>\n'
import doctest

def test_suite():
    """Return all doctests as a test suite, required by zope.testrunner"""
    return doctest.DocFileSuite('../README.rst', 'server.rst', 'client.rst', optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)