# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/boduch/subscription/state/machine.py
# Compiled at: 2009-08-14 17:29:30
__doc__ = 'This module defines subscription instances for state machine events.'
from boduch.event import subscribe, EventStateMachineAddState, EventStateMachineAddTransition, EventStateMachineRemoveState, EventStateMachineChangeState, EventStateMachineTransition, EventStateMachineEqual
from boduch.handle import HandleStateMachineAddState, HandleStateMachineAddTransition, HandleStateMachineRemoveState, HandleStateMachineChangeState, HandleStateMachineTransition, HandleStateMachineEqual
SubStateMachineAddState = subscribe(EventStateMachineAddState, HandleStateMachineAddState)
SubStateMachineAddTransition = subscribe(EventStateMachineAddTransition, HandleStateMachineAddTransition)
SubStateMachineRemoveState = subscribe(EventStateMachineRemoveState, HandleStateMachineRemoveState)
SubStateMachineChangeState = subscribe(EventStateMachineChangeState, HandleStateMachineChangeState)
SubStateMachineTransition = subscribe(EventStateMachineTransition, HandleStateMachineTransition)
SubStateMachineEqual = subscribe(EventStateMachineEqual, HandleStateMachineEqual)
__all__ = [
 'SubStateMachineAddState', 'SubStateMachineAddTransition',
 'SubStateMachineRemoveState', 'SubStateMachineChangeState',
 'SubStateMachineTransition', 'SubStateMachineEqual']