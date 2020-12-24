# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/workflow/tal/api.py
# Compiled at: 2012-07-12 02:08:15
__docformat__ = 'restructuredtext'
from hurry.workflow.interfaces import IWorkflowState
from zope.tales.interfaces import ITALESFunctionNamespace
from ztfy.workflow.interfaces import IWorkflow, IWorkflowTarget, IWorkflowContent
from ztfy.workflow.tal.interfaces import IWorkflowTalesAPI
from zope.component import queryUtility
from zope.i18n import translate
from zope.interface import implements
from ztfy.utils.traversing import getParent
from ztfy.workflow import _

class WorkflowTalesAdapter(object):
    implements(IWorkflowTalesAPI, ITALESFunctionNamespace)

    def __init__(self, context):
        self.context = context

    def setEngine(self, engine):
        self.request = engine.vars['request']

    def status(self):
        target = IWorkflowTarget(self.context, None)
        if target is None:
            return translate(_('None'), context=self.request)
        else:
            wf = queryUtility(IWorkflow, target.workflow_name)
            if wf is None:
                return translate(_('None'), context=self.request)
            state = IWorkflowState(self.context).getState()
            return translate(wf.states.getTerm(state).title, context=self.request)

    def published(self):
        if self.context is None:
            return False
        else:
            content = getParent(self.context, IWorkflowTarget)
            if content is None:
                return True
            return IWorkflowContent(content).isPublished()

    def visible(self):
        if self.context is None:
            return False
        else:
            content = getParent(self.context, IWorkflowTarget)
            if content is None:
                return True
            return IWorkflowContent(content).isVisible()