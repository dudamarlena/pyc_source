# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/config/recorders.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1270 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class Recorders(AWSResources):

    def __init__(self, facade, region):
        super(Recorders, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_recorders = await self.facade.config.get_recorders(self.region)
        for raw_recorder in raw_recorders:
            name, resource = self._parse_recorder(raw_recorder)
            self[name] = resource

    def _parse_recorder(self, raw_recorder):
        recorder = {}
        recorder['name'] = raw_recorder['name']
        recorder['region'] = self.region
        recorder['role_ARN'] = raw_recorder['roleARN']
        recorder['recording_group'] = raw_recorder['recordingGroup']
        recorder['enabled'] = raw_recorder['ConfigurationRecordersStatus']['recording']
        recorder['last_status'] = raw_recorder['ConfigurationRecordersStatus'].get('lastStatus')
        recorder['last_start_time'] = raw_recorder['ConfigurationRecordersStatus'].get('lastStartTime')
        recorder['last_status_change_time'] = raw_recorder['ConfigurationRecordersStatus'].get('lastStatusChangeTime')
        return (recorder['name'], recorder)