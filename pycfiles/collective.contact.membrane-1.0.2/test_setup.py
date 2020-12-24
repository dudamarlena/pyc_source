# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cedricmessiant/workspace/buildouts/webpro/src/collective.contact.membrane/src/collective/contact/membrane/tests/test_setup.py
# Compiled at: 2014-10-07 09:08:31
"""Setup/installation tests for this package."""
from collective.contact.membrane.testing import IntegrationTestCase
from plone import api

class TestInstall(IntegrationTestCase):
    """Test installation of collective.contact.membrane into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.contact.membrane is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.contact.membrane'))

    def test_uninstall(self):
        """Test if collective.contact.membrane is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.contact.membrane'])
        self.assertFalse(self.installer.isProductInstalled('collective.contact.membrane'))

    def test_membrane_person_user(self):
        degaulle = self.portal.mydirectory.degaulle
        user = api.user.get(degaulle.UID())
        self.assertEqual(user.getProperty('fullname'), 'Charles De Gaulle')
        self.assertEqual(user.getProperty('email'), 'charles.de.gaulle@armees.fr')
        self.assertEqual(user.getProperty('home_page'), 'http://www.charles-de-gaulle.org')