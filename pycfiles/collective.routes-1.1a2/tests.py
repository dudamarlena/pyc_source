# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/roundabout/tests.py
# Compiled at: 2008-12-29 12:01:34
import unittest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
import collective.roundabout
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    """Set up the package and its dependencies."""
    fiveconfigure.debug_mode = True
    import collective.roundabout
    zcml.load_config('configure.zcml', collective.roundabout)
    fiveconfigure.debug_mode = False
    ptc.installPackage('collective.roundabout')


setup_product()
ptc.setupPloneSite(extension_profiles=['collective.roundabout:default'])

def test_suite():
    return unittest.TestSuite([ztc.ZopeDocFileSuite('README.txt', package='collective.roundabout', test_class=ptc.PloneTestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')