# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentgenerator/tests/test_unit.py
# Compiled at: 2009-01-19 09:24:11
import unittest
from zope.testing import doctest

def test_suite():
    return unittest.TestSuite([doctest.DocFileSuite('tests/unit.txt', package='collective.contentgenerator')])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')