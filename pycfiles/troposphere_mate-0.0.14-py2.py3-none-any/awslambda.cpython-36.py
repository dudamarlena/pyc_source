# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/awslambda.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 16438 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.awslambda
from troposphere.awslambda import AliasRoutingConfiguration as _AliasRoutingConfiguration, Code as _Code, Content as _Content, DeadLetterConfig as _DeadLetterConfig, DestinationConfig as _DestinationConfig, Environment as _Environment, OnFailure as _OnFailure, ProvisionedConcurrencyConfiguration as _ProvisionedConcurrencyConfiguration, Tags as _Tags, TracingConfig as _TracingConfig, VPCConfig as _VPCConfig, VersionWeight as _VersionWeight
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Code(troposphere.awslambda.Code, Mixin):

    def __init__(self, title=None, S3Bucket=NOTHING, S3Key=NOTHING, S3ObjectVersion=NOTHING, ZipFile=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         S3Bucket=S3Bucket, 
         S3Key=S3Key, 
         S3ObjectVersion=S3ObjectVersion, 
         ZipFile=ZipFile, **kwargs)
        (super(Code, self).__init__)(**processed_kwargs)


class VPCConfig(troposphere.awslambda.VPCConfig, Mixin):

    def __init__(self, title=None, SecurityGroupIds=REQUIRED, SubnetIds=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SecurityGroupIds=SecurityGroupIds, 
         SubnetIds=SubnetIds, **kwargs)
        (super(VPCConfig, self).__init__)(**processed_kwargs)


class OnFailure(troposphere.awslambda.OnFailure, Mixin):

    def __init__(self, title=None, Destination=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Destination=Destination, **kwargs)
        (super(OnFailure, self).__init__)(**processed_kwargs)


class DestinationConfig(troposphere.awslambda.DestinationConfig, Mixin):

    def __init__(self, title=None, OnFailure=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         OnFailure=OnFailure, **kwargs)
        (super(DestinationConfig, self).__init__)(**processed_kwargs)


class EventInvokeConfig(troposphere.awslambda.EventInvokeConfig, Mixin):

    def __init__(self, title, template=None, validation=True, FunctionName=REQUIRED, Qualifier=REQUIRED, DestinationConfig=NOTHING, MaximumEventAgeInSeconds=NOTHING, MaximumRetryAttempts=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         FunctionName=FunctionName, 
         Qualifier=Qualifier, 
         DestinationConfig=DestinationConfig, 
         MaximumEventAgeInSeconds=MaximumEventAgeInSeconds, 
         MaximumRetryAttempts=MaximumRetryAttempts, **kwargs)
        (super(EventInvokeConfig, self).__init__)(**processed_kwargs)


class EventSourceMapping(troposphere.awslambda.EventSourceMapping, Mixin):

    def __init__(self, title, template=None, validation=True, EventSourceArn=REQUIRED, FunctionName=REQUIRED, BatchSize=NOTHING, BisectBatchOnFunctionError=NOTHING, DestinationConfig=NOTHING, Enabled=NOTHING, MaximumBatchingWindowInSeconds=NOTHING, MaximumRecordAgeInSeconds=NOTHING, MaximumRetryAttempts=NOTHING, ParallelizationFactor=NOTHING, StartingPosition=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         EventSourceArn=EventSourceArn, 
         FunctionName=FunctionName, 
         BatchSize=BatchSize, 
         BisectBatchOnFunctionError=BisectBatchOnFunctionError, 
         DestinationConfig=DestinationConfig, 
         Enabled=Enabled, 
         MaximumBatchingWindowInSeconds=MaximumBatchingWindowInSeconds, 
         MaximumRecordAgeInSeconds=MaximumRecordAgeInSeconds, 
         MaximumRetryAttempts=MaximumRetryAttempts, 
         ParallelizationFactor=ParallelizationFactor, 
         StartingPosition=StartingPosition, **kwargs)
        (super(EventSourceMapping, self).__init__)(**processed_kwargs)


class DeadLetterConfig(troposphere.awslambda.DeadLetterConfig, Mixin):

    def __init__(self, title=None, TargetArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TargetArn=TargetArn, **kwargs)
        (super(DeadLetterConfig, self).__init__)(**processed_kwargs)


class Environment(troposphere.awslambda.Environment, Mixin):

    def __init__(self, title=None, Variables=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Variables=Variables, **kwargs)
        (super(Environment, self).__init__)(**processed_kwargs)


class TracingConfig(troposphere.awslambda.TracingConfig, Mixin):

    def __init__(self, title=None, Mode=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Mode=Mode, **kwargs)
        (super(TracingConfig, self).__init__)(**processed_kwargs)


