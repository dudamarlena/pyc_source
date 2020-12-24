# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/nw1/niteoweb.ipn.jvzoo/src/niteoweb/ipn/jvzoo/tests/test_setup.py
# Compiled at: 2013-10-02 09:19:46
"""Setup/installation tests for this package."""
from niteoweb.ipn.jvzoo.testing import IntegrationTestCase
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import unittest2 as unittest

class TestInstall(IntegrationTestCase):
    """Test installation of niteoweb.ipn.jvzoo into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if niteoweb.ipn.jvzoo is installed in portal_quickinstaller."""
        self.failUnless(self.installer.isProductInstalled('niteoweb.ipn.jvzoo'))

    def test_uninstall(self):
        """Test if niteoweb.ipn.jvzoo is cleanly uninstalled."""
        self.installer.uninstallProducts(['niteoweb.ipn.jvzoo'])
        self.failIf(self.installer.isProductInstalled('niteoweb.ipn.jvzoo'))

    def test_record_secretkey(self):
        """Test that the secretkey record is in the registry."""
        registry = getUtility(IRegistry)
        record_secretkey = registry.records['niteoweb.ipn.jvzoo.interfaces.IJVZooSettings.secretkey']
        from niteoweb.ipn.jvzoo.interfaces import IJVZooSettings
        self.assertIn('secretkey', IJVZooSettings)
        self.assertEquals(record_secretkey.value, None)
        return


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)