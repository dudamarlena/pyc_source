# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/plone.hud/plone.hud1/src/plone/hud/testing.py
# Compiled at: 2013-08-07 08:57:27
"""Base module for unittesting."""
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

class PloneHudLayer(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        import plone.hud
        self.loadZCML(package=plone.hud)
        z2.installProduct(app, 'plone.hud')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        applyProfile(portal, 'plone.hud:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'folder')
        portal.portal_catalog.clearFindAndRebuild()
        import transaction
        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'plone.hud')


FIXTURE = PloneHudLayer()
INTEGRATION_TESTING = IntegrationTesting(bases=(
 FIXTURE,), name='PloneHudLayer:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(bases=(
 FIXTURE,), name='PloneHudLayer:Functional')

class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""
    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""
    layer = FUNCTIONAL_TESTING