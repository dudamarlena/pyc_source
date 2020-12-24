# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/dockerfabric/api.py
# Compiled at: 2016-12-11 14:21:37
from __future__ import unicode_literals
from fabric.api import env
from .apiclient import DockerFabricApiConnections, ContainerApiFabricClient, DockerClientConfiguration
from .cli import DockerCliConnections, ContainerCliFabricClient, DockerCliConfig
CLIENT_API = b'API'
CLIENT_CLI = b'CLI'
docker_api = DockerFabricApiConnections().get_connection
docker_cli = DockerCliConnections().get_connection

def docker_fabric(*args, **kwargs):
    """
    :param args: Positional arguments to Docker client.
    :param kwargs: Keyword arguments to Docker client.
    :return: Docker client.
    :rtype: dockerfabric.apiclient.DockerFabricClient | dockerfabric.cli.DockerCliClient
    """
    ci = kwargs.get(b'client_implementation') or env.get(b'docker_fabric_implementation') or CLIENT_API
    if ci == CLIENT_API:
        return docker_api(*args, **kwargs)
    if ci == CLIENT_CLI:
        return docker_cli(*args, **kwargs)
    raise ValueError(b'Invalid client implementation.', ci)


def container_fabric(container_maps=None, docker_client=None, clients=None, client_implementation=None):
    """
    :param container_maps: Container map or a tuple / list thereof.
    :type container_maps: list[dockermap.map.config.main.ContainerMap] | dockermap.map.config.main.ContainerMap
    :param docker_client: Default Docker client instance.
    :type docker_client: dockerfabric.base.FabricClientConfiguration or docker.docker.Client
    :param clients: Optional dictionary of Docker client configuration objects.
    :type clients: dict[unicode | str, dockerfabric.base.FabricClientConfiguration]
    :param client_implementation: Client implementation to use (API or CLI).
    :type client_implementation: unicode | str
    :return: Container mapping client.
    :rtype: dockerfabric.base.FabricContainerClient
    """
    ci = client_implementation or env.get(b'docker_fabric_implementation') or CLIENT_API
    if ci == CLIENT_API:
        return ContainerApiFabricClient(container_maps, docker_client, clients)
    if ci == CLIENT_CLI:
        return ContainerCliFabricClient(container_maps, docker_client, clients)
    raise ValueError(b'Invalid client implementation.', ci)