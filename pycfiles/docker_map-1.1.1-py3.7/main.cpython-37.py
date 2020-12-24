# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockermap/map/state/update/main.py
# Compiled at: 2019-10-19 14:38:08
# Size of source mod 2**32: 3629 bytes
from __future__ import unicode_literals
import six
from ...input import CmdCheck
from ..base import DependencyStateGenerator
from .container import UpdateContainerState
from .network import UpdateNetworkState, NetworkEndpointRegistry
from .volume import ContainerLegacyVolumeChecker, ContainerVolumeChecker, VolumeUpdateState

class UpdateStateGenerator(DependencyStateGenerator):
    __doc__ = "\n    Generates states for updating configured containers. Before checking each configuration, for each image the latest\n    version is pulled from the registry, but only if :attr:`UpdateStateGenerator.pull_before_update` is set to ``True``.\n\n    An attached container is considered outdated, if its image id does not correspond with the current base\n    image, and :attr:`~ContainerUpdateMixin.update_persistent` is set to ``True``.\n    Any other container is considered outdated, if\n\n      - any of its attached volumes' paths does not match (i.e. they are not actually sharing the same virtual\n        file system), or\n      - the image id does not correspond with the configured image (e.g. because the image has been updated), or\n      - environment variables have been changed in the configuration, or\n      - command or entrypoint have been set or changed, or\n      - network ports differ from what is specified in the configuration.\n\n    In addition, the default state implementation applies, considering nonexistent containers or containers that\n    cannot be restarted.\n    "
    container_state_class = UpdateContainerState
    network_state_class = UpdateNetworkState
    volume_state_class = VolumeUpdateState
    update_persistent = False
    check_exec_commands = CmdCheck.FULL
    skip_limit_reset = False
    policy_options = ['update_persistent', 'check_exec_commands', 'skip_limit_reset']

    def __init__(self, policy, kwargs):
        super(UpdateStateGenerator, self).__init__(policy, kwargs)
        self._volume_checkers = {client_name:(ContainerVolumeChecker(policy) if client_config.features['volumes'] else ContainerLegacyVolumeChecker(policy)) for client_name, client_config in six.iteritems(policy.clients)}
        default_network_details = {client_name:{n_name:client_config.get_client().inspect_network(n_name) for n_name in policy.default_network_names if n_name in policy.network_names[client_name]} for client_name, client_config in six.iteritems(policy.clients) if client_config.features['networks']}
        self._network_registries = {client_name:NetworkEndpointRegistry(policy.nname, policy.cname, policy.get_hostname, policy.container_names[client_name], default_network_details[client_name]) for client_name, network_details in six.iteritems(default_network_details)}

    def get_container_state(self, client_name, *args, **kwargs):
        c_state = (super(UpdateStateGenerator, self).get_container_state)(client_name, *args, **kwargs)
        c_state.volume_checker = self._volume_checkers[client_name]
        c_state.endpoint_registry = self._network_registries.get(client_name)
        return c_state

    def get_network_state(self, client_name, *args, **kwargs):
        n_state = (super(UpdateStateGenerator, self).get_network_state)(client_name, *args, **kwargs)
        n_state.endpoint_registry = self._network_registries.get(client_name)
        return n_state