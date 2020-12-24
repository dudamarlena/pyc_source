# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/slc.cart/src/slc/cart/tests/test_setup.py
# Compiled at: 2012-11-01 15:54:50
"""Setup/installation tests for this package."""
from plone import api
from slc.cart.tests.base import IntegrationTestCase
import unittest2 as unittest

class TestInstall(IntegrationTestCase):
    """Test installation of slc.cart into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if slc.cart is installed with portal_quickinstaller."""
        self.failUnless(self.installer.isProductInstalled('slc.cart'))

    def test_uninstall(self):
        """Test if slc.cart is cleanly uninstalled."""
        self.installer.uninstallProducts(['slc.cart'])
        self.failIf(self.installer.isProductInstalled('slc.cart'))

    def test_browserlayer(self):
        """Test that ISlcCartLayer is registered."""
        from slc.cart.interfaces import ISlcCartLayer
        from plone.browserlayer import utils
        self.failUnless(ISlcCartLayer in utils.registered_layers())

    def test_css_registered(self):
        """Test if slc.cart's css files are registered with portal_css."""
        resources = self.portal.portal_css.getResources()
        ids = [ r.getId() for r in resources ]
        self.assertIn('++resource++slc.cart/cart.css', ids)

    def test_js_registered(self):
        """Test if JavaScript files are registered with portal_javascript."""
        resources = self.portal.portal_javascripts.getResources()
        ids = [ r.getId() for r in resources ]
        self.assertIn('++resource++slc.cart/cart.js', ids)

    def test_cart_actions_added(self):
        """Test if cart actions are added to user and document actions."""
        actions_tool = api.portal.get_tool('portal_actions')
        user_actions = actions_tool.user.listActions()
        self.assertEquals(len(user_actions), 9)
        ids = [ a.getId() for a in user_actions ]
        self.assertIn('cart', ids)

    def test_registry_records_added(self):
        """Test if registry records have been added."""
        limit = api.portal.get_registry_record('slc.cart.limit')
        self.assertEquals(limit, 100)

    def test_authenticate_can_use_cart(self):
        """Test that all logged-in users can use the cart."""
        self.assertEquals(self.portal._slc_cart__Use_cart_Permission, ('Manager', 'Authenticated'))


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)