# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/workflow/content.py
# Compiled at: 2012-06-26 16:56:38
from datetime import datetime
from persistent.dict import PersistentDict
import pytz
from zope.annotation.interfaces import IAnnotations
from zope.dublincore.interfaces import IZopeDublinCore
from zope.component import adapts, queryUtility
from zope.interface import implements
from hurry.workflow.interfaces import IWorkflowState
from ztfy.security.security import getSecurityManager
from ztfy.utils.date import unidate, parsedate
from ztfy.utils.traversing import getParent
from ztfy.workflow.interfaces import IWorkflow, IWorkflowTarget, IWorkflowContent
WORKFLOW_CONTENT_KEY = 'ztfy.workflow.content'
GMT = pytz.timezone('GMT')

class WorkflowContentAdapter(object):
    adapts(IWorkflowTarget)
    implements(IWorkflowContent)

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(self.context)
        data = annotations.get(WORKFLOW_CONTENT_KEY)
        if data is None:
            data = annotations[WORKFLOW_CONTENT_KEY] = PersistentDict()
        self.data = data
        return

    def _getStateDate(self):
        return parsedate(self.data.get('state_date')) or IZopeDublinCore(self.context).created

    def _setStateDate(self, date):
        if date and not date.tzinfo:
            date = GMT.localize(date)
        self.data['state_date'] = unidate(date)

    state_date = property(_getStateDate, _setStateDate)

    def _getStatePrincipal(self):
        return self.data.get('state_principal') or IZopeDublinCore(self.context).creators[0]

    def _setStatePrincipal(self, principal):
        self.data['state_principal'] = principal

    state_principal = property(_getStatePrincipal, _setStatePrincipal)

    def _getPublicationDate(self):
        return parsedate(self.data.get('publication_date'))

    def _setPublicationDate(self, date):
        if date and not date.tzinfo:
            date = GMT.localize(date)
        self.data['publication_date'] = unidate(date)

    publication_date = property(_getPublicationDate, _setPublicationDate)

    def _getFirstPublicationDate(self):
        return parsedate(self.data.get('first_publication_date'))

    def _setFirstPublicationDate(self, date):
        if date and not date.tzinfo:
            date = GMT.localize(date)
        self.data['first_publication_date'] = unidate(date)

    first_publication_date = property(_getFirstPublicationDate, _setFirstPublicationDate)

    def _getEffectiveDate(self):
        return IZopeDublinCore(self.context).effective

    def _setEffectiveDate(self, date):
        if date:
            if not date.tzinfo:
                date = GMT.localize(date)
            IZopeDublinCore(self.context).effective = date
            if self.first_publication_date is None or self.first_publication_date > date:
                self.first_publication_date = date
        else:
            if self.first_publication_date == self.publication_effective_date:
                self.first_publication_date = None
            if self.publication_effective_date:
                del IZopeDublinCore(self.context)._mapping['Date.Effective']
        return

    publication_effective_date = property(_getEffectiveDate, _setEffectiveDate)

    def _getExpirationDate(self):
        return IZopeDublinCore(self.context).expires

    def _setExpirationDate(self, date):
        if date:
            if not date.tzinfo:
                date = GMT.localize(date)
            IZopeDublinCore(self.context).expires = date
        elif self.publication_expiration_date:
            del IZopeDublinCore(self.context)._mapping['Date.Expires']

    publication_expiration_date = property(_getExpirationDate, _setExpirationDate)

    def isPublished(self):
        parent = getParent(self.context, IWorkflowTarget, allow_context=False)
        if parent is not None and not IWorkflowContent(parent).isPublished():
            return False
        else:
            workflow_name = IWorkflowTarget(self.context).workflow_name
            if not workflow_name:
                return True
            workflow = queryUtility(IWorkflow, workflow_name)
            if workflow is None or not workflow.published_states:
                return False
            if IWorkflowState(self.context).getState() not in workflow.published_states:
                return False
            now = datetime.now(pytz.UTC)
            return self.publication_effective_date is not None and self.publication_effective_date <= now and (self.publication_expiration_date is None or self.publication_expiration_date >= now)

    def isVisible(self):
        result = True
        sm = getSecurityManager(self.context)
        if sm is not None:
            result = sm.canView()
        return result and self.isPublished()