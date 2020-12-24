# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/spectools/tests/tests.py
# Compiled at: 2008-10-01 10:40:59
import unittest
from zope.testing import doctest

def test_suite():
    optionflags = doctest.ELLIPSIS | doctest.REPORT_NDIFF | doctest.NORMALIZE_WHITESPACE
    return unittest.TestSuite([doctest.DocFileSuite('../README.txt', optionflags=optionflags)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')