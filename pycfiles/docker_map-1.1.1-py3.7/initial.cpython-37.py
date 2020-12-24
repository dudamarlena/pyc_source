# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockermap/map/state/initial.py
# Compiled at: 2019-10-19 14:38:08
# Size of source mod 2**32: 1059 bytes
from __future__ import unicode_literals
from . import State, StateFlags
from .base import DependencyStateGenerator, AbstractState

class InitialState(AbstractState):
    __doc__ = '\n    Assumes every item to be absent. This is intended for testing and situations where the actual state\n    cannot be determined.\n    '

    def inspect(self):
        pass

    def get_state(self):
        return (
         State.ABSENT, StateFlags.NONE, {})


class PresentState(AbstractState):
    __doc__ = '\n    Assumes every item to be present. This is intended for testing and situations where the actual state\n    cannot be determined.\n    '

    def inspect(self):
        pass

    def get_state(self):
        return (
         State.PRESENT, StateFlags.NONE, {})


class InitialStateGenerator(DependencyStateGenerator):
    container_state_class = InitialState
    network_state_class = InitialState
    volume_state_class = InitialState
    image_state_class = PresentState