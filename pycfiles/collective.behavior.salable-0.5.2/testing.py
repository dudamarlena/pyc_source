# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/collective/behavior.richpreview/src/collective/behavior/richpreview/testing.py
# Compiled at: 2018-04-05 17:11:05
__doc__ = 'Setup testing infrastructure.\n\nFor Plone 5 we need to install plone.app.contenttypes.\n'
from collective.behavior.richpreview.tests.utils import enable_rich_preview_behavior
from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
IS_PLONE_5 = api.env.plone_version().startswith('5')

class Fixture(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.behavior.richpreview
        self.loadZCML(package=collective.behavior.richpreview)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.behavior.richpreview:default')
        enable_rich_preview_behavior('News Item')
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(bases=(
 FIXTURE,), name='collective.behavior.richpreview:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(bases=(
 FIXTURE,), name='collective.behavior.richpreview:Functional')
ROBOT_TESTING = FunctionalTesting(bases=(
 FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE), name='collective.behavior.richpreview:Robot')