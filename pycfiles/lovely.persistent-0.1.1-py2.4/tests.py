# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/lovely/persistent/tests.py
# Compiled at: 2007-12-10 10:14:22
"""
$Id: tests.py 82239 2007-12-10 15:14:21Z batlogg $
"""
__docformat__ = 'reStructuredText'
import unittest
from zope.testing import doctest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing.setup import placefulSetUp, placefulTearDown
from lovely import persistent

class LovelyPersistent(persistent.Persistent):
    __module__ = __name__


def setUp(test):
    root = placefulSetUp(site=True)
    test.globs['root'] = root
    test.globs['LovelyPersistent'] = LovelyPersistent


def tearDown(test):
    placefulTearDown()


def test_suite():
    return unittest.TestSuite((DocFileSuite('README.txt', setUp=setUp, tearDown=tearDown, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')