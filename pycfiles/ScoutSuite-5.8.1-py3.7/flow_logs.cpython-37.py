# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/vpc/flow_logs.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 705 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.utils import get_name

class FlowLogs(AWSResources):

    def __init__(self, facade, region):
        self.region = region
        super(FlowLogs, self).__init__(facade)

    async def fetch_all(self):
        raw_logs = await self.facade.ec2.get_flow_logs(self.region)
        for raw_log in raw_logs:
            id, log = self._parse_log(raw_log)
            self[id] = log

    def _parse_log(self, raw_log):
        get_name(raw_log, raw_log, 'FlowLogId')
        log_id = raw_log.pop('FlowLogId')
        return (log_id, raw_log)