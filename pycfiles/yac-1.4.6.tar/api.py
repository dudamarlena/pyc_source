# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/container/api.py
# Compiled at: 2017-11-16 20:28:41
import json
from docker import Client

def get_connection_str(host, port=5555):
    return 'http://%s:%s' % (host, port)


def get_docker_client(connection_str='unix://var/run/docker.sock'):
    return Client(version='auto', base_url=connection_str)


def find_container_by_name(container_name, connection_str='unix://var/run/docker.sock'):
    client = get_docker_client(connection_str)
    containers = client.containers(all=True)
    null_container = {}
    for container in containers:
        if container and 'Names' in container and container['Names']:
            for this_name in container['Names']:
                if this_name and container_name in this_name:
                    return container

    return null_container


def find_container_by_image(container_image, connection_str='unix://var/run/docker.sock'):
    client = get_docker_client(connection_str)
    containers = client.containers(all=True)
    to_ret = {}
    for container in containers:
        if 'Image' in container and container['Image']:
            if container_image in container['Image'] and 'Up' in container['Status']:
                to_ret = container
                break

    return to_ret