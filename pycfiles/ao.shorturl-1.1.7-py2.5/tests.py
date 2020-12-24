# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ao/shorturl/tests.py
# Compiled at: 2010-03-22 00:36:40
import doctest, unittest
docfiles = ('shorturl.rst', 'django.rst', 'appengine.rst')
docstrings = ('ao.shorturl', )

def test_suite():
    """Run all doctests in one test suite."""
    tests = [ doctest.DocFileSuite(file, optionflags=doctest.ELLIPSIS) for file in docfiles
            ]
    tests += [ doctest.DocTestSuite(docstring, optionflags=doctest.ELLIPSIS) for docstring in docstrings
             ]
    return unittest.TestSuite(tests)