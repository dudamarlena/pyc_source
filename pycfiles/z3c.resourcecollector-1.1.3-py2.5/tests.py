# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/z3c/resourcecollector/tests.py
# Compiled at: 2008-07-29 15:59:13
__docformat__ = 'reStructuredText'
import os, doctest, unittest
from zope.testing import doctest
from zope.testing.doctestunit import DocFileSuite, DocTestSuite

def test_suite():
    return unittest.TestSuite((
     DocFileSuite('zcml.txt', optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')