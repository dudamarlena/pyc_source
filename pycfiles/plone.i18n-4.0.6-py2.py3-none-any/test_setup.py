# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/matej/workarea/plone.hud/plone.hud1/src/plone/hud/tests/test_setup.py
# Compiled at: 2013-08-07 08:57:27
__doc__ = 'Setup/installation tests for this package.'
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