# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/browser/batch/batchfolder.py
# Compiled at: 2014-12-12 07:13:54
from Products.CMFCore.utils import getToolByName
from bika.health import bikaMessageFactory as _
from bika.lims.browser.batchfolder import BatchFolderContentsView as BaseView

class BatchFolderContentsView(BaseView):

    def __init__(self, context, request):
        super(BatchFolderContentsView, self).__init__(context, request)
        self.title = self.context.translate(_('Cases'))
        self.columns = {'BatchID': {'title': _('Case ID')}, 'getPatientID': {'title': _('Patient ID'), 'toggle': True}, 'getClientPatientID': {'title': _('Client PID'), 'toggle': True}, 'Patient': {'title': _('Patient')}, 'Doctor': {'title': _('Doctor')}, 'Client': {'title': _('Client')}, 'OnsetDate': {'title': _('Onset Date')}, 'state_title': {'title': _('State'), 'sortable': False}}
        self.review_states = [
         {'id': 'default', 'contentFilter': {'review_state': 'open', 'cancellation_state': 'active', 
                              'sort_on': 'created', 
                              'sort_order': 'reverse'}, 
            'title': _('Open'), 
            'transitions': [{'id': 'close'}, {'id': 'cancel'}], 'columns': [
                      'BatchID',
                      'Patient',
                      'getPatientID',
                      'getClientPatientID',
                      'Doctor',
                      'Client',
                      'OnsetDate',
                      'state_title']},
         {'id': 'closed', 'contentFilter': {'review_state': 'closed', 'cancellation_state': 'active', 
                              'sort_on': 'created', 
                              'sort_order': 'reverse'}, 
            'title': _('Closed'), 
            'transitions': [{'id': 'open'}], 'columns': [
                      'BatchID',
                      'Patient',
                      'getPatientID',
                      'getClientPatientID',
                      'Doctor',
                      'Client',
                      'OnsetDate',
                      'state_title']},
         {'id': 'cancelled', 'title': _('Cancelled'), 
            'transitions': [{'id': 'reinstate'}], 'contentFilter': {'cancellation_state': 'cancelled', 'sort_on': 'created', 
                              'sort_order': 'reverse'}, 
            'columns': [
                      'BatchID',
                      'Patient',
                      'getPatientID',
                      'getClientPatientID',
                      'Doctor',
                      'Client',
                      'OnsetDate',
                      'state_title']},
         {'id': 'all', 'title': _('All'), 
            'transitions': [], 'contentFilter': {'sort_on': 'created', 'sort_order': 'reverse'}, 
            'columns': [
                      'BatchID',
                      'Patient',
                      'getPatientID',
                      'getClientPatientID',
                      'Doctor',
                      'Client',
                      'OnsetDate',
                      'state_title']}]

    def folderitems(self):
        self.filter_indexes = None
        items = BaseView.folderitems(self)
        pm = getToolByName(self.context, 'portal_membership')
        member = pm.getAuthenticatedMember()
        roles = member.getRoles()
        hidepatientinfo = 'Manager' not in roles and 'LabManager' not in roles and 'LabClerk' not in roles
        hideclientlink = 'RegulatoryInspector' in roles and 'Manager' not in roles and 'LabManager' not in roles and 'LabClerk' not in roles
        if hidepatientinfo:
            del self.columns['getPatientID']
            del self.columns['Patient']
            del self.columns['getClientPatientID']
            for rs in self.review_states:
                del rs['columns'][rs['columns'].index('getClientPatientID')]
                del rs['columns'][rs['columns'].index('Patient')]
                del rs['columns'][rs['columns'].index('getPatientID')]

        for x in range(len(items)):
            if 'obj' not in items[x]:
                continue
            obj = items[x]['obj']
            bid = obj.getBatchID()
            items[x]['BatchID'] = bid
            client = obj.Schema()['Client'].get(obj)
            doctor = obj.Schema()['Doctor'].get(obj)
            items[x]['Doctor'] = doctor and doctor.Title() or ''
            items[x]['replace']['Doctor'] = doctor and "<a href='%s'>%s</a>" % (
             doctor.absolute_url(),
             doctor.Title()) or ''
            items[x]['Client'] = client and client.Title() or ''
            if hideclientlink == False:
                items[x]['replace']['Client'] = client and "<a href='%s'>%s</a>" % (
                 client.absolute_url(),
                 client.Title()) or ''
            OnsetDate = obj.Schema()['OnsetDate'].get(obj)
            items[x]['replace']['OnsetDate'] = OnsetDate and self.ulocalized_time(OnsetDate) or ''
            if hidepatientinfo == False:
                patient = obj.Schema()['Patient'].get(obj)
                items[x]['Patient'] = patient and patient or ''
                items[x]['replace']['Patient'] = patient and "<a href='%s'>%s</a>" % (
                 patient.absolute_url(),
                 patient.Title()) or ''
                items[x]['getClientPatientID'] = patient and patient.getClientPatientID() or ''
                items[x]['replace']['getClientPatientID'] = patient and "<a href='%s'>%s</a>" % (
                 patient.absolute_url(),
                 items[x]['getClientPatientID']) or ''
                items[x]['getPatientID'] = patient and patient.id or ''
                items[x]['replace']['getPatientID'] = patient and "<a href='%s'>%s</a>" % (
                 patient.absolute_url(),
                 items[x]['getPatientID']) or ''

        return items