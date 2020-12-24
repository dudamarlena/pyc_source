# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/osha.quizzes/src/osha/quizzes/tests/test_setup.py
# Compiled at: 2012-10-19 05:44:35
"""Setup/installation tests for this package."""
from osha.quizzes.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName
import unittest2 as unittest

class TestInstall(IntegrationTestCase):
    """Test installation of osha.quizzes into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_installed(self):
        """Test if osha.quizzes is installed with portal_quickinstaller."""
        self.failUnless(self.installer.isProductInstalled('osha.quizzes'))

    def test_uninstall(self):
        """Test if osha.quizzes is cleanly uninstalled."""
        self.installer.uninstallProducts(['osha.quizzes'])
        self.failIf(self.installer.isProductInstalled('osha.quizzes'))

    def test_folder_available_layouts(self):
        """Test that our custom display layout (@@quizzes) is available on folders
        and that the default ones are also still there.
        """
        layouts = self.portal.folder.getAvailableLayouts()
        layout_ids = [ id for (id, title) in layouts ]
        self.assertIn('folder_listing', layout_ids)
        self.assertIn('folder_summary_view', layout_ids)
        self.assertIn('folder_tabular_view', layout_ids)
        self.assertIn('atct_album_view', layout_ids)
        self.assertIn('folder_full_view', layout_ids)
        self.assertIn('quizzes', layout_ids)

    def test_js_registered(self):
        """Test if quizzes.js JavaScript file is registered in
        portal_javascript.
        """
        resources = self.portal.portal_javascripts.getResources()
        ids = [ r.getId() for r in resources ]
        self.assertIn('++resource++osha.quizzes/quizzes.js', ids)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)