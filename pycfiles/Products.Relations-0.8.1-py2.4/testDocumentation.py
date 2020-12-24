# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/tests/testDocumentation.py
# Compiled at: 2008-09-11 19:48:09
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
package = 'Products.Relations.doc'
from Products.PloneTestCase import PloneTestCase
import common
common.installWithinPortal()

class TestOverviewTxt(PloneTestCase.PloneTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.folder.invokeFactory('SimpleType', 'alfred')
        self.folder.invokeFactory('ComplexType', 'manfred')
        self.ruleset = common.createRuleset(self, 'IsParentOf')


def test_suite():
    from unittest import TestSuite
    from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
    return TestSuite((ZopeDocFileSuite('Overview.txt', package='Products.Relations.doc', test_class=TestOverviewTxt),))


if __name__ == '__main__':
    framework()