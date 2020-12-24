# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/dockerfabric/utils/base.py
# Compiled at: 2015-01-05 09:31:37
from __future__ import unicode_literals
import six
from fabric.api import env
from fabric.network import needs_host

@needs_host
def get_current_roles():
    """
    Determines the list of roles, that the current host is assigned to. If ``env.roledefs`` is not set, an empty list
    is returned.

    :return: List of roles of the current host.
    :rtype: list
    """
    current_host = env.host_string
    roledefs = env.get(b'roledefs')
    if roledefs:
        return [ role for role, hosts in six.iteritems(roledefs) if current_host in hosts ]
    return []


def get_role_addresses(role_name, interface_name):
    roledefs = env.get(b'roledefs')
    clients = env.get(b'docker_clients')
    if roledefs and clients:
        role_hosts = roledefs.get(role_name)
        if role_hosts:
            return set(client_config.interfaces[interface_name] for client_name, client_config in six.iteritems(clients) if client_config.get(b'fabric_host') in role_hosts)
    return set()