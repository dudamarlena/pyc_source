# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/z2utils/tests/test_all.py
# Compiled at: 2007-11-30 08:40:13
import unittest
from zope.testing import doctest

def test_suite():
    return unittest.TestSuite((doctest.DocFileSuite('pkgloader.txt', package='p4a.z2utils'), doctest.DocTestSuite('p4a.z2utils.pkgloader', optionflags=doctest.ELLIPSIS), doctest.DocTestSuite('p4a.z2utils.utils', optionflags=doctest.ELLIPSIS)))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')