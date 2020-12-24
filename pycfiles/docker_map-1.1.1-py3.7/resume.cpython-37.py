# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockermap/map/action/resume.py
# Compiled at: 2019-10-19 14:38:08
# Size of source mod 2**32: 3449 bytes
from __future__ import unicode_literals
from ..input import ItemType
from ..state import State, StateFlags
from . import ItemAction, Action, VolumeUtilAction, ContainerUtilAction, DerivedAction
from .base import AbstractActionGenerator

class ResumeActionGenerator(AbstractActionGenerator):

    def __init__(self, *args, **kwargs):
        (super(ResumeActionGenerator, self).__init__)(*args, **kwargs)
        self.recreated_volumes = set()

    def get_state_actions(self, state, **kwargs):
        """
        Attached containers are created and prepared, if they are missing. They are re-created if they have terminated
        with errors. Instance containers are created if missing, started if stopped, and re-created / started if an
        attached container has been missing.

        :param state: Configuration state.
        :type state: dockermap.map.state.ConfigState
        :param kwargs: Additional keyword arguments.
        :return: Actions on the client, map, and configurations.
        :rtype: list[dockermap.map.action.ItemAction]
        """
        config_type = state.config_id.config_type
        config_tuple = (state.client_name, state.config_id.map_name, state.config_id.config_name)
        if config_type == ItemType.VOLUME:
            if state.base_state == State.ABSENT:
                action = Action.CREATE
                self.recreated_volumes.add(config_tuple)
            else:
                if state.state_flags & StateFlags.NONRECOVERABLE:
                    action = DerivedAction.RESET_VOLUME
                    self.recreated_volumes.add(config_tuple)
                else:
                    if state.state_flags & StateFlags.INITIAL:
                        action = Action.START
                    else:
                        return
            return [
             ItemAction(state, action),
             ItemAction(state, VolumeUtilAction.PREPARE)]
            if config_type == ItemType.CONTAINER:
                if config_tuple in self.recreated_volumes:
                    if state.base_state == State.ABSENT:
                        action = DerivedAction.STARTUP_CONTAINER
                elif state.base_state == State.RUNNING:
                    action = DerivedAction.RESET_CONTAINER
                else:
                    if state.base_state == State.PRESENT:
                        if state.base_state & StateFlags.INITIAL:
                            action = Action.START
                    else:
                        action = DerivedAction.RELAUNCH_CONTAINER
            else:
                return
        else:
            pass
        if state.base_state == State.ABSENT:
            action = DerivedAction.STARTUP_CONTAINER
        else:
            if state.state_flags & StateFlags.NONRECOVERABLE:
                action = DerivedAction.RESET_CONTAINER
            else:
                if state.base_state != State.RUNNING:
                    if not state.state_flags & StateFlags.INITIAL:
                        action = state.state_flags & StateFlags.PERSISTENT or Action.START
                    else:
                        return
                else:
                    return [
                     ItemAction(state, action),
                     ItemAction(state, ContainerUtilAction.EXEC_ALL)]
                    if config_type == ItemType.NETWORK and state.base_state == State.ABSENT:
                        return [
                         ItemAction(state, Action.CREATE)]