# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bopen/atcontenttypes/tests/test_doctest.py
# Compiled at: 2010-09-07 11:53:01
import unittest, doctest
from Testing import ZopeTestCase as ztc
from bopen.atcontenttypes.tests import base

def test_suite():
    return unittest.TestSuite([ztc.ZopeDocFileSuite('README.txt', package='bopen.atcontenttypes', test_class=base.FunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')