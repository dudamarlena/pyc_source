# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3392)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/lazysizes/src/collective/lazysizes/tests/test_setup.py
# Compiled at: 2019-03-12 21:37:53
# Size of source mod 2**32: 2434 bytes
from collective.lazysizes.config import PROJECTNAME
from collective.lazysizes.interfaces import ILazySizesLayer
from collective.lazysizes.testing import INTEGRATION_TESTING
from collective.lazysizes.testing import IS_BBB
from collective.lazysizes.testing import QIBBB
from plone.browserlayer.utils import registered_layers
import unittest
JS = ('++resource++collective.lazysizes/lazysizes.js', )

class InstallTestCase(unittest.TestCase):
    __doc__ = 'Ensure product is properly installed.'
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    @unittest.skipIf(IS_BBB, 'Plone >= 5.1')
    def test_installed(self):
        from Products.CMFPlone.utils import get_installer
        qi = get_installer(self.portal, self.request)
        self.assertTrue(qi.is_product_installed(PROJECTNAME))

    @unittest.skipUnless(IS_BBB, 'Plone < 5.1')
    def test_installed_BBB(self):
        qi = self.portal['portal_quickinstaller']
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        self.assertIn(ILazySizesLayer, registered_layers())

    def test_setup_permission(self):
        permission = 'collective.lazysizes: Setup'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Manager', 'Site Administrator']
        self.assertListEqual(roles, expected)

    def test_version(self):
        profile = 'collective.lazysizes:default'
        setup_tool = self.portal['portal_setup']
        self.assertEqual(setup_tool.getLastVersionForProfile(profile), ('10', ))


class UninstallTestCase(unittest.TestCase, QIBBB):
    __doc__ = 'Ensure product is properly uninstalled.'
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.qi = self.uninstall()

    @unittest.skipIf(IS_BBB, 'Plone >= 5.1')
    def test_uninstalled(self):
        self.assertFalse(self.qi.is_product_installed(PROJECTNAME))

    @unittest.skipUnless(IS_BBB, 'Plone < 5.1')
    def test_uninstalled_BBB(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        self.assertNotIn(ILazySizesLayer, registered_layers())