# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/boduch/subscription/state/transition.py
# Compiled at: 2009-08-14 17:29:30
"""This module defines subscription instances for state transition events."""
from boduch.event import subscribe, EventStateTransitionTransition
from boduch.handle import HandleStateTransitionTransition
SubStateTransitionTransition = subscribe(EventStateTransitionTransition, HandleStateTransitionTransition)
__all__ = [
 'SubStateTransitionTransition']