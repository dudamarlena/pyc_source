# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/browser/worksheet/manageresults.py
# Compiled at: 2015-11-03 03:53:39
from Products.CMFCore.utils import getToolByName
from bika.health import bikaMessageFactory as _
from bika.health.browser.analysis.resultoutofrange import ResultOutOfRange
from bika.lims.browser.worksheet.views import ManageResultsView as BaseView

class ManageResultsView(BaseView):

    def __call__(self):
        workflow = getToolByName(self.context, 'portal_workflow')
        analyses = self.context.getAnalyses()
        for obj in analyses:
            obj = obj.getObject() if hasattr(obj, 'getObject') else obj
            astate = workflow.getInfoFor(obj, 'review_state')
            if astate == 'retracted':
                continue
            panic_alerts = ResultOutOfRange(obj)()
            if panic_alerts:
                translate = self.context.translate
                addPortalMessage = self.context.plone_utils.addPortalMessage
                message = translate(_('Some results exceeded the panic levels that may indicate an imminent life-threatening condition.'))
                addPortalMessage(message, 'warning')
                break

        return super(ManageResultsView, self).__call__()