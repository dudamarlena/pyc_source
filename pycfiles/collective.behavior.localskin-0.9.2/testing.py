# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/collective/behavior.localregistry/src/collective/behavior/localregistry/testing.py
# Compiled at: 2014-03-12 09:30:39
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig

class CollectiveBehaviorLocalregistry(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.dexterity
        xmlconfig.file('configure.zcml', plone.app.dexterity, context=configurationContext)
        import collective.behavior.localregistry
        xmlconfig.file('configure.zcml', collective.behavior.localregistry, context=configurationContext)

    def setUpPloneSite(self, portal):
        self['portal'] = portal
        roles = ('Member', 'Manager')
        portal.portal_membership.addMember('manager', 'secret', roles, [])
        roles = ('Member', 'Contributor')
        portal.portal_membership.addMember('contributor', 'secret', roles, [])


COLLECTIVE_BEHAVIOR_LOCALREGISTRY_FIXTURE = CollectiveBehaviorLocalregistry()
COLLECTIVE_BEHAVIOR_LOCALREGISTRY_INTEGRATION_TESTING = IntegrationTesting(bases=(COLLECTIVE_BEHAVIOR_LOCALREGISTRY_FIXTURE,), name='CollectiveBehaviorLocalregistry:Integration')