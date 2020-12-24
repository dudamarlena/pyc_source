# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/lazysizes/src/collective/lazysizes/tests/test_setup.py
# Compiled at: 2018-09-06 08:44:35
from collective.lazysizes.config import PROJECTNAME
from collective.lazysizes.interfaces import ILazySizesLayer
from collective.lazysizes.testing import INTEGRATION_TESTING
from plone import api
from plone.browserlayer.utils import registered_layers
import unittest
JS = ('++resource++collective.lazysizes/lazysizes.js', )

class InstallTestCase(unittest.TestCase):
    """Ensure product is properly installed."""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = self.portal['portal_quickinstaller']
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        self.assertIn(ILazySizesLayer, registered_layers())

    def test_setup_permission(self):
        permission = 'collective.lazysizes: Setup'
        roles = self.portal.rolesOfPermission(permission)
        roles = [ r['name'] for r in roles if r['selected'] ]
        expected = ['Manager', 'Site Administrator']
        self.assertListEqual(roles, expected)

    def test_version(self):
        profile = 'collective.lazysizes:default'
        setup_tool = self.portal['portal_setup']
        self.assertEqual(setup_tool.getLastVersionForProfile(profile), ('10', ))


class UninstallTestCase(unittest.TestCase):
    """Ensure product is properly uninstalled."""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        with api.env.adopt_roles(['Manager']):
            self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        self.assertNotIn(ILazySizesLayer, registered_layers())