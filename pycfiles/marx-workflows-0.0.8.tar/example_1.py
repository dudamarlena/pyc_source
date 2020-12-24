# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nino/dev/marx/tests/workflow/example_1.py
# Compiled at: 2014-09-26 20:08:33
"""
This defines a workflow around the imperative: "Throw a Pie".

In a simple system this is about 5 lines of code. But in others,
where business logic requires the interaction of many systems,
logic is smeared around and duplicated, and not well encapsulated.

The approach here splits execution into discrete units which can be
composed into other workflows encouraging reuse, testability, etc.
"""
from marx.workflow.step import LogicUnit, ArgSpec, Step, ResultSpec
from marx.workflow.flow import Workflow
from marx.workflow.context import DefaultContext, Field
from tests.workflow.example_objects import User, PermissionDeniedError

class IsUserAuthorized(LogicUnit):
    """Checks permission for a user+action, and notifies authorities
    if it fails."""
    user = ArgSpec(User, docs='The user performing the action')

    def __init__(self, action):
        """
        @param action: The action that will be checked.
        """
        self.action = action

    def __call__(self, user):
        """
        @param user: The user performing the action.
        """
        if self.is_authorized(user):
            return
        self.notify_authorities(user, self.action)
        raise PermissionDeniedError(self.action)

    def is_authorized(self, user):
        return user.name in ('bob', 'mary')

    def notify_authorities(self, user, action):
        print 'AUTHORITIES!!!', user, ' attempted illegal action', self.action


class MakePie(LogicUnit):
    """Makes the pie."""
    maker = ArgSpec(User, docs='The person making pie.')
    pie = ResultSpec(basestring, docs='Kind of pie')

    def __call__(self, maker):
        maker.increment('pies_made', 1)
        self.result.pie = 'lemon'


class ThrowThing(LogicUnit):
    """Subject Object (Verb) Indirect-object"""
    actor = ArgSpec(User)
    hit = ResultSpec(bool, default=False, docs="Did we get 'em?")

    def __call__(self, actor, thing, target):
        actor.increment('things_throw')
        print 'Throwing', thing
        self.result.hit = actor.can_throw()
        return self.result


class ThrowPieContext(DefaultContext):
    """The execution context for the ThrowPieWorkflow."""
    thrower = Field(User, docs='Somebody has to throw it')
    target = Field(User, docs='At somebody')
    pie = Field(str, docs='A pie, which we make along the way')
    was_hit = Field(bool, docs='Success of the throwing event')


IsUserAuthorizedStep = Step(IsUserAuthorized('throw_pie'), arg_map={IsUserAuthorized.USER: ThrowPieContext.THROWER})
MakePieStep = Step(MakePie(), arg_map={MakePie.MAKER: ThrowPieContext.THROWER}, result_map=MakePie.ResultMap(ThrowPieContext))
ThrowThingStep = Step(ThrowThing(), arg_map=ThrowThing.AutoMap({ThrowThing.ACTOR: ThrowPieContext.THROWER, ThrowThing.THING: ThrowPieContext.PIE}), result_map={ThrowPieContext.WAS_HIT: 'hit'})
ThrowPieWorkflowA = Workflow(steps=[
 IsUserAuthorizedStep,
 MakePieStep,
 ThrowThingStep])
ThrowPieWorkflowB = Workflow().add_step(IsUserAuthorizedStep).add_step(MakePieStep).add_step(ThrowThingStep)
EmptyWorkflow = Workflow()
ThrowPieWorkflowC_A = EmptyWorkflow + IsUserAuthorizedStep + MakePieStep
ThrowPieWorkflowC_B = EmptyWorkflow + ThrowThingStep
ThrowPieWorkflowC = ThrowPieWorkflowC_A + ThrowPieWorkflowC_B

def run():
    """To execute a workflow, prepare a context, and pass it through."""
    ctx = ThrowPieContext()
    ctx.thrower = User('bob')
    ctx.target = User('frank')
    for WorkflowType in (ThrowPieWorkflowA,
     ThrowPieWorkflowB,
     ThrowPieWorkflowC):
        try:
            WorkflowType(ctx)
            assert ctx.was_hit is not None
            assert ctx.pie == 'lemon'
            return ctx
        except PermissionDeniedError:
            assert False

    assert EmptyWorkflow.steps == []
    assert ThrowThingStep not in ThrowPieWorkflowC_A.steps
    return