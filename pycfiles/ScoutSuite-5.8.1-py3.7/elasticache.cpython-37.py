# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/facade/elasticache.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 3778 bytes
from asyncio import Lock
from botocore.exceptions import ClientError
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.utils import ec2_classic
from ScoutSuite.providers.utils import get_and_set_concurrently

class ElastiCacheFacade(AWSBaseFacade):
    regional_clusters_cache_locks = {}
    regional_subnets_cache_locks = {}
    clusters_cache = {}
    subnets_cache = {}

    async def get_clusters(self, region, vpc):
        await self.cache_clusters(region)
        return [cluster for cluster in self.clusters_cache[region] if cluster['VpcId'] == vpc]

    async def cache_clusters(self, region):
        async with self.regional_clusters_cache_locks.setdefault(region, Lock()):
            if region in self.clusters_cache:
                return
            self.clusters_cache[region] = await AWSFacadeUtils.get_all_pages('elasticache', region, self.session, 'describe_cache_clusters', 'CacheClusters')
            await get_and_set_concurrently([
             self._get_and_set_cluster_vpc],
              (self.clusters_cache[region]), region=region)

    async def _get_and_set_cluster_vpc(self, cluster: {}, region: str):
        if 'CacheSubnetGroupName' not in cluster:
            cluster['VpcId'] = ec2_classic
        else:
            subnets = await AWSFacadeUtils.get_all_pages('elasticache',
              region, (self.session), 'describe_cache_subnet_groups', 'CacheSubnetGroups', CacheSubnetGroupName=(cluster['CacheSubnetGroupName']))
            subnet_group = subnets[0]
            cluster['VpcId'] = subnet_group['VpcId']

    async def get_security_groups(self, region):
        client = AWSFacadeUtils.get_client('elasticache', self.session, region)
        try:
            return await AWSFacadeUtils.get_all_pages('elasticache', region, self.session, 'describe_cache_security_groups', 'CacheSecurityGroups')
        except client.exceptions.InvalidParameterValueException:
            pass
        except Exception as e:
            try:
                print_exception('Failed to get ElastiCache security groups: {}'.format(e))
            finally:
                e = None
                del e

        return []

    async def get_subnet_groups(self, region, vpc):
        await self.cache_subnets(region)
        return [subnet for subnet in self.subnets_cache[region] if subnet['VpcId'] == vpc]

    async def cache_subnets(self, region):
        async with self.regional_subnets_cache_locks.setdefault(region, Lock()):
            if region in self.subnets_cache:
                return
            self.subnets_cache[region] = await AWSFacadeUtils.get_all_pages('elasticache', region, self.session, 'describe_cache_subnet_groups', 'CacheSubnetGroups')

    async def get_parameter_groups(self, region):
        try:
            return await AWSFacadeUtils.get_all_pages('elasticache', region, self.session, 'describe_cache_parameter_groups', 'CacheParameterGroups')
        except ClientError as e:
            try:
                if e.response['Error']['Code'] != 'InvalidParameterValue':
                    print_exception('Failed to describe cache parameter groups: {}'.format(e))
                return []
            finally:
                e = None
                del e