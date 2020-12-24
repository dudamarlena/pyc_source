# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/upgrade/to317.py
# Compiled at: 2015-11-03 03:53:39
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from bika.lims.utils import tmpID
from bika.lims.idserver import renameAfterCreation
from bika.health.permissions import AddEthnicity, ViewEthnicities
from bika.lims import logger

def upgrade(tool):
    portal = aq_parent(aq_inner(tool))
    setup = portal.portal_setup
    typestool = getToolByName(portal, 'portal_types')
    bpc = getToolByName(tool, 'bika_patient_catalog')
    all_patients = bpc(portal_type='Patient')
    patient_list = []
    for patient in all_patients:
        patient_obj = patient.getObject()
        pa_ethnicity = patient_obj.Schema()['Ethnicity'].get(patient_obj)
        pa_uid = patient_obj.UID()
        if pa_ethnicity != '':
            patient_list.append((pa_uid, pa_ethnicity))

    setup.runImportStepFromProfile('profile-bika.health:default', 'jsregistry')
    setup.runImportStepFromProfile('profile-bika.health:default', 'cssregistry')
    setup.runImportStepFromProfile('profile-bika.health:default', 'typeinfo')
    setup.runImportStepFromProfile('profile-bika.health:default', 'factorytool')
    setup.runImportStepFromProfile('profile-bika.health:default', 'workflow')
    setup.runImportStepFromProfile('profile-bika.health:default', 'controlpanel')
    workflow = getToolByName(portal, 'portal_workflow')
    workflow.updateRoleMappings()
    at = getToolByName(portal, 'archetype_tool')
    at.setCatalogsByType('Ethnicity', ['bika_setup_catalog'])
    if not portal['bika_setup'].get('bika_ethnicities'):
        typestool.constructContent(type_name='Ethnicities', container=portal['bika_setup'], id='bika_ethnicities', title='Ethnicity')
    obj = portal['bika_setup']['bika_ethnicities']
    obj.unmarkCreationFlag()
    obj.reindexObject()
    if not portal['bika_setup'].get('bika_ethnicities'):
        logger.info('Ethnicities not created')
    mp = portal.manage_permission
    mp(AddEthnicity, ['Manager', 'Owner', 'LabManager', 'LabClerk'], 1)
    mp(ViewEthnicities, ['Manager', 'LabManager', 'Owner', 'LabClerk', 'Doctor', 'RegulatoryInspector'], 1)
    createEthnicities(tool)
    addPatientEthnicity(tool, patient_list)
    return True


def createEthnicities(context):
    """
    This function creates al the standard ethnicities
    :return: a list of tuples with the created ethnicities contents as: [(ethnicity_name, ethnicity_uid), (), ...]
    """
    ethnicities = [
     'Native American', 'Asian', 'Black', 'Native Hawaiian or Other Pacific Islander', 'White',
     'Hispanic or Latino']
    for ethnicityname in ethnicities:
        folder = context.bika_setup.bika_ethnicities
        _id = folder.invokeFactory('Ethnicity', id=tmpID())
        obj = folder[_id]
        obj.edit(title=ethnicityname, description='')
        obj.unmarkCreationFlag()
        renameAfterCreation(obj)


def addPatientEthnicity(context, patient_list):
    """
    This function adds to the patient, its ethnicity.
    :Patient_list: is a list of tuples. Each tuple contains a patient UID and a string. This string is the name of the
    ethnicity that used te be related in the patient.  [(patientUID, ethnicityName),(),...]
    :return: Ethnicity object
    """
    for patientUID, ethnicityname in patient_list:
        bsc = getToolByName(context, 'bika_setup_catalog')
        bpc = getToolByName(context, 'bika_patient_catalog')
        if len(bsc(Portal_type='Ethnicity', Title=ethnicityname)[0].getObject().UID()) == 1:
            ethnicityUID = bsc(Portal_type='Ethnicity', Title=ethnicityname)[0].getObject().UID()
            patient = bpc(Portal_type='Patient', UID=patientUID)[0].getObject()
            patient.setEthnicity(ethnicityUID)