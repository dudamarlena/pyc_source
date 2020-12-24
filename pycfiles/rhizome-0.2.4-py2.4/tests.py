# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/rhizome/five/tests.py
# Compiled at: 2006-10-13 18:27:38
from collective.testing.utils import monkeyAppAsSite
monkeyAppAsSite()
import os, sys, unittest
from zope.testing import doctest
from collective.testing.layer import ZCMLLayer
optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS

def test_suite():
    import rhizome.five
    from Testing.ZopeTestCase import FunctionalDocFileSuite
    testsuite = FunctionalDocFileSuite('README.txt', optionflags=optionflags, package=rhizome)
    testsuite.layer = ZCMLLayer
    return testsuite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')