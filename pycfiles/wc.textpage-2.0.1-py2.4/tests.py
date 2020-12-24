# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/wc/textpage/tests.py
# Compiled at: 2007-02-23 15:42:05
import unittest
from zope.testing.doctestunit import DocTestSuite

def test_suite():
    return unittest.TestSuite((DocTestSuite('wc.textpage.page'), DocTestSuite('wc.textpage.dublincore')))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')