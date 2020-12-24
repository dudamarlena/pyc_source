# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/tests/base.py
# Compiled at: 2009-11-11 04:31:22
"""
Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of Plone's
products are loaded, and a Plone site will be created. This happens at module
level, which makes it faster to run each test, but slows down test runner
startup.
"""
from zope.component import getUtility
from zope.component import getMultiAdapter
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

@onsetup
def setup_product():
    """Set up the package and its dependencies.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer. We could have created our
    own layer, but this is the easiest way for Plone integration tests.
    """
    fiveconfigure.debug_mode = True
    import iscorpio.plonepm
    zcml.load_config('configure.zcml', iscorpio.plonepm)
    fiveconfigure.debug_mode = False
    ztc.installPackage('iscorpio.plonepm')


setup_product()
ptc.setupPloneSite(products=['iscorpio.plonepm'])

class PlonepmTestCase(ptc.PloneTestCase):
    """
    We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit 
    test cases.
    """
    __module__ = __name__
    portal_type = ''
    title = ''


class PlonepmPortletTestCase(PlonepmTestCase):
    """
    base test case for testing Plonepm Portlet.
    """
    __module__ = __name__

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        if not assignment:
            raise AttributeError('assignment is required!')
        context = context or self.portal
        request = request or self.app.REQUEST
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn', context=self.portal)
        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)


class PlonepmFunctionalTestCase(ptc.FunctionalTestCase):
    """
    We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """
    __module__ = __name__