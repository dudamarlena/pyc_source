# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/tagger/tests.py
# Compiled at: 2006-10-11 12:04:48
import os, sys, unittest, doctest
try:
    from zope.testing import doctest
except ImportError:
    pass

flags = doctest.ELLIPSIS | doctest.REPORT_ONLY_FIRST_FAILURE

def test_suite():
    return doctest.DocFileSuite('README.txt', optionflags=flags)


if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())