# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/browser/patient/batches.py
# Compiled at: 2014-12-12 07:13:54
from Products.CMFCore.utils import getToolByName
from bika.health.browser.batch.batchfolder import BatchFolderContentsView
from bika.health import bikaMessageFactory as _

class BatchesView(BatchFolderContentsView):

    def __init__(self, context, request):
        super(BatchesView, self).__init__(context, request)
        self.view_url = self.context.absolute_url() + '/batches'
        self.contentFilter['getPatientID'] = self.context.id
        self.columns['getPatientID']['toggle'] = False
        self.columns['getClientPatientID']['toggle'] = False
        self.columns['Patient']['toggle'] = False

    def __call__(self):
        self.context_actions[_('Add')] = {'url': self.portal.absolute_url() + '/batches/createObject?type_name=Batch', 
           'icon': self.portal.absolute_url() + '/++resource++bika.lims.images/add.png'}
        return BatchFolderContentsView.__call__(self)