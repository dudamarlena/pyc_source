# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/hexagonit/decorators/tests.py
# Compiled at: 2007-09-04 13:06:55
import unittest
from zope.testing import doctest
optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE

def test_suite():
    suite = unittest.TestSuite((doctest.DocFileSuite('README.txt', optionflags=optionflags), doctest.DocFileSuite('edgecases.txt', optionflags=optionflags)))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')