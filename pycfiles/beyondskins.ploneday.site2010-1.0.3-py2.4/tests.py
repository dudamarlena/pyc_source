# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-fat/egg/beyondskins/ploneday/site2010/tests.py
# Compiled at: 2010-04-15 11:13:05
import unittest, doctest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup
ptc.setupPloneSite()
import beyondskins.ploneday.site2010

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', beyondskins.ploneday.site2010)
    fiveconfigure.debug_mode = False


setup_product()
ptc.setupPloneSite(products=['beyondskins.ploneday.site2010'], extension_profiles=['beyondskins.ploneday.site2010:default'])

class TestCase(ptc.PloneTestCase):
    __module__ = __name__

    class layer(PloneSite):
        __module__ = __name__

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', beyondskins.ploneday.site2010)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([ztc.FunctionalDocFileSuite('browser.txt', package='beyondskins.ploneday.site2010.doc', test_class=TestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')