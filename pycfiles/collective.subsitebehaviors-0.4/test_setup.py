# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/psf/Home/Code/koodaamo/collective.subsitebehaviors/src/collective/subsitebehaviors/tests/test_setup.py
# Compiled at: 2015-09-05 08:35:05
"""Setup/installation tests for this package."""
from collective.subsitebehaviors.testing import INTEGRATION
from plone import api
import unittest2 as unittest

class TestInstall(unittest.TestCase):
    """Test installation of collective.subsitebehaviors into Plone."""
    layer = INTEGRATION

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.subsitebehaviors is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.subsitebehaviors'))

    def test_uninstall(self):
        """Test if collective.subsitebehaviors is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.subsitebehaviors'])
        self.assertFalse(self.installer.isProductInstalled('collective.subsitebehaviors'))

    def test_browserlayer(self):
        """Test that ICollectiveSubsitebehaviorsLayer is registered."""
        from collective.subsitebehaviors.interfaces import ICollectiveSubsiteBehaviorsLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveSubsiteBehaviorsLayer, utils.registered_layers())