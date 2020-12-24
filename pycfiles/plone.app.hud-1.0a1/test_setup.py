# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/plone.hud/plone.app.hud/src/plone/app/hud/tests/test_setup.py
# Compiled at: 2013-07-28 05:45:45
"""Setup/installation tests for this package."""
from plone.app.hud.testing import IntegrationTestCase
from plone import api

class TestInstall(IntegrationTestCase):
    """Test installation of plone.app.hud into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if plone.app.hud is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('plone.app.hud'))

    def test_uninstall(self):
        """Test if plone.app.hud is cleanly uninstalled."""
        self.installer.uninstallProducts(['plone.app.hud'])
        self.assertFalse(self.installer.isProductInstalled('plone.app.hud'))

    def test_browserlayer(self):
        """Test that IPloneAppHudLayer is registered."""
        from plone.app.hud.interfaces import IPloneAppHudLayer
        from plone.browserlayer import utils
        self.failUnless(IPloneAppHudLayer in utils.registered_layers())