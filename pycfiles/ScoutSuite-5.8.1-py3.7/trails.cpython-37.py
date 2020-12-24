# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/cloudtrail/trails.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 3152 bytes
import time
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id

class Trails(AWSResources):

    def __init__(self, facade, region):
        super(Trails, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_trails = await self.facade.cloudtrail.get_trails(self.region)
        for raw_trail in raw_trails:
            name, resource = self._parse_trail(raw_trail)
            self[name] = resource

    def _parse_trail(self, raw_trail):
        trail = {'name': raw_trail.pop('Name')}
        trail_id = get_non_provider_id(trail['name'])
        if 'IsMultiRegionTrail' in raw_trail:
            if raw_trail['IsMultiRegionTrail']:
                if raw_trail['HomeRegion'] != self.region:
                    for key in ('HomeRegion', 'TrailARN'):
                        trail[key] = raw_trail[key]

                    trail['scout_link'] = 'services.cloudtrail.regions.%s.trails.%s' % (raw_trail['HomeRegion'], trail_id)
                    return (trail_id, trail)
        for key in raw_trail:
            trail[key] = raw_trail[key]

        trail['bucket_id'] = get_non_provider_id(trail.pop('S3BucketName'))
        for key in ('IsMultiRegionTrail', 'LogFileValidationEnabled'):
            if key not in trail:
                trail[key] = False

        for key in ('KMSKeyId', 'IsLogging', 'LatestDeliveryTime', 'LatestDeliveryError',
                    'StartLoggingTime', 'StopLoggingTime', 'LatestNotificationTime',
                    'LatestNotificationError', 'LatestCloudWatchLogsDeliveryError',
                    'LatestCloudWatchLogsDeliveryTime'):
            trail[key] = trail[key] if key in trail else None

        trail['wildcard_data_logging'] = self.data_logging_status(trail)
        for event_selector in trail['EventSelectors']:
            trail['DataEventsEnabled'] = len(event_selector['DataResources']) > 0
            trail['ManagementEventsEnabled'] = event_selector['IncludeManagementEvents']

        return (trail_id, trail)

    def data_logging_status(self, trail):
        for event_selector in trail['EventSelectors']:
            has_wildcard = {'Values':[
              'arn:aws:s3'], 
             'Type':'AWS::S3::Object'} in event_selector['DataResources'] or {'Values':[
              'arn:aws:lambda'], 
             'Type':'AWS::Lambda::Function'} in event_selector['DataResources']
            is_logging = trail['IsLogging']
            if has_wildcard and is_logging and self.is_fresh(trail):
                return True

        return False

    @staticmethod
    def is_fresh(trail_details):
        if trail_details.get('LatestCloudWatchLogsDeliveryTime'):
            delivery_time = trail_details.get('LatestCloudWatchLogsDeliveryTime').strftime('%s')
            delivery_age = (int(time.time()) - int(delivery_time)) / 1440
            return delivery_age <= 24
        return False