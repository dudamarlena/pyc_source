# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/workflow/browser/namespace.py
# Compiled at: 2012-09-19 17:26:43
__docformat__ = 'restructuredtext'
from zope.traversing.interfaces import TraversalError
from hurry.workflow.interfaces import IWorkflowState, InvalidTransitionError
from ztfy.workflow.interfaces import IWorkflow, IWorkflowTarget
from zope.component import getUtility, queryMultiAdapter
from zope.interface import Interface
from zope.traversing import namespace

class WorkflowNamespaceTraverser(namespace.view):
    """Workflow namespace traverser"""

    def traverse(self, name, ignored):
        try:
            workflow = getUtility(IWorkflow, IWorkflowTarget(self.context).workflow_name)
            state = IWorkflowState(self.context).getState()
            transition = workflow.getTransition(state, name)
            view_name = transition.user_data.get('view')
            if view_name is not None:
                view = queryMultiAdapter((self.context, self.request), Interface, view_name)
                if view is not None:
                    view.transition = transition
                    return view
        except InvalidTransitionError as e:
            view = queryMultiAdapter((e, self.request), Interface, 'index.html')
            if view is not None:
                return view

        raise TraversalError('++wf++%s' % name)
        return