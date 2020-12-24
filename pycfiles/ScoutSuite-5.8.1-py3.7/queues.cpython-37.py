# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/sqs/queues.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1253 bytes
import json
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class Queues(AWSResources):

    def __init__(self, facade, region):
        super(Queues, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        queues = await self.facade.sqs.get_queues(self.region, [
         'CreatedTimestamp', 'Policy', 'QueueArn', 'KmsMasterKeyId'])
        for queue_url, queue_attributes in queues:
            id, queue = self._parse_queue(queue_url, queue_attributes)
            self[id] = queue

    def _parse_queue(self, queue_url, queue_attributes):
        queue = {}
        queue['QueueUrl'] = queue_url
        queue['arn'] = queue_attributes.pop('QueueArn')
        queue['name'] = queue['arn'].split(':')[(-1)]
        queue['kms_master_key_id'] = queue_attributes.pop('KmsMasterKeyId', None)
        queue['CreatedTimestamp'] = queue_attributes.pop('CreatedTimestamp', None)
        if 'Policy' in queue_attributes:
            queue['Policy'] = json.loads(queue_attributes['Policy'])
        else:
            queue['Policy'] = {'Statement': []}
        return (queue['name'], queue)