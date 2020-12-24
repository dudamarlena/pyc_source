# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/croppingimagefield/tests.py
# Compiled at: 2009-07-20 20:54:41
import unittest, os
from Globals import InitializeClass, package_home
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()
import collective.croppingimagefield

class TestCase(ptc.PloneTestCase):
    __module__ = __name__

    def afterSetUp(self):
        PACKAGE_HOME = package_home(globals())
        imgpath = os.path.join(PACKAGE_HOME, 'test.gif')
        self._image = open(imgpath).read()


def test_suite():
    return unittest.TestSuite([ztc.FunctionalDocFileSuite('README.txt', package='collective.croppingimagefield', test_class=TestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')