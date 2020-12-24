# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sc/object/dissect/tests.py
# Compiled at: 2009-11-18 13:46:44
import unittest, doctest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup
import sc.object.dissect

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', sc.object.dissect)
    fiveconfigure.debug_mode = False
    ztc.installPackage('sc.object.dissect')


setup_product()
ptc.setupPloneSite(extension_profiles=['sc.object.dissect:default'])

class TestCase(ptc.PloneTestCase):
    __module__ = __name__

    class layer(PloneSite):
        __module__ = __name__

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([ztc.ZopeDocFileSuite('README.txt', package='sc.object.dissect.docs', optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, test_class=TestCase), ztc.FunctionalDocFileSuite('browser.txt', package='sc.object.dissect.docs', optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, test_class=TestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')