# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/events.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 12000 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.events
from troposphere.events import AwsVpcConfiguration as _AwsVpcConfiguration, BatchArrayProperties as _BatchArrayProperties, BatchParameters as _BatchParameters, BatchRetryStrategy as _BatchRetryStrategy, Condition as _Condition, EcsParameters as _EcsParameters, InputTransformer as _InputTransformer, KinesisParameters as _KinesisParameters, NetworkConfiguration as _NetworkConfiguration, RunCommandParameters as _RunCommandParameters, RunCommandTarget as _RunCommandTarget, SqsParameters as _SqsParameters, Target as _Target
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class EventBus(troposphere.events.EventBus, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, EventSourceName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         EventSourceName=EventSourceName, **kwargs)
        (super(EventBus, self).__init__)(**processed_kwargs)


class Condition(troposphere.events.Condition, Mixin):

    def __init__(self, title=None, Key=NOTHING, Type=NOTHING, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Type=Type, 
         Value=Value, **kwargs)
        (super(Condition, self).__init__)(**processed_kwargs)


class EventBusPolicy(troposphere.events.EventBusPolicy, Mixin):

    def __init__(self, title, template=None, validation=True, Action=REQUIRED, Principal=REQUIRED, StatementId=REQUIRED, Condition=NOTHING, EventBusName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Action=Action, 
         Principal=Principal, 
         StatementId=StatementId, 
         Condition=Condition, 
         EventBusName=EventBusName, **kwargs)
        (super(EventBusPolicy, self).__init__)(**processed_kwargs)


class BatchArrayProperties(troposphere.events.BatchArrayProperties, Mixin):

    def __init__(self, title=None, Size=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Size=Size, **kwargs)
        (super(BatchArrayProperties, self).__init__)(**processed_kwargs)


class BatchRetryStrategy(troposphere.events.BatchRetryStrategy, Mixin):

    def __init__(self, title=None, Attempts=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Attempts=Attempts, **kwargs)
        (super(BatchRetryStrategy, self).__init__)(**processed_kwargs)


class BatchParameters(troposphere.events.BatchParameters, Mixin):

    def __init__(self, title=None, JobDefinition=REQUIRED, JobName=REQUIRED, ArrayProperties=NOTHING, RetryStrategy=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         JobDefinition=JobDefinition, 
         JobName=JobName, 
         ArrayProperties=ArrayProperties, 
         RetryStrategy=RetryStrategy, **kwargs)
        (super(BatchParameters, self).__init__)(**processed_kwargs)


class AwsVpcConfiguration(troposphere.events.AwsVpcConfiguration, Mixin):

    def __init__(self, title=None, Subnets=REQUIRED, AssignPublicIp=NOTHING, SecurityGroups=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Subnets=Subnets, 
         AssignPublicIp=AssignPublicIp, 
         SecurityGroups=SecurityGroups, **kwargs)
        (super(AwsVpcConfiguration, self).__init__)(**processed_kwargs)


class NetworkConfiguration(troposphere.events.NetworkConfiguration, Mixin):

    def __init__(self, title=None, AwsVpcConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AwsVpcConfiguration=AwsVpcConfiguration, **kwargs)
        (super(NetworkConfiguration, self).__init__)(**processed_kwargs)


class EcsParameters(troposphere.events.EcsParameters, Mixin):

    def __init__(self, title=None, TaskDefinitionArn=REQUIRED, Group=NOTHING, LaunchType=NOTHING, NetworkConfiguration=NOTHING, PlatformVersion=NOTHING, TaskCount=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TaskDefinitionArn=TaskDefinitionArn, 
         Group=Group, 
         LaunchType=LaunchType, 
         NetworkConfiguration=NetworkConfiguration, 
         PlatformVersion=PlatformVersion, 
         TaskCount=TaskCount, **kwargs)
        (super(EcsParameters, self).__init__)(**processed_kwargs)


class InputTransformer(troposphere.events.InputTransformer, Mixin):

    def __init__(self, title=None, InputTemplate=REQUIRED, InputPathsMap=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         InputTemplate=InputTemplate, 
         InputPathsMap=InputPathsMap, **kwargs)
        (super(InputTransformer, self).__init__)(**processed_kwargs)


class KinesisParameters(troposphere.events.KinesisParameters, Mixin):

    def __init__(self, title=None, PartitionKeyPath=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PartitionKeyPath=PartitionKeyPath, **kwargs)
        (super(KinesisParameters, self).__init__)(**processed_kwargs)


class RunCommandTarget(troposphere.events.RunCommandTarget, Mixin):

    def __init__(self, title=None, Key=REQUIRED, Values=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Values=Values, **kwargs)
        (super(RunCommandTarget, self).__init__)(**processed_kwargs)


class RunCommandParameters(troposphere.events.RunCommandParameters, Mixin):

    def __init__(self, title=None, RunCommandTargets=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RunCommandTargets=RunCommandTargets, **kwargs)
        (super(RunCommandParameters, self).__init__)(**processed_kwargs)


class SqsParameters(troposphere.events.SqsParameters, Mixin):

    def __init__(self, title=None, MessageGroupId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MessageGroupId=MessageGroupId, **kwargs)
        (super(SqsParameters, self).__init__)(**processed_kwargs)


class Target(troposphere.events.Target, Mixin):

    def __init__(self, title=None, Arn=REQUIRED, Id=REQUIRED, BatchParameters=NOTHING, EcsParameters=NOTHING, Input=NOTHING, InputPath=NOTHING, InputTransformer=NOTHING, KinesisParameters=NOTHING, RoleArn=NOTHING, RunCommandParameters=NOTHING, SqsParameters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Arn=Arn, 
         Id=Id, 
         BatchParameters=BatchParameters, 
         EcsParameters=EcsParameters, 
         Input=Input, 
         InputPath=InputPath, 
         InputTransformer=InputTransformer, 
         KinesisParameters=KinesisParameters, 
         RoleArn=RoleArn, 
         RunCommandParameters=RunCommandParameters, 
         SqsParameters=SqsParameters, **kwargs)
        (super(Target, self).__init__)(**processed_kwargs)


class Rule(troposphere.events.Rule, Mixin):

    def __init__(self, title, template=None, validation=True, Description=NOTHING, EventBusName=NOTHING, EventPattern=NOTHING, Name=NOTHING, RoleArn=NOTHING, ScheduleExpression=NOTHING, State=NOTHING, Targets=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         EventBusName=EventBusName, 
         EventPattern=EventPattern, 
         Name=Name, 
         RoleArn=RoleArn, 
         ScheduleExpression=ScheduleExpression, 
         State=State, 
         Targets=Targets, **kwargs)
        (super(Rule, self).__init__)(**processed_kwargs)