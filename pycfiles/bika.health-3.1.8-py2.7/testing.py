# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/testing.py
# Compiled at: 2014-12-12 07:13:54
from bika.lims.exportimport.load_setup_data import LoadSetupData
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import applyProfile
from plone.testing import z2
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.setuphandlers import setupPortalContent
from Testing.makerequest import makerequest
import Products.ATExtensions, Products.PloneTestCase.setup, collective.js.jqueryui, plone.app.iterate

class BikaTestLayer(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import bika.lims, bika.health, archetypes.schemaextender
        self.loadZCML(package=Products.ATExtensions)
        self.loadZCML(package=plone.app.iterate)
        self.loadZCML(package=collective.js.jqueryui)
        self.loadZCML(package=archetypes.schemaextender)
        self.loadZCML(package=bika.lims)
        self.loadZCML(package=bika.health)
        z2.installProduct(app, 'Products.PythonScripts')
        z2.installProduct(app, 'bika.lims')
        z2.installProduct(app, 'bika.health')

    def setUpPloneSite(self, portal):
        login(portal.aq_parent, SITE_OWNER_NAME)
        wf = getToolByName(portal, 'portal_workflow')
        wf.setDefaultChain('plone_workflow')
        setupPortalContent(portal)
        portal.getTypeInfo().manage_changeProperties(view_methods=[
         'folder_listing'], default_view='folder_listing')
        applyProfile(portal, 'bika.lims:default')
        applyProfile(portal, 'bika.health:default')
        for role in ('LabManager', 'LabClerk', 'Analyst', 'Verifier', 'Sampler', 'Preserver',
                     'Publisher', 'Member', 'Reviewer', 'RegulatoryInspector'):
            for user_nr in range(2):
                if user_nr == 0:
                    username = 'test_%s' % role.lower()
                else:
                    username = 'test_%s%s' % (role.lower(), user_nr)
                member = portal.portal_registration.addMember(username, username, properties={'username': username, 
                   'email': username + '@example.com', 
                   'fullname': username})
                group_id = role + 's'
                group = portal.portal_groups.getGroupById(group_id)
                if group:
                    group.addMember(username)
                member._addRole(role)
                if role == 'LabManager':
                    portal.clients.manage_setLocalRoles(username, ['Owner'])

        self.request = makerequest(portal.aq_parent).REQUEST
        self.request.form['setupexisting'] = 1
        self.request.form['existing'] = 'bika.health:test'
        lsd = LoadSetupData(portal, self.request)
        lsd()
        logout()


BIKA_HEALTH_FIXTURE = BikaTestLayer()
HEALTH_INTEGRATION_TESTING = IntegrationTesting(bases=(
 BIKA_HEALTH_FIXTURE,), name='HealthTestingLayer:Integration')
HEALTH_FUNCTIONAL_TESTING = FunctionalTesting(bases=(
 BIKA_HEALTH_FIXTURE,), name='HealthTestingLayer:Functional')
BIKA_ROBOT_TESTING = FunctionalTesting(bases=(
 BIKA_HEALTH_FIXTURE, z2.ZSERVER_FIXTURE), name='HealthTestingLayer:Robot')