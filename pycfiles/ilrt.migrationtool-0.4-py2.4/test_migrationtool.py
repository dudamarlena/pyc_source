# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ilrt/migrationtool/tests/test_migrationtool.py
# Compiled at: 2009-05-08 04:37:50
import unittest
from Testing import ZopeTestCase as ztc
from ilrt.migrationtool.tests import base
from Products.CMFPlone.tests.testMigrationTool import TestMigrationTool

def test_suite():
    return unittest.TestSuite([ztc.ZopeDocFileSuite('tests/browsertool.txt', package='ilrt.migrationtool', test_class=base.BaseFunctionalTestCase), ztc.ZopeDocFileSuite('tests/workflowtool.txt', package='ilrt.migrationtool', test_class=base.BaseFunctionalTestCase), unittest.makeSuite(TestMigrationTool), ztc.ZopeDocFileSuite('tests/migrationtool.txt', package='ilrt.migrationtool', test_class=base.BaseFunctionalTestCase), ztc.ZopeDocFileSuite('tests/utils.txt', package='ilrt.migrationtool', test_class=base.BaseFunctionalTestCase), ztc.ZopeDocFileSuite('tests/atfitool.txt', package='ilrt.migrationtool', test_class=base.BaseFunctionalTestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')