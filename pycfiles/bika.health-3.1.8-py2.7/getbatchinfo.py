# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/browser/batch/getbatchinfo.py
# Compiled at: 2014-12-12 07:13:54
from Products.CMFCore.utils import getToolByName
from bika.health import bikaMessageFactory as _
from bika.lims import bikaMessageFactory as _b
from bika.lims.browser import BrowserView
from bika.lims.permissions import *
import json, plone

class ajaxGetBatchInfo(BrowserView):
    """ Grab the details for Doctor, Patient, Hospital (Titles).
    """

    def __call__(self):
        plone.protect.CheckAuthenticator(self.request)
        batch = self.context
        client = batch.Schema()['Client'].get(batch)
        doctor = batch.Schema()['Doctor'].get(batch)
        patient = batch.Schema()['Patient'].get(batch)
        ret = {'ClientID': client and client.getClientID() or '', 'ClientSysID': client and client.id or '', 
           'ClientUID': client and client.UID() or '', 
           'ClientTitle': client and client.Title() or '', 
           'PatientID': patient and patient.getPatientID() or '', 
           'PatientUID': patient and patient.UID() or '', 
           'PatientTitle': patient and patient.Title() or '', 
           'ClientPatientID': patient and patient.getClientPatientID() or '', 
           'DoctorID': doctor and doctor.getDoctorID(), 
           'DoctorUID': doctor and doctor.UID() or '', 
           'DoctorTitle': doctor and doctor.Title() or ''}
        return json.dumps(ret)