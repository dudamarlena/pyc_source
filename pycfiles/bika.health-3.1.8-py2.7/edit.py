# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/browser/sample/edit.py
# Compiled at: 2014-12-12 07:13:54
from Products.CMFCore.utils import getToolByName
from bika.health import bikaMessageFactory as _
from bika.lims.browser.sample import SampleEdit as BaseClass

class SampleEditView(BaseClass):
    """ Overrides bika.lims.browser.sample.SampleEdit
        Shows additional information to be edited about the Patient
    """

    def __call__(self):
        super(SampleEditView, self).__call__()
        pm = getToolByName(self.context, 'portal_membership')
        member = pm.getAuthenticatedMember()
        roles = member.getRoles()
        if 'Manager' in roles or 'LabManager' in roles or 'LabClerk' in roles:
            if self.context.portal_type == 'AnalysisRequest':
                ar = self.context
            else:
                wf = getToolByName(self.context, 'portal_workflow')
                rawars = self.context.getAnalysisRequests()
                ars = [ ar for ar in rawars if wf.getInfoFor(ar, 'review_state') != 'invalid'
                      ]
                if len(ars) == 0 and len(rawars) > 0:
                    ar = rawars[(len(rawars) - 1)]
                elif len(ars) > 1:
                    ar = ars[(len(ars) - 1)]
                elif len(ars) == 1:
                    ar = ars[0]
        return self.template()