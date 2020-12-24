# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/browser/sample/getsamplepatient.py
# Compiled at: 2015-11-03 03:53:19
from Products.ZCTextIndex.ParseTree import ParseError
from bika.lims.browser import BrowserView
from Products.CMFCore.utils import getToolByName
import plone, json

class ajaxGetSamplePatient(BrowserView):
    """ Returns the patient assigned to the newest AnalysisRequest with
        a patient assigned.
    """

    def __call__(self):
        plone.protect.CheckAuthenticator(self.request)
        uid = self.request.get('uid', '')
        ret = {}
        if uid:
            uc = getToolByName(self.context, 'uid_catalog')
            proxies = uc(UID=uid)
            if proxies and len(proxies) > 0:
                sample = proxies[0].getObject()
                prefix = sample.getSampleType().getPrefix()
                ars = sample.getAnalysisRequests()
                ars = dict((ar.id, ar) for ar in ars)
                for key in sorted(ars, key=lambda key: ars[key]):
                    ar = ars[key]
                    patient = ar.Schema().getField('Patient').get(ar) if 'Patient' in ar.Schema() else None
                    if patient:
                        PR = patient.getPrimaryReferrer()
                        ret = {'PatientID': patient.getPatientID(), 'PatientUID': patient.UID(), 
                           'ClientPatientID': patient.getClientPatientID(), 
                           'ClientID': PR and PR.getClientID() or '', 
                           'ClientUID': PR and PR.UID() or '', 
                           'ClientTitle': PR and PR.Title() or '', 
                           'ClientSysID': PR and PR.id or '', 
                           'PatientFullname': patient.Title(), 
                           'PatientBirthDate': self.ulocalized_time(patient.getBirthDate()), 
                           'PatientGender': patient.getGender(), 
                           'PatientMenstrualStatus': patient.getMenstrualStatus()}
                        break

        return json.dumps(ret)