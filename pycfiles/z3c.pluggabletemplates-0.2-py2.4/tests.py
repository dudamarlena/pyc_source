# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/pluggabletemplates/tests.py
# Compiled at: 2006-11-01 08:19:33
__docformat__ = 'restructuredtext'
import unittest
from zope.testing import doctest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing import setup

def setUp(test):
    root = setup.placefulSetUp(site=True)
    test.globs['root'] = root


def tearDown(test):
    setup.placefulTearDown()


def test_suite():
    return unittest.TestSuite((DocFileSuite('./README.txt', setUp=setUp, tearDown=tearDown, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')