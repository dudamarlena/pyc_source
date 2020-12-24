# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/vpc/peering_connections.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 845 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class PeeringConnections(AWSResources):

    def __init__(self, facade, region):
        super().__init__(facade)
        self.facade = facade
        self.region = region

    async def fetch_all(self):
        raw_peering_connections = await self.facade.ec2.get_peering_connections(self.region)
        for raw_peering_connection in raw_peering_connections:
            id, peering_connection = self._parse_peering_connections(raw_peering_connection)
            self[id] = peering_connection

    def _parse_peering_connections(self, raw_peering_connection):
        peering_connection_id = raw_peering_connection['VpcPeeringConnectionId']
        return (peering_connection_id, raw_peering_connection)