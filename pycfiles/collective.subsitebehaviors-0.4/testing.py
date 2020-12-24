# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/psf/Home/Code/koodaamo/collective.subsitebehaviors/src/collective/subsitebehaviors/testing.py
# Compiled at: 2015-09-05 08:33:52
"""Base module for unittesting."""
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.testing import z2
import collective.subsitebehaviors

class CollectiveSubsiteBehaviorsLayer(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)
    products = [
     'collective.subsitebehaviors']

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        self.loadZCML(package=collective.subsitebehaviors, name='testing.zcml')
        for product in self.products:
            z2.installProduct(app, product)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        applyProfile(portal, 'collective.subsitebehaviors:testing')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

    def tearDownZope(self, app):
        """Tear down Zope."""
        for product in reversed(self.products):
            z2.uninstallProduct(app, product)


FIXTURE = CollectiveSubsiteBehaviorsLayer(name='FIXTURE')
INTEGRATION = IntegrationTesting(bases=(
 FIXTURE,), name='INTEGRATION')
FUNCTIONAL = FunctionalTesting(bases=(
 FIXTURE,), name='FUNCTIONAL')
ACCEPTANCE = FunctionalTesting(bases=(
 FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE), name='ACCEPTANCE')