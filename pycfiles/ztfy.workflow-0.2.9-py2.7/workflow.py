# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/workflow/workflow.py
# Compiled at: 2012-06-26 16:56:38
from zope.security.interfaces import NoInteraction, Unauthorized
from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState, ConditionFailedError
from ztfy.workflow.interfaces import IWorkflow, IWorkflowTarget, ITransition, ITransitionTarget
from zope.component import adapts, getUtility
from zope.event import notify
from zope.interface import Interface, implements
from zope.lifecycleevent import ObjectModifiedEvent
from zope.security.management import getInteraction
from zope.traversing.browser import absoluteURL
from hurry.workflow.workflow import nullCheckPermission, WorkflowTransitionEvent, WorkflowVersionTransitionEvent
from hurry.workflow.workflow import Workflow as WorkflowBase
from hurry.workflow.workflow import WorkflowInfo as WorkflowInfoBase, WorkflowState as WorkflowStateBase

class WorkflowStateAdapter(WorkflowStateBase):
    """Workflow state adapter implementing ILocation"""
    adapts(IWorkflowTarget)
    implements(IWorkflowState)


class WorkflowInfoAdapter(WorkflowInfoBase):
    """Enhanced IWorkflowInfo adapter handling several registered workflows"""
    adapts(IWorkflowTarget)
    implements(IWorkflowInfo)

    @property
    def name(self):
        return IWorkflowTarget(self.context).workflow_name

    def fireTransition(self, transition_id, comment=None, side_effect=None, check_security=True):
        state = IWorkflowState(self.context)
        wf = getUtility(IWorkflow, self.name)
        transition = wf.getTransition(state.getState(), transition_id)
        try:
            interaction = getInteraction()
        except NoInteraction:
            checkPermission = nullCheckPermission

        if check_security:
            checkPermission = interaction.checkPermission
        else:
            checkPermission = nullCheckPermission
        if not checkPermission(transition.permission, self.context):
            raise Unauthorized(self.context, 'transition: %s' % transition_id, transition.permission)
        if not transition.condition(self, self.context):
            raise ConditionFailedError
        result = transition.action(self, self.context)
        if result is not None:
            if transition.source is None:
                IWorkflowState(result).initialize()
            state = IWorkflowState(result)
            state.setId(IWorkflowState(self.context).getId())
            if side_effect is not None:
                side_effect(result)
            event = WorkflowVersionTransitionEvent(result, self.context, transition.source, transition.destination, transition, comment)
        else:
            if transition.source is None:
                IWorkflowState(self.context).initialize()
            if side_effect is not None:
                side_effect(self.context)
            event = WorkflowTransitionEvent(self.context, transition.source, transition.destination, transition, comment)
        state.setState(transition.destination)
        notify(event)
        if result is None:
            notify(ObjectModifiedEvent(self.context))
        else:
            notify(ObjectModifiedEvent(result))
        return result

    def getFireableTransitionIdsToward(self, state):
        wf = getUtility(IWorkflow, self.name)
        result = []
        for transition_id in self.getFireableTransitionIds():
            transition = wf.getTransitionById(transition_id)
            if transition.destination == state:
                result.append(transition_id)

        return result

    def _getTransitions(self, trigger):
        wf = getUtility(IWorkflow, self.name)
        transitions = wf.getTransitions(IWorkflowState(self.context).getState())
        return [ transition for transition in transitions if transition.trigger == trigger
               ]


class Workflow(WorkflowBase):
    """Custom workflow class"""
    implements(IWorkflow)

    def __init__(self, transitions, states, published_states=()):
        super(Workflow, self).__init__(transitions)
        self.states = states
        self.published_states = published_states


class WorkflowTransitionTargetAdapter(object):
    adapts(Interface, Interface, ITransition)
    implements(ITransitionTarget)

    def __init__(self, context, request, transition):
        self.context = context
        self.request = request
        self.transition = transition

    def absoluteURL(self):
        return '%s/++wf++%s' % (absoluteURL(self.context, self.request),
         self.transition.transition_id)