class Function(troposphere.awslambda.Function, Mixin):

    def __init__(self, title, template=None, validation=True, Code=REQUIRED, Handler=REQUIRED, Role=REQUIRED, Runtime=REQUIRED, Description=NOTHING, DeadLetterConfig=NOTHING, Environment=NOTHING, FunctionName=NOTHING, KmsKeyArn=NOTHING, MemorySize=NOTHING, Layers=NOTHING, ReservedConcurrentExecutions=NOTHING, Tags=NOTHING, Timeout=NOTHING, TracingConfig=NOTHING, VpcConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Code=Code, 
         Handler=Handler, 
         Role=Role, 
         Runtime=Runtime, 
         Description=Description, 
         DeadLetterConfig=DeadLetterConfig, 
         Environment=Environment, 
         FunctionName=FunctionName, 
         KmsKeyArn=KmsKeyArn, 
         MemorySize=MemorySize, 
         Layers=Layers, 
         ReservedConcurrentExecutions=ReservedConcurrentExecutions, 
         Tags=Tags, 
         Timeout=Timeout, 
         TracingConfig=TracingConfig, 
         VpcConfig=VpcConfig, **kwargs)
        (super(Function, self).__init__)(**processed_kwargs)


class Permission(troposphere.awslambda.Permission, Mixin):

    def __init__(self, title, template=None, validation=True, Action=REQUIRED, FunctionName=REQUIRED, Principal=REQUIRED, EventSourceToken=NOTHING, SourceAccount=NOTHING, SourceArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Action=Action, 
         FunctionName=FunctionName, 
         Principal=Principal, 
         EventSourceToken=EventSourceToken, 
         SourceAccount=SourceAccount, 
         SourceArn=SourceArn, **kwargs)
        (super(Permission, self).__init__)(**processed_kwargs)


class VersionWeight(troposphere.awslambda.VersionWeight, Mixin):

    def __init__(self, title=None, FunctionVersion=REQUIRED, FunctionWeight=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FunctionVersion=FunctionVersion, 
         FunctionWeight=FunctionWeight, **kwargs)
        (super(VersionWeight, self).__init__)(**processed_kwargs)


class AliasRoutingConfiguration(troposphere.awslambda.AliasRoutingConfiguration, Mixin):

    def __init__(self, title=None, AdditionalVersionWeights=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AdditionalVersionWeights=AdditionalVersionWeights, **kwargs)
        (super(AliasRoutingConfiguration, self).__init__)(**processed_kwargs)


class ProvisionedConcurrencyConfiguration(troposphere.awslambda.ProvisionedConcurrencyConfiguration, Mixin):

    def __init__(self, title=None, ProvisionedConcurrentExecutions=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ProvisionedConcurrentExecutions=ProvisionedConcurrentExecutions, **kwargs)
        (super(ProvisionedConcurrencyConfiguration, self).__init__)(**processed_kwargs)


class Alias(troposphere.awslambda.Alias, Mixin):

    def __init__(self, title, template=None, validation=True, FunctionName=REQUIRED, FunctionVersion=REQUIRED, Name=REQUIRED, Description=NOTHING, ProvisionedConcurrencyConfig=NOTHING, RoutingConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         FunctionName=FunctionName, 
         FunctionVersion=FunctionVersion, 
         Name=Name, 
         Description=Description, 
         ProvisionedConcurrencyConfig=ProvisionedConcurrencyConfig, 
         RoutingConfig=RoutingConfig, **kwargs)
        (super(Alias, self).__init__)(**processed_kwargs)


class Version(troposphere.awslambda.Version, Mixin):

    def __init__(self, title, template=None, validation=True, FunctionName=REQUIRED, CodeSha256=NOTHING, Description=NOTHING, ProvisionedConcurrencyConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         FunctionName=FunctionName, 
         CodeSha256=CodeSha256, 
         Description=Description, 
         ProvisionedConcurrencyConfig=ProvisionedConcurrencyConfig, **kwargs)
        (super(Version, self).__init__)(**processed_kwargs)


class Content(troposphere.awslambda.Content, Mixin):

    def __init__(self, title=None, S3Bucket=REQUIRED, S3Key=REQUIRED, S3ObjectVersion=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         S3Bucket=S3Bucket, 
         S3Key=S3Key, 
         S3ObjectVersion=S3ObjectVersion, **kwargs)
        (super(Content, self).__init__)(**processed_kwargs)


class LayerVersion(troposphere.awslambda.LayerVersion, Mixin):

    def __init__(self, title, template=None, validation=True, Content=REQUIRED, CompatibleRuntimes=NOTHING, Description=NOTHING, LayerName=NOTHING, LicenseInfo=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Content=Content, 
         CompatibleRuntimes=CompatibleRuntimes, 
         Description=Description, 
         LayerName=LayerName, 
         LicenseInfo=LicenseInfo, **kwargs)
        (super(LayerVersion, self).__init__)(**processed_kwargs)


class LayerVersionPermission(troposphere.awslambda.LayerVersionPermission, Mixin):

    def __init__(self, title, template=None, validation=True, Action=REQUIRED, LayerVersionArn=REQUIRED, Principal=REQUIRED, OrganizationId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Action=Action, 
         LayerVersionArn=LayerVersionArn, 
         Principal=Principal, 
         OrganizationId=OrganizationId, **kwargs)
        (super(LayerVersionPermission, self).__init__)(**processed_kwargs)