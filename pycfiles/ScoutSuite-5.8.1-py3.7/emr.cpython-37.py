# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/facade/emr.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1152 bytes
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import map_concurrently, run_concurrently

class EMRFacade(AWSBaseFacade):

    async def get_clusters(self, region):
        try:
            cluster_list = await AWSFacadeUtils.get_all_pages('emr', region, self.session, 'list_clusters', 'Clusters')
            cluster_ids = [cluster['Id'] for cluster in cluster_list]
        except Exception as e:
            try:
                print_exception('Failed to get EMR clusterss: {}'.format(e))
                return []
            finally:
                e = None
                del e

        else:
            return await map_concurrently((self._get_cluster), cluster_ids, region=region)

    async def _get_cluster(self, cluster_id: str, region: str):
        client = AWSFacadeUtils.get_client('emr', self.session, region)
        try:
            return await run_concurrently(lambda : client.describe_cluster(ClusterId=cluster_id)['Cluster'])
        except Exception as e:
            try:
                print_exception('Failed to describe EMR cluster: {}'.format(e))
                raise
            finally:
                e = None
                del e