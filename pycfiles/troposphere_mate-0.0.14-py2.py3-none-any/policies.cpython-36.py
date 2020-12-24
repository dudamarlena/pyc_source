# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/policies.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 4255 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.policies
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class AutoScalingRollingUpdate(troposphere.policies.AutoScalingRollingUpdate, Mixin):

    def __init__(self, title=None, MaxBatchSize=NOTHING, MinInstancesInService=NOTHING, MinSuccessfulInstancesPercent=NOTHING, PauseTime=NOTHING, SuspendProcesses=NOTHING, WaitOnResourceSignals=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MaxBatchSize=MaxBatchSize, 
         MinInstancesInService=MinInstancesInService, 
         MinSuccessfulInstancesPercent=MinSuccessfulInstancesPercent, 
         PauseTime=PauseTime, 
         SuspendProcesses=SuspendProcesses, 
         WaitOnResourceSignals=WaitOnResourceSignals, **kwargs)
        (super(AutoScalingRollingUpdate, self).__init__)(**processed_kwargs)


class AutoScalingScheduledAction(troposphere.policies.AutoScalingScheduledAction, Mixin):

    def __init__(self, title=None, IgnoreUnmodifiedGroupSizeProperties=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         IgnoreUnmodifiedGroupSizeProperties=IgnoreUnmodifiedGroupSizeProperties, **kwargs)
        (super(AutoScalingScheduledAction, self).__init__)(**processed_kwargs)


class AutoScalingReplacingUpdate(troposphere.policies.AutoScalingReplacingUpdate, Mixin):

    def __init__(self, title=None, WillReplace=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         WillReplace=WillReplace, **kwargs)
        (super(AutoScalingReplacingUpdate, self).__init__)(**processed_kwargs)


class CodeDeployLambdaAliasUpdate(troposphere.policies.CodeDeployLambdaAliasUpdate, Mixin):

    def __init__(self, title=None, ApplicationName=REQUIRED, DeploymentGroupName=REQUIRED, AfterAllowTrafficHook=NOTHING, BeforeAllowTrafficHook=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ApplicationName=ApplicationName, 
         DeploymentGroupName=DeploymentGroupName, 
         AfterAllowTrafficHook=AfterAllowTrafficHook, 
         BeforeAllowTrafficHook=BeforeAllowTrafficHook, **kwargs)
        (super(CodeDeployLambdaAliasUpdate, self).__init__)(**processed_kwargs)


class ResourceSignal(troposphere.policies.ResourceSignal, Mixin):

    def __init__(self, title=None, Count=NOTHING, Timeout=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Count=Count, 
         Timeout=Timeout, **kwargs)
        (super(ResourceSignal, self).__init__)(**processed_kwargs)


class AutoScalingCreationPolicy(troposphere.policies.AutoScalingCreationPolicy, Mixin):

    def __init__(self, title=None, MinSuccessfulInstancesPercent=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MinSuccessfulInstancesPercent=MinSuccessfulInstancesPercent, **kwargs)
        (super(AutoScalingCreationPolicy, self).__init__)(**processed_kwargs)