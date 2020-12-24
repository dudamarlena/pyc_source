# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/xm/globalissues/tests.py
# Compiled at: 2009-02-20 03:18:45
import unittest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()
import xm.globalissues
ztc.installProduct('Poi')
ztc.installProduct('eXtremeManagement')

class TestCase(ptc.PloneTestCase):
    __module__ = __name__

    class layer(PloneSite):
        __module__ = __name__

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', xm.globalissues)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


ptc.setupPloneSite(products=['Poi', 'eXtremeManagement', 'xm.globalissues'])

def test_suite():
    return unittest.TestSuite([ztc.ZopeDocFileSuite('README.txt', package='xm.globalissues', test_class=TestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')