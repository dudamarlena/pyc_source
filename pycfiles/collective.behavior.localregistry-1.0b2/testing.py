# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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