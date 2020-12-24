# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/facade/route53.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1379 bytes
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils

class Route53Facade(AWSBaseFacade):

    async def get_domains(self, region):
        try:
            return await AWSFacadeUtils.get_all_pages('route53domains', region, self.session, 'list_domains', 'Domains')
        except Exception as e:
            try:
                print_exception('Failed to get Route53 domains: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_hosted_zones(self):
        try:
            return await AWSFacadeUtils.get_all_pages('route53', None, self.session, 'list_hosted_zones', 'HostedZones')
        except Exception as e:
            try:
                print_exception('Failed to get Route53 hosted zones: {}'.format(e))
            finally:
                e = None
                del e

    async def get_resource_records(self, hosted_zone_id):
        try:
            return await AWSFacadeUtils.get_all_pages('route53', None, (self.session), 'list_resource_record_sets',
              'ResourceRecordSets', HostedZoneId=hosted_zone_id)
        except Exception as e:
            try:
                print_exception('Failed to get Route53 resource records: {}'.format(e))
            finally:
                e = None
                del e