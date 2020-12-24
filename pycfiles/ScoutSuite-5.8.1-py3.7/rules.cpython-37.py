# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/config/rules.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1170 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class Rules(AWSResources):

    def __init__(self, facade, region):
        super(Rules, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_rules = await self.facade.config.get_rules(self.region)
        for raw_rule in raw_rules:
            name, resource = self._parse_rule(raw_rule)
            self[name] = resource

    def _parse_rule(self, raw_rule):
        rule = {}
        rule['id'] = raw_rule.pop('ConfigRuleId', None)
        rule['arn'] = raw_rule.pop('ConfigRuleArn', None)
        rule['name'] = raw_rule.pop('ConfigRuleName', None)
        rule['description'] = raw_rule.pop('Description', None)
        rule['scope'] = raw_rule.pop('Scope', None)
        rule['source'] = raw_rule.pop('Source', None)
        rule['input_parameters'] = raw_rule.pop('InputParameters', None)
        rule['maximum_execution_frequency'] = raw_rule.pop('MaximumExecutionFrequency', None)
        rule['state'] = raw_rule.pop('ConfigRuleState', None)
        return (rule['name'], rule)