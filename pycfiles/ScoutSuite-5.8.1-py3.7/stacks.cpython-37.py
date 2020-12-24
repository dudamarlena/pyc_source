# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/cloudformation/stacks.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 2390 bytes
import re
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class Stacks(AWSResources):

    def __init__(self, facade, region):
        super(Stacks, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_stacks = await self.facade.cloudformation.get_stacks(self.region)
        for raw_stack in raw_stacks:
            name, stack = self._parse_stack(raw_stack)
            self[name] = stack

    def _parse_stack(self, raw_stack):
        raw_stack['id'] = raw_stack.pop('StackId')
        raw_stack['name'] = raw_stack.pop('StackName')
        raw_stack['drifted'] = raw_stack.pop('DriftInformation')['StackDriftStatus'] == 'DRIFTED'
        raw_stack['termination_protection'] = raw_stack['EnableTerminationProtection']
        template = raw_stack.pop('template')
        raw_stack['deletion_policy'] = self.has_deletion_policy(template)
        if hasattr(template, 'keys'):
            for group in template.keys():
                if 'DeletionPolicy' in template[group]:
                    raw_stack['deletion_policy'] = template[group]
                    break

        return (
         raw_stack['name'], raw_stack)

    @staticmethod
    def has_deletion_policy(template):
        """
        Return region to be used for global calls such as list bucket and get bucket location
        :param template: The api response containing the stack's template
        :return:
        """
        has_dp = True
        if isinstance(template, dict):
            template = template['Resources']
            for group in template.keys():
                if 'DeletionPolicy' in template[group]:
                    if template[group]['DeletionPolicy'] == 'Delete':
                        has_dp = False
                else:
                    has_dp = False

        elif isinstance(template, str):
            if re.match('\\"DeletionPolicy\\"\\s*:\\s*\\"Delete\\"', template):
                has_dp = False
            else:
                if not re.match('\\"DeletionPolicy\\"', template):
                    has_dp = False
        return has_dp