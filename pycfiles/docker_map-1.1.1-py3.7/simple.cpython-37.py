# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockermap/map/action/simple.py
# Compiled at: 2020-04-02 07:00:31
# Size of source mod 2**32: 10778 bytes
from __future__ import unicode_literals
from ..input import ItemType
from ..state import State, StateFlags
from . import ItemAction, Action, ContainerUtilAction, VolumeUtilAction, NetworkUtilAction, DerivedAction, ImageAction
from .base import AbstractActionGenerator

class CreateActionGenerator(AbstractActionGenerator):

    def get_state_actions(self, state, **kwargs):
        """
        Creates all missing containers, networks, and volumes.

        :param state: Configuration state.
        :type state: dockermap.map.state.ConfigState
        :param kwargs: Additional keyword arguments.
        :return: Actions on the client, map, and configurations.
        :rtype: list[dockermap.map.action.ItemAction]
        """
        if state.base_state == State.ABSENT:
            if state.config_id.config_type == ItemType.IMAGE:
                return [
                 ItemAction(state, ImageAction.PULL)]
            actions = [
             ItemAction(state, (Action.CREATE), extra_data=kwargs)]
            if state.config_id.config_type == ItemType.CONTAINER:
                actions.append(ItemAction(state, ContainerUtilAction.CONNECT_ALL))
            return actions


class StartActionGenerator(AbstractActionGenerator):

    def get_state_actions(self, state, **kwargs):
        """
        Generally starts containers that are not running. Attached containers are skipped unless they are initial.
        Attached containers are also prepared with permissions. Where applicable, exec commands are run in started
        instance containers.

        :param state: Configuration state.
        :type state: dockermap.map.state.ConfigState
        :param kwargs: Additional keyword arguments.
        :return: Actions on the client, map, and configurations.
        :rtype: list[dockermap.map.action.ItemAction]
        """
        config_type = state.config_id.config_type
        if config_type == ItemType.VOLUME:
            if state.base_state == State.PRESENT:
                if state.state_flags & StateFlags.INITIAL:
                    return [ItemAction(state, Action.START),
                     ItemAction(state, VolumeUtilAction.PREPARE)]
        if config_type == ItemType.CONTAINER:
            if state.base_state == State.PRESENT:
                return [
                 ItemAction(state, (Action.START), extra_data=kwargs),
                 ItemAction(state, ContainerUtilAction.EXEC_ALL)]


class RestartActionGenerator(AbstractActionGenerator):
    restart_exec_commands = False
    policy_options = ['restart_exec_commands']

    def get_state_actions(self, state, **kwargs):
        """
        Restarts instance containers.

        :param state: Configuration state.
        :type state: dockermap.map.state.ConfigState
        :param kwargs: Additional keyword arguments.
        :return: Actions on the client, map, and configurations.
        :rtype: list[dockermap.map.action.ItemAction]
        """
        if state.config_id.config_type == ItemType.CONTAINER:
            if state.base_state != State.ABSENT:
                if not state.state_flags & StateFlags.INITIAL:
                    actions = [
                     ItemAction(state, (DerivedAction.RESTART_CONTAINER), extra_data=kwargs)]
                    if self.restart_exec_commands:
                        actions.append(ItemAction(state, (ContainerUtilAction.EXEC_ALL), extra_data=kwargs))
                    return actions


class StopActionGenerator(AbstractActionGenerator):

    def get_state_actions(self, state, **kwargs):
        """
        Stops containers that are running. Does not check attached containers. Considers using the pre-configured
        ``stop_signal``.

        :param state: Configuration state.
        :type state: dockermap.map.state.ConfigState
        :param kwargs: Additional keyword arguments.
        :return: Actions on the client, map, and configurations.
        :rtype: list[dockermap.map.action.ItemAction]
        """
        if state.config_id.config_type == ItemType.CONTAINER:
            if state.base_state != State.ABSENT:
                if not state.state_flags & StateFlags.INITIAL:
                    return [
                     ItemAction(state, (ContainerUtilAction.SIGNAL_STOP), extra_data=kwargs)]


class RemoveActionGenerator(AbstractActionGenerator):
    remove_persistent = True
    remove_attached = False
    policy_options = ['remove_persistent', 'remove_attached']

    def get_state_actions(self, state, **kwargs):
        """
        Removes containers that are stopped. Optionally skips persistent containers. Attached containers are skipped
        by default from removal but can optionally be included.

        :param state: Configuration state.
        :type state: dockermap.map.state.ConfigState
        :param kwargs: Additional keyword arguments.
        :return: Actions on the client, map, and configurations.
        :rtype: list[dockermap.map.action.ItemAction]
        """
        config_type = state.config_id.config_type
        if config_type == ItemType.CONTAINER:
            extra_data = kwargs
        else:
            extra_data = None
        if state.base_state == State.PRESENT:
            if not (config_type == ItemType.VOLUME):
                return [
                 ItemAction(state, (Action.REMOVE), extra_data=extra_data)]
            if config_type == ItemType.NETWORK:
                connected_containers = state.extra_data.get('containers')
                if connected_containers:
                    actions = [
                     ItemAction(state, NetworkUtilAction.DISCONNECT_ALL, {'containers': connected_containers})]
                else:
                    actions = []
                actions.append(ItemAction(state, (Action.REMOVE), extra_data=kwargs))
                return actions


class StartupActionGenerator(AbstractActionGenerator):

    def get_state_actions(self, state, **kwargs):
        """
        A combination of CreateActionGenerator and StartActionGenerator - creates and starts containers where
        appropriate.

        :param state: Configuration state.
        :type state: dockermap.map.state.ConfigState
        :param kwargs: Additional keyword arguments.
        :return: Actions on the client, map, and configurations.
        :rtype: list[dockermap.map.action.ItemAction]
        """
        config_type = state.config_id.config_type
        if config_type == ItemType.VOLUME:
            if state.base_state == State.ABSENT:
                return [ItemAction(state, Action.CREATE),
                 ItemAction(state, VolumeUtilAction.PREPARE)]
            if state.base_state == State.PRESENT and state.state_flags & StateFlags.INITIAL:
                return [ItemAction(state, Action.START),
                 ItemAction(state, VolumeUtilAction.PREPARE)]
        elif config_type == ItemType.CONTAINER:
            if state.base_state == State.ABSENT:
                return [ItemAction(state, DerivedAction.STARTUP_CONTAINER),
                 ItemAction(state, ContainerUtilAction.EXEC_ALL)]
            if state.base_state == State.PRESENT:
                return [ItemAction(state, Action.START),
                 ItemAction(state, ContainerUtilAction.EXEC_ALL)]
        else:
            if config_type == ItemType.NETWORK:
                return [
                 ItemAction(state, Action.CREATE)]
            if config_type == ItemType.IMAGE:
                return [
                 ItemAction(state, ImageAction.PULL)]


class ShutdownActionGenerator(RemoveActionGenerator):

    def get_state_actions(self, state, **kwargs):
        """
        A combination of StopActionGenerator and RemoveActionGenerator - stops and removes containers where
        appropriate.

        :param state: Configuration state.
        :type state: dockermap.map.state.ConfigState
        :param kwargs: Additional keyword arguments.
        :return: Actions on the client, map, and configurations.
        :rtype: list[dockermap.map.action.ItemAction]
        """
        config_type = state.config_id.config_type
        if config_type == ItemType.NETWORK:
            if state.base_state == State.PRESENT:
                connected_containers = state.extra_data.get('containers')
                if connected_containers:
                    cc_names = [c.get('Name', c['Id']) for c in connected_containers]
                    actions = [
                     ItemAction(state, (NetworkUtilAction.DISCONNECT_ALL), extra_data={'containers': cc_names})]
                else:
                    actions = []
                actions.append(ItemAction(state, (Action.REMOVE), extra_data=kwargs))
                return actions
            else:
                pass
        if config_type == ItemType.VOLUME:
            if self.remove_attached:
                return [
                 ItemAction(state, Action.REMOVE)]
        if config_type == ItemType.CONTAINER:
            if not (self.remove_persistent or state.state_flags & StateFlags.PERSISTENT or state.base_state == State.RUNNING):
                if state.state_flags & StateFlags.RESTARTING:
                    return [
                     ItemAction(state, DerivedAction.SHUTDOWN_CONTAINER)]
                if state.base_state == State.PRESENT:
                    return [
                     ItemAction(state, Action.REMOVE)]
            elif state.base_state == State.RUNNING or state.state_flags & StateFlags.RESTARTING:
                return [
                 ItemAction(state, Action.REMOVE)]


class SignalActionGenerator(AbstractActionGenerator):

    def get_state_actions(self, state, **kwargs):
        """
        Sends kill signals to running containers.

        :param state: Configuration state.
        :type state: dockermap.map.state.ConfigState
        :param kwargs: Additional keyword arguments.
        :return: Actions on the client, map, and configurations.
        :rtype: list[dockermap.map.action.ItemAction]
        """
        if state.config_id.config_type == ItemType.CONTAINER:
            if state.base_state == State.RUNNING:
                return [
                 ItemAction(state, (Action.KILL), extra_data=kwargs)]


class ImagePullActionGenerator(AbstractActionGenerator):
    pull_all_images = True
    pull_insecure_registry = False
    policy_options = ['pull_all_images', 'pull_insecure_regsitry']

    def get_state_actions(self, state, **kwargs):
        pull_kwargs = {}
        if self.pull_insecure_registry:
            pull_kwargs['insecure_registry'] = self.pull_insecure_registry
        if state.config_id.config_type == ItemType.IMAGE:
            if self.pull_all_images or state.base_state == State.ABSENT:
                return [
                 ItemAction(state, (ImageAction.PULL), **pull_kwargs)]