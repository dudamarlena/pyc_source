# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ao/social/tests.py
# Compiled at: 2010-04-09 14:35:49
import doctest, unittest
docfiles = ('middleware.rst', 'django.rst')

def test_suite():
    """Run all doctests in one test suite."""
    tests = [ doctest.DocFileSuite(file, optionflags=doctest.ELLIPSIS) for file in docfiles
            ]
    return unittest.TestSuite(tests)