# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/matej/workarea/plone.hud/plone.app.hud/src/plone/app/hud/testing.py
# Compiled at: 2013-07-28 05:44:03
__doc__ = 'Base module for unittesting.'
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

class PloneAppHudLayer(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        import plone.app.hud
        self.loadZCML(package=plone.app.hud)
        z2.installProduct(app, 'plone.app.hud')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        applyProfile(portal, 'plone.app.hud:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'folder')
        portal.portal_catalog.clearFindAndRebuild()
        import transaction
        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'plone.app.hud')


FIXTURE = PloneAppHudLayer()
INTEGRATION_TESTING = IntegrationTesting(bases=(
 FIXTURE,), name='PloneAppHudLayer:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(bases=(
 FIXTURE,), name='PloneAppHudLayer:Functional')

class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""
    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""
    layer = FUNCTIONAL_TESTING