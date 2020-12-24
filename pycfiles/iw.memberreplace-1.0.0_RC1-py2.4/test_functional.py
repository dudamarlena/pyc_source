# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/memberreplace/tests/test_functional.py
# Compiled at: 2009-03-07 19:02:29
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
import os, glob
from unittest import TestSuite
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite
from iw.memberreplace.tests.base import memberreplaceFunctionalTestCase
OPTIONFLAGS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

def tests_list():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    return glob.glob1(this_dir, 'test*.txt')


def test_suite():
    suite = TestSuite()
    for test in tests_list():
        suite.addTest(FunctionalDocFileSuite(test, optionflags=OPTIONFLAGS, package='iw.memberreplace.tests', test_class=memberreplaceFunctionalTestCase))

    return suite