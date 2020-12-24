# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/template/tests/tests.py
# Compiled at: 2009-05-04 14:30:04
import unittest, doctest
from zope.app.testing import setup
from zope.testing.doctestunit import DocFileSuite

def setUp(test):
    setup.placefulSetUp()


def tearDown(test):
    setup.placefulTearDown()


def test_suite():
    return unittest.TestSuite((DocFileSuite('README.txt', package='ice.template', setUp=setUp, tearDown=tearDown, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),))