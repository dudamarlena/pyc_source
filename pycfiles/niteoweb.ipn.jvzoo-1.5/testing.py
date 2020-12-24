# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/nw1/niteoweb.ipn.jvzoo/src/niteoweb/ipn/jvzoo/testing.py
# Compiled at: 2013-10-02 09:19:46
"""Base module for unittesting."""
from plone.app.controlpanel.tests import ControlPanelTestCase
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2
import unittest2 as unittest

class NiteowebIpnJvzooLayer(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        import niteoweb.ipn.jvzoo
        self.loadZCML(package=niteoweb.ipn.jvzoo)
        z2.installProduct(app, 'niteoweb.ipn.jvzoo')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        applyProfile(portal, 'niteoweb.ipn.jvzoo:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'folder')
        portal.portal_catalog.clearFindAndRebuild()
        import transaction
        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'niteoweb.ipn.jvzoo')


FIXTURE = NiteowebIpnJvzooLayer()
INTEGRATION_TESTING = IntegrationTesting(bases=(
 FIXTURE,), name='NiteowebIpnJvzooLayer:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(bases=(
 FIXTURE,), name='NiteowebIpnJvzooLayer:Functional')

class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""
    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""
    layer = FUNCTIONAL_TESTING


class JvzooControlPanelTestCase(FunctionalTestCase, ControlPanelTestCase):
    """Test case used for control panel tests

    Comes with convenience methods from plone.app.controlpanel.
    """
    pass