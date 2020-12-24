# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/workflow/events.py
# Compiled at: 2012-06-26 16:56:38
__docformat__ = 'restructuredtext'
import pytz
from datetime import datetime
from hurry.workflow.interfaces import IWorkflowTransitionEvent
from ztfy.comment.interfaces import IComments
from ztfy.utils.request import getRequest
from ztfy.workflow.interfaces import IWorkflow, IWorkflowTarget, IWorkflowContent
from zope.component import adapter, getUtility
from zope.i18n import translate
from ztfy.workflow import _

@adapter(IWorkflowTarget, IWorkflowTransitionEvent)
def handleWorkflowTransition(object, event):
    request = getRequest()
    content = IWorkflowContent(object, None)
    if content is not None:
        content.state_date = datetime.now(pytz.UTC)
        content.state_principal = request.principal.id
    wf = getUtility(IWorkflow, IWorkflowTarget(object).workflow_name)
    if event.source is not None:
        comment = translate(_('Changed state: from %s to %s'), context=request) % (translate(wf.states.getTerm(event.source).title, context=request),
         translate(wf.states.getTerm(event.destination).title, context=request))
    else:
        comment = translate(_('New state: %s'), context=request) % translate(wf.states.getTerm(event.destination).title, context=request)
    if event.comment:
        comment += '\n%s' % event.comment
    comments = IComments(object)
    comments.addComment(body=comment, renderer='zope.source.plaintext', tags='__workflow__')
    return