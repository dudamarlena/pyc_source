# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentgenerator/tests/test_users.py
# Compiled at: 2009-01-19 09:24:11
import unittest
from Testing import ZopeTestCase as ztc
from collective.contentgenerator.tests import base

def test_suite():
    return unittest.TestSuite([ztc.ZopeDocFileSuite('tests/users.txt', package='collective.contentgenerator', test_class=base.BaseFunctionalTestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')