# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zgeo/wfs/tests/tests.py
# Compiled at: 2008-04-20 13:31:51
import unittest, doctest
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return unittest.TestSuite([ztc.ZopeDocFileSuite('tests/webfeatureservice.txt', package='zgeo.wfs', test_class=ExampleFunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/geoitem.txt', package='zgeo.wfs', test_class=ExampleFunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)])


@onsetup
def setup_product():
    """Set up the package and its dependencies.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer. We could have created our
    own layer, but this is the easiest way for Plone integration tests.
    """
    fiveconfigure.debug_mode = True
    import zgeo.wfs
    zcml.load_config('configure.zcml', zgeo.wfs)
    fiveconfigure.debug_mode = False


setup_product()
ptc.setupPloneSite()

class ExampleFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """
    __module__ = __name__