# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/opml/tests.py
# Compiled at: 2008-02-13 15:51:52
import re, unittest, zope.testing
from zope.testing import doctest, renormalizing

def test_suite():
    return unittest.TestSuite((
     doctest.DocFileSuite('README', optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')