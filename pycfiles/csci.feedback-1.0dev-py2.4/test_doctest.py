# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/csci/feedback/tests/test_doctest.py
# Compiled at: 2009-10-20 07:07:12
import unittest, doctest
from zope.testing import doctestunit
from zope.component import testing, eventtesting
from Testing import ZopeTestCase as ztc
from csci.feedback.tests import base

def test_suite():
    return unittest.TestSuite([ztc.ZopeDocFileSuite('README.txt', package='csci.feedback', test_class=base.FunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')