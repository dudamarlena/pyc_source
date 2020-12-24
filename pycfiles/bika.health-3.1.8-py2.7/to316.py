# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/upgrade/to316.py
# Compiled at: 2015-11-03 03:53:19
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from bika.health.permissions import ViewPatients, EditPatient, ViewAnalysisRequests, ViewSamples, ViewBatches
from bika.health.permissions import AddInsuranceCompany, ViewInsuranceCompanies
from bika.lims import logger

def upgrade(tool):
    """ Health-191: Giving patient view permissions to referrer institutions contacts
        Create InsuranceCompany content type.
    """
    portal = aq_parent(aq_inner(tool))
    typestool = getToolByName(portal, 'portal_types')
    setup = portal.portal_setup
    setup.runImportStepFromProfile('profile-bika.health:default', 'typeinfo')
    setup.runImportStepFromProfile('profile-bika.health:default', 'controlpanel')
    setup.runImportStepFromProfile('profile-bika.health:default', 'factorytool')
    setup.runImportStepFromProfile('profile-bika.health:default', 'propertiestool')
    setup.runImportStepFromProfile('profile-bika.health:default', 'jsregistry')
    setup.runImportStepFromProfile('profile-bika.health:default', 'cssregistry')
    setup.runImportStepFromProfile('profile-bika.health:default', 'workflow')
    setup.runImportStepFromProfile('profile-bika.health:default', 'workflow-csv')
    workflow = getToolByName(portal, 'portal_workflow')
    workflow.updateRoleMappings()
    at = getToolByName(portal, 'archetype_tool')
    at.setCatalogsByType('InsuranceCompany', ['bika_setup_catalog'])
    if not portal['bika_setup'].get('bika_insurancecompanies'):
        typestool.constructContent(type_name='InsuranceCompanies', container=portal['bika_setup'], id='bika_insurancecompanies', title='Insurance Companies')
    obj = portal['bika_setup']['bika_insurancecompanies']
    obj.unmarkCreationFlag()
    obj.reindexObject()
    if not portal['bika_setup'].get('bika_insurancecompanies'):
        logger.info('InsuranceCompanies not created')
    mp = portal.manage_permission
    mp(AddInsuranceCompany, ['Manager', 'Owner', 'LabManager', 'LabClerk'], 1)
    mp(ViewInsuranceCompanies, ['Manager', 'LabManager', 'Owner', 'LabClerk', 'Doctor', 'RegulatoryInspector'], 1)
    mp = portal.clients.manage_permission
    mp(ViewPatients, ['Manager', 'LabManager', 'Owner', 'LabClerk', 'Doctor', 'Client', 'RegulatoryInspector', 'Client'], 1)
    portal.clients.reindexObject()
    mp = portal.patients.manage_permission
    mp(EditPatient, ['Manager', 'LabManager', 'LabClerk', 'Client'], 1)
    mp(ViewPatients, ['Manager', 'LabManager', 'Owner', 'LabClerk', 'Doctor', 'RegulatoryInspector', 'Client'], 1)
    mp(ViewAnalysisRequests, ['Manager', 'LabManager', 'LabClerk', 'RegulatoryInspector', 'Doctor', 'Client'], 0)
    mp(ViewSamples, ['Manager', 'LabManager', 'LabClerk', 'RegulatoryInspector', 'Doctor', 'Client'], 0)
    mp(ViewBatches, ['Manager', 'LabManager', 'LabClerk', 'RegulatoryInspector', 'Doctor', 'Client'], 0)
    mp(permissions.View, ['Manager', 'LabManager', 'LabClerk', 'RegulatoryInspector', 'Doctor', 'Client'], 0)
    mp('Access contents information', ['Manager', 'LabManager', 'LabClerk', 'RegulatoryInspector', 'Doctor', 'Client'], 0)
    portal.patients.reindexObject()
    client = portal.portal_types.getTypeInfo('Client')
    client.addAction(id='patients', name='Patients', action='string:${object_url}/patients', permission='BIKA: View Patients', category='object', visible=True, icon_expr='string:${portal_url}/images/patient.png', link_target='', description='', condition='')
    portal.moveObjectToPosition('invoices', portal.objectIds().index('supplyorders'))
    portal.moveObjectToPosition('arimports', portal.objectIds().index('referencesamples'))
    return True