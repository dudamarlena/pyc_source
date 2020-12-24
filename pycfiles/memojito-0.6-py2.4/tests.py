# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/memojito/tests.py
# Compiled at: 2007-05-01 00:37:57
import os, sys, unittest
try:
    from zope.testing import doctest
except ImportError:
    import doctest

optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS

def test_suite():
    return unittest.TestSuite((doctest.DocFileSuite('README.txt', package='memojito', optionflags=optionflags),))


if __name__ == '__main__':
    import unittest
    unittest.TextTestRunner().run(test_suite())