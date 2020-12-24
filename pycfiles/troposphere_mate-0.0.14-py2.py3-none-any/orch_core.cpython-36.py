# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/core/orch_core.py
# Compiled at: 2019-08-08 16:17:45
# Size of source mod 2**32: 3514 bytes
try:
    from typing import List, Tuple
except:
    pass

from collections import OrderedDict
DEPLOY_NOW_SIGNAL_TIER_NAME = 'deploy'
DEPLOY_NOW_SIGNAL_TIER_ENV = 'now'

def extract_all_env_tag(plan):
    """
    :type plan: List[List[str, str]]
    :param plan: [(can_id1, env_tag1), (can_id2, env_tag2), ...]

    :rtype: List[str]
    """
    env_tag_dict = OrderedDict()
    for tier_name, tier_env in plan:
        if tier_name.lower() == DEPLOY_NOW_SIGNAL_TIER_NAME:
            if tier_env.lower() == DEPLOY_NOW_SIGNAL_TIER_ENV:
                continue
        env_tag_dict[tier_env] = None

    return list(env_tag_dict)


def resolve_pipeline(plan):
    """
    Convert the item-to-deploy pipeline syntax to several execution plan.

    :type plan: List[List[str, str]]
    :param plan: [(can_id1, env_tag1), (can_id2, env_tag2), ...]

    :rtype: List[Tuple[List[str], str]]]
    """
    pipeline_change_set = list()
    job = ([], None)
    previous_env = None
    for tier_name, tier_env in plan:
        if tier_name.lower() == DEPLOY_NOW_SIGNAL_TIER_NAME and tier_env.lower() == DEPLOY_NOW_SIGNAL_TIER_ENV:
            if job != pipeline_change_set[(-1)]:
                pipeline_change_set.append(job)
                job = (list(job[0]),
                 job[1])
                continue
            if tier_env != previous_env:
                if len(pipeline_change_set):
                    if job != pipeline_change_set[(-1)]:
                        pipeline_change_set.append(job)
                else:
                    pipeline_change_set.append(job)
                previous_env = tier_env
                job = ([tier_name], tier_env)
            else:
                job[0].append(tier_name)

    if job != pipeline_change_set[(-1)]:
        pipeline_change_set.append(job)
    pipeline_change_set = pipeline_change_set[1:]
    dct = dict()
    pipeline = list()
    for tier_list, tier_env in pipeline_change_set:
        if tier_env in dct:
            for tier_name in tier_list:
                if tier_name not in dct[tier_env]:
                    dct[tier_env].append(tier_name)

        else:
            dct[tier_env] = tier_list
        pipeline.append((list(dct[tier_env]), tier_env))

    return pipeline


class ResourceFilter(object):
    __doc__ = '\n    Construct a Resource Filter Class to decide if a specific AWS Resource\n    should be ignored or not.\n\n    1. Explicit Deny\n    2. Explicit Allow\n    3. Default Deny\n    '

    def __init__(self, ignored_stack_id_list, allowed_stack_id_list):
        self.ignored_stack_id_list = ignored_stack_id_list
        self.allowed_stack_id_list = allowed_stack_id_list

    def filter(self, resource, template):
        """
        Check if we want to keep this resource in the cloudformation.
        If ``True``, we keep it. if ``False`` we call
        ``Template.remove_resource(resource)`` to remove it,

        :type resource: AWSObject
        :type template: Template
        :rtype: bool
        """
        if resource.resource_type == 'AWS::CloudFormation::Stack':
            if resource.title in self.allowed_stack_id_list:
                return True
            else:
                return False
        else:
            return True