# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/tutorial.todoapp/src/tutorial/todoapp/tests/base.py
# Compiled at: 2012-09-05 03:54:45
"""Base module for unittesting."""
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
import unittest2 as unittest

class TodoAppLayer(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        import tutorial.todoapp
        self.loadZCML(package=tutorial.todoapp)
        z2.installProduct(app, 'tutorial.todoapp')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        applyProfile(portal, 'tutorial.todoapp:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        api.content.create(container=portal, type='Folder', id='folder')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'tutorial.todoapp')


FIXTURE = TodoAppLayer()
INTEGRATION_TESTING = IntegrationTesting(bases=(
 FIXTURE,), name='TodoAppLayer:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(bases=(
 FIXTURE,), name='TodoAppLayer:Functional')

class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""
    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""
    layer = FUNCTIONAL_TESTING