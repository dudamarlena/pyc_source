# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wc/rating/tests.py
# Compiled at: 2007-03-07 18:02:59
import unittest
from doctest import DocFileSuite
import zope.component.testing
from zope.annotation.attribute import AttributeAnnotations
from wc.rating.rating import rating_adapter

def setUp(test):
    zope.component.testing.setUp(test)
    zope.component.provideAdapter(AttributeAnnotations)
    zope.component.provideAdapter(rating_adapter)


def test_suite():
    return unittest.TestSuite((DocFileSuite('README.txt', package='wc.rating', setUp=setUp, tearDown=zope.component.testing.tearDown),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')