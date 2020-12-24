# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/directconnect/connections.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 800 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class Connections(AWSResources):

    def __init__(self, facade, region):
        super(Connections, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_connections = await self.facade.directconnect.get_connections(self.region)
        for raw_connection in raw_connections:
            name, resource = self._parse_connection(raw_connection)
            self[name] = resource

    def _parse_connection(self, raw_connection):
        raw_connection['id'] = raw_connection.pop('connectionId')
        raw_connection['name'] = raw_connection.pop('connectionName')
        return (raw_connection['id'], raw_connection)