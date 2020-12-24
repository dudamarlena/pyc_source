# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/boduch/subscription/state/transition.py
# Compiled at: 2009-08-14 17:29:30
__doc__ = 'This module defines subscription instances for state transition events.'
from boduch.event import subscribe, EventStateTransitionTransition
from boduch.handle import HandleStateTransitionTransition
SubStateTransitionTransition = subscribe(EventStateTransitionTransition, HandleStateTransitionTransition)
__all__ = [
 'SubStateTransitionTransition']