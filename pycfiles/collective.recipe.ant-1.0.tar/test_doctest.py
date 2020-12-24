# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/recaptchawidget/tests/test_doctest.py
# Compiled at: 2010-04-15 12:24:16
import unittest, doctest
from Testing import ZopeTestCase as ztc
from collective.recaptchawidget.tests import base

def test_suite():
    return unittest.TestSuite([ztc.ZopeDocFileSuite('README.txt', package='collective.recaptchawidget', test_class=base.FunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')