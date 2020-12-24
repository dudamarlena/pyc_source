# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cedricmessiant/workspace/buildouts/webpro/src/collective.contact.membrane/src/collective/contact/membrane/testing.py
# Compiled at: 2014-02-14 06:28:25
__doc__ = 'Base module for unittesting.'
from plone import api
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
import unittest2 as unittest, collective.contact.membrane

class CollectiveContactMembraneLayer(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)
    products = ('collective.contact.membrane', 'Products.membrane')

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        self.loadZCML(package=collective.contact.membrane, name='testing.zcml')
        for p in self.products:
            z2.installProduct(app, p)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        applyProfile(portal, 'collective.contact.membrane:testing')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        folder_id = portal.invokeFactory('Folder', 'folder')
        portal[folder_id].reindexObject()
        membrane = api.portal.get_tool('membrane_tool')
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog.searchResults(portal_type=tuple(membrane.membrane_types))
        for brain in brains:
            membrane.reindexObject(brain.getObject())

        import transaction
        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        for p in reversed(self.products):
            z2.uninstallProduct(app, p)


FIXTURE = CollectiveContactMembraneLayer(name='FIXTURE')
INTEGRATION = IntegrationTesting(bases=(
 FIXTURE,), name='INTEGRATION')
FUNCTIONAL = FunctionalTesting(bases=(
 FIXTURE,), name='FUNCTIONAL')

class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""
    layer = INTEGRATION

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.portal = self.layer['portal']


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""
    layer = FUNCTIONAL