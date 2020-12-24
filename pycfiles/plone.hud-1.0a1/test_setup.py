# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/plone.hud/plone.hud1/src/plone/hud/tests/test_setup.py
# Compiled at: 2013-08-07 08:57:27
"""Setup/installation tests for this package."""
from plone.hud.testing import IntegrationTestCase
from plone import api

class TestInstall(IntegrationTestCase):
    """Test installation of plone.hud into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if plone.hud is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('plone.hud'))

    def test_uninstall(self):
        """Test if plone.hud is cleanly uninstalled."""
        self.installer.uninstallProducts(['plone.hud'])
        self.assertFalse(self.installer.isProductInstalled('plone.hud'))

    def test_browserlayer(self):
        """Test that IPloneHudLayer is registered."""
        from plone.hud.interfaces import IPloneHudLayer
        from plone.browserlayer import utils
        self.failUnless(IPloneHudLayer in utils.registered_layers())