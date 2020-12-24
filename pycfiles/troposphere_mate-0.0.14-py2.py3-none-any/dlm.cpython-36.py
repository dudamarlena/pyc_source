# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/dlm.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 4466 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.dlm
from troposphere.dlm import CreateRule as _CreateRule, Parameters as _Parameters, PolicyDetails as _PolicyDetails, RetainRule as _RetainRule, Schedule as _Schedule, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Parameters(troposphere.dlm.Parameters, Mixin):

    def __init__(self, title=None, ExcludeBootVolume=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ExcludeBootVolume=ExcludeBootVolume, **kwargs)
        (super(Parameters, self).__init__)(**processed_kwargs)


class CreateRule(troposphere.dlm.CreateRule, Mixin):

    def __init__(self, title=None, Interval=REQUIRED, IntervalUnit=REQUIRED, Times=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Interval=Interval, 
         IntervalUnit=IntervalUnit, 
         Times=Times, **kwargs)
        (super(CreateRule, self).__init__)(**processed_kwargs)


class RetainRule(troposphere.dlm.RetainRule, Mixin):

    def __init__(self, title=None, Count=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Count=Count, **kwargs)
        (super(RetainRule, self).__init__)(**processed_kwargs)


class Schedule(troposphere.dlm.Schedule, Mixin):

    def __init__(self, title=None, CopyTags=NOTHING, CreateRule=NOTHING, Name=NOTHING, RetainRule=NOTHING, TagsToAdd=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CopyTags=CopyTags, 
         CreateRule=CreateRule, 
         Name=Name, 
         RetainRule=RetainRule, 
         TagsToAdd=TagsToAdd, **kwargs)
        (super(Schedule, self).__init__)(**processed_kwargs)


class PolicyDetails(troposphere.dlm.PolicyDetails, Mixin):

    def __init__(self, title=None, Parameters=NOTHING, PolicyType=NOTHING, ResourceTypes=NOTHING, Schedules=NOTHING, TargetTags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Parameters=Parameters, 
         PolicyType=PolicyType, 
         ResourceTypes=ResourceTypes, 
         Schedules=Schedules, 
         TargetTags=TargetTags, **kwargs)
        (super(PolicyDetails, self).__init__)(**processed_kwargs)


class LifecyclePolicy(troposphere.dlm.LifecyclePolicy, Mixin):

    def __init__(self, title, template=None, validation=True, Description=NOTHING, ExecutionRoleArn=NOTHING, PolicyDetails=NOTHING, State=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         ExecutionRoleArn=ExecutionRoleArn, 
         PolicyDetails=PolicyDetails, 
         State=State, **kwargs)
        (super(LifecyclePolicy, self).__init__)(**processed_kwargs)