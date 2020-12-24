# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/tests/test_rating.py
# Compiled at: 2006-09-21 05:27:35
import unittest
from doctest import DocFileSuite
import zope.component.testing, zope.component.eventtesting
from zope.annotation.attribute import AttributeAnnotations
from worldcookery.rating import Rating

def setUp(test):
    zope.component.testing.setUp(test)
    zope.component.eventtesting.setUp(test)
    zope.component.provideAdapter(AttributeAnnotations)
    zope.component.provideAdapter(Rating)


def test_suite():
    return unittest.TestSuite((DocFileSuite('rating.txt', package='worldcookery', setUp=setUp, tearDown=zope.component.testing.tearDown),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')