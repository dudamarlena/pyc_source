# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockermap/docker_api.py
# Compiled at: 2020-04-02 07:00:31
# Size of source mod 2**32: 1348 bytes
from __future__ import unicode_literals, absolute_import
import docker
CLIENT_FEATURES = [
 ('host_config', '1.15'),
 ('networks', '1.21'),
 ('volumes', '1.21'),
 ('container_update', '1.22'),
 ('stop_signal', '1.21')]
if docker.version_info[0] == 1:
    import docker.utils as docker_utils
    APIClient = docker.Client
    HostConfig = docker_utils.create_host_config
    NetworkingConfig = docker_utils.create_networking_config
    EndpointConfig = docker_utils.create_endpoint_config
    IPAMPool = docker_utils.create_ipam_pool
    IPAMConfig = docker_utils.create_ipam_config
    CLIENT_FEATURES.extend([
     ('stop_timeout', '100.0'),
     ('healthcheck', '100.0'),
     ('container_update_restart_policy', '100.0')])
    INSECURE_REGISTRIES = True
else:
    from docker import types as docker_types
    APIClient = docker.APIClient
    HostConfig = docker_types.HostConfig
    NetworkingConfig = docker_types.NetworkingConfig
    EndpointConfig = docker_types.EndpointConfig
    IPAMPool = docker_types.IPAMPool
    IPAMConfig = docker_types.IPAMConfig
    CLIENT_FEATURES.extend([
     ('stop_timeout', '1.25'),
     ('healthcheck', '1.24'),
     ('container_update_restart_policy', '1.23')])
    INSECURE_REGISTRIES = docker.version_info[0] < 3