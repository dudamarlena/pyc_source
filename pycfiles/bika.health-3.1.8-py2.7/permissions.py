# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/permissions.py
# Compiled at: 2015-11-03 03:53:19
"""All permissions are defined here.
They are also defined in permissions.zcml.
The two files must be kept in sync.

bika.health.__init__ imports * from this file, so
bika.health.PermName or bika.health.permissions.PermName are
both valid.

"""
AddPatient = 'BIKA: Add Patient'
AddDoctor = 'BIKA: Add Doctor'
AddAetiologicAgent = 'BIKA: Add AetiologicAgent'
AddTreatment = 'BIKA: AddTreatment'
AddDrug = 'BIKA: Add Drug'
AddImmunization = 'BIKA: Add Immunization'
AddVaccinationCenter = 'BIKA: Add VaccinationCenter'
AddSymptom = 'BIKA: Add Symptom'
AddDrugProhibition = 'BIKA: Add DrugProhibition'
AddInsuranceCompany = 'BIKA: Add InsuranceCompany'
AddEthnicity = 'BIKA: Add Ethnicity'
ADD_CONTENT_PERMISSIONS = {'Doctor': AddDoctor, 
   'Patient': AddPatient, 
   'AetiologicAgent': AddAetiologicAgent, 
   'Treatment': AddTreatment, 
   'Drug': AddDrug, 
   'Immunization': AddImmunization, 
   'VaccinationCenter': AddVaccinationCenter, 
   'Symptom': AddSymptom, 
   'DrugProhibition': AddDrugProhibition, 
   'InsuranceCompany': AddInsuranceCompany, 
   'Ethnicity': AddEthnicity}
ManageDoctors = 'BIKA: Manage Doctors'
ViewBatches = 'BIKA: View Batches'
ViewSamples = 'BIKA: View Samples'
ViewAnalysisRequests = 'BIKA: View AnalysisRequests'
ViewInsuranceCompanies = 'BIKA: View InsuranceCompanies'
ViewEthnicities = 'BIKA: View Ethnicities'
ViewPatients = 'BIKA: View Patients'
EditPatient = 'BIKA: Edit Patient'