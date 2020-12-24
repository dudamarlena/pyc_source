# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/pingtool/tests/base.py
# Compiled at: 2009-03-31 04:47:32
from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.CMFCore.utils import getToolByName
from Products.Five.testbrowser import Browser
from Products.Five import fiveconfigure, zcml
from quintagroup.pingtool import PingTool
from quintagroup.pingtool.config import *
PRODUCTS = [
 PROJECTNAME]

@onsetup
def setup_product():
    """Set up additional products and ZCML required to test this product.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    fiveconfigure.debug_mode = True
    import quintagroup.pingtool
    zcml.load_config('configure.zcml', quintagroup.pingtool)
    fiveconfigure.debug_mode = False
    ZopeTestCase.installPackage(PROJECTNAME)


setup_product()
map(PloneTestCase.installProduct, ('XMLRPCMethod', ))
PloneTestCase.setupPloneSite(products=PRODUCTS)

class TestCase(PloneTestCase.PloneTestCase):
    """Base class used for test cases
    """
    __module__ = __name__


class FunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """
    __module__ = __name__

    def afterSetUp(self):
        super(FunctionalTestCase, self).afterSetUp()
        self.browser = Browser()
        self.uf = self.portal.acl_users
        self.uf.userFolderAddUser('root', 'secret', ['Manager'], [])
        self.ptool = getToolByName(self.portal, 'portal_properties')
        self.pitool = getToolByName(self.ptool, 'portal_pingtool')
        self.site_props = self.ptool.site_properties

    def loginAsManager(self, user='root', pwd='secret'):
        """points the browser to the login screen and logs in as user root with Manager role."""
        self.browser.open('http://nohost/plone/')
        self.browser.getLink('Log in').click()
        self.browser.getControl('Login Name').value = user
        self.browser.getControl('Password').value = pwd
        self.browser.getControl('Log in').click()