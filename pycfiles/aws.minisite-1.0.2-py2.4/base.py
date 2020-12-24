# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\aws\minisite\tests\base.py
# Compiled at: 2010-04-08 08:46:16
"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""
import sys
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    """Set up the package and its dependencies.

    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer. We could
    have created our own layer, but this is the easiest way for Plone
    integration tests.
    """
    fiveconfigure.debug_mode = True
    import aws.minisite
    zcml.load_config('configure.zcml', aws.minisite)
    fiveconfigure.debug_mode = False
    ztc.installProduct('FCKeditor')
    ztc.installProduct('SmartColorWidget')
    ztc.installPackage('collective.phantasy')
    ztc.installPackage('aws.minisite')


setup_product()
ptc.setupPloneSite(products=['aws.minisite'])

class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """
    __module__ = __name__


class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """
    __module__ = __name__

    class layer(PloneSite):
        __module__ = __name__

        @classmethod
        def setUp(cls):
            try:
                iphook = sys.displayhook
                sys.displayhook = sys.__displayhook__
            except:
                pass

        @classmethod
        def tearDown(cls):
            pass

    def afterSetUp(self):
        roles = ('Member', 'Contributor')
        self.portal.portal_membership.addMember('contributor', 'secret', roles, [])