# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/workflow/versions.py
# Compiled at: 2012-06-26 16:56:38
from hurry.query.interfaces import IQuery
from hurry.workflow.interfaces import IWorkflowVersions, IWorkflowState
from zope.component import getUtility
from zope.interface import implements
from hurry.query import And
from hurry.query.value import In, Eq
from hurry.workflow.workflow import WorkflowVersions as WorkflowVersionsBase
WF_STATE_INDEX = ('WorkflowCatalog', 'wf_state')
WF_IDS_INDEX = ('WorkflowCatalog', 'wf_id')

class WorkflowVersions(WorkflowVersionsBase):
    """Utility used to handle content versions"""
    implements(IWorkflowVersions)

    def getVersions(self, state=None, id=None, object=None):
        assert state is not None or id is not None or object is not None
        query = getUtility(IQuery)
        request = []
        if state is not None:
            if isinstance(state, tuple):
                request.append(In(WF_STATE_INDEX, state))
            else:
                request.append(Eq(WF_STATE_INDEX, state))
        if id is not None:
            request.append(Eq(WF_IDS_INDEX, id))
        elif object is not None:
            state = IWorkflowState(object, None)
            if state is not None:
                request.append(Eq(WF_IDS_INDEX, state.getId()))
        return query.searchResults(And(*request))

    def getVersionsWithAutomaticTransitions(self):
        return ()

    def hasVersion(self, state, id):
        return bool(self.getVersions(state, id))

    def hasVersionId(self, id):
        query = getUtility(IQuery)
        return bool(query.searchResults(Eq(WF_IDS_INDEX, id)))