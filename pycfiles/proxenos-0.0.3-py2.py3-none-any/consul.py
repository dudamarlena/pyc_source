# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dave/Projects/Github/proxenos/src/proxenos/mappers/consul.py
# Compiled at: 2017-01-23 19:49:52
"""Provides data mappers for Consul service discovery."""
from __future__ import absolute_import
import consulate, proxenos.mappers.base, proxenos.node
__all__ = ('ConsulClusterMapper', )

class ConsulClusterMapper(proxenos.mappers.base.BaseClusterMapper):
    """Reads service socket addresses from Consul."""

    def make_connection(self):
        """Initializes a Consul connection with :mod:`consulate`."""
        return consulate.Consul(host=self.host, port=self.port)

    def update(self):
        """Reads services from a Consul catalog into a cluster."""
        self.cluster.clear()
        service_names = [ service for dc in self._conn.catalog.services() for service in dc
                        ]
        for service in service_names:
            for node in self._conn.catalog.service(service):
                socket_address = proxenos.node.SocketAddress(node['ServiceAddress'], node['ServicePort'])
                self.cluster.add(proxenos.node.Service(name=node['ServiceName'], socket_address=socket_address, tags=node['ServiceTags']))