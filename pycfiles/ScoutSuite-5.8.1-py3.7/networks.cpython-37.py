# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/gcp/resources/gce/networks.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1440 bytes
from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade

class Networks(Resources):

    def __init__(self, facade, project_id):
        super(Networks, self).__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_networks = await self.facade.gce.get_networks(self.project_id)
        for raw_network in raw_networks:
            network_id, network = self._parse_network(raw_network)
            self[network_id] = network

    def _parse_network(self, raw_network):
        network_dict = {}
        network_dict['id'] = raw_network['id']
        network_dict['project_id'] = raw_network['selfLink'].split('/')[(-4)]
        network_dict['name'] = raw_network['name']
        network_dict['description'] = self._get_description(raw_network)
        network_dict['creation_timestamp'] = raw_network['creationTimestamp']
        network_dict['network_url'] = raw_network['selfLink']
        network_dict['subnetwork_urls'] = raw_network.get('subnetworks', None)
        network_dict['auto_subnet'] = raw_network.get('autoCreateSubnetworks', None)
        network_dict['routing_config'] = raw_network['routingConfig']
        return (network_dict['id'], network_dict)

    def _get_description(self, raw_network):
        description = raw_network.get('description')
        if description:
            return description
        return 'N/A'