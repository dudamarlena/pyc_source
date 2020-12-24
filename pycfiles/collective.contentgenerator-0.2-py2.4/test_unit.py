# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentgenerator/tests/test_unit.py
# Compiled at: 2009-01-19 09:24:11
import unittest
from zope.testing import doctest

def test_suite():
    return unittest.TestSuite([doctest.DocFileSuite('tests/unit.txt', package='collective.contentgenerator')])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')