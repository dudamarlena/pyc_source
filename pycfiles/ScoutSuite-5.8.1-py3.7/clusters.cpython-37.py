# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/redshift/clusters.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 735 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class Clusters(AWSResources):

    def __init__(self, facade, region, vpc):
        super(Clusters, self).__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_clusters = await self.facade.redshift.get_clusters(self.region, self.vpc)
        for raw_cluster in raw_clusters:
            id, cluster = self._parse_cluster(raw_cluster)
            self[id] = cluster

    def _parse_cluster(self, raw_cluster):
        name = raw_cluster.pop('ClusterIdentifier')
        raw_cluster['name'] = name
        return (
         name, raw_cluster)