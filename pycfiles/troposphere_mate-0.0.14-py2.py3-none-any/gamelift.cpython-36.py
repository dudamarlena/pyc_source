# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/gamelift.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 9801 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.gamelift
from troposphere.gamelift import CertificateConfiguration as _CertificateConfiguration, IpPermission as _IpPermission, ResourceCreationLimitPolicy as _ResourceCreationLimitPolicy, RoutingStrategy as _RoutingStrategy, RuntimeConfiguration as _RuntimeConfiguration, S3Location as _S3Location, ServerProcess as _ServerProcess
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class RoutingStrategy(troposphere.gamelift.RoutingStrategy, Mixin):

    def __init__(self, title=None, Type=REQUIRED, FleetId=NOTHING, Message=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         FleetId=FleetId, 
         Message=Message, **kwargs)
        (super(RoutingStrategy, self).__init__)(**processed_kwargs)


class Alias(troposphere.gamelift.Alias, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, RoutingStrategy=REQUIRED, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         RoutingStrategy=RoutingStrategy, 
         Description=Description, **kwargs)
        (super(Alias, self).__init__)(**processed_kwargs)


class S3Location(troposphere.gamelift.S3Location, Mixin):

    def __init__(self, title=None, Bucket=REQUIRED, Key=REQUIRED, RoleArn=REQUIRED, ObjectVersion=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Bucket=Bucket, 
         Key=Key, 
         RoleArn=RoleArn, 
         ObjectVersion=ObjectVersion, **kwargs)
        (super(S3Location, self).__init__)(**processed_kwargs)


class Build(troposphere.gamelift.Build, Mixin):

    def __init__(self, title, template=None, validation=True, Name=NOTHING, OperatingSystem=NOTHING, StorageLocation=NOTHING, Version=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         OperatingSystem=OperatingSystem, 
         StorageLocation=StorageLocation, 
         Version=Version, **kwargs)
        (super(Build, self).__init__)(**processed_kwargs)


class CertificateConfiguration(troposphere.gamelift.CertificateConfiguration, Mixin):

    def __init__(self, title=None, CertificateType=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CertificateType=CertificateType, **kwargs)
        (super(CertificateConfiguration, self).__init__)(**processed_kwargs)


class IpPermission(troposphere.gamelift.IpPermission, Mixin):

    def __init__(self, title=None, FromPort=REQUIRED, IpRange=REQUIRED, Protocol=REQUIRED, ToPort=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FromPort=FromPort, 
         IpRange=IpRange, 
         Protocol=Protocol, 
         ToPort=ToPort, **kwargs)
        (super(IpPermission, self).__init__)(**processed_kwargs)


class ResourceCreationLimitPolicy(troposphere.gamelift.ResourceCreationLimitPolicy, Mixin):

    def __init__(self, title=None, NewGameSessionsPerCreator=NOTHING, PolicyPeriodInMinutes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         NewGameSessionsPerCreator=NewGameSessionsPerCreator, 
         PolicyPeriodInMinutes=PolicyPeriodInMinutes, **kwargs)
        (super(ResourceCreationLimitPolicy, self).__init__)(**processed_kwargs)


class ServerProcess(troposphere.gamelift.ServerProcess, Mixin):

    def __init__(self, title=None, ConcurrentExecutions=REQUIRED, LaunchPath=REQUIRED, Parameters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ConcurrentExecutions=ConcurrentExecutions, 
         LaunchPath=LaunchPath, 
         Parameters=Parameters, **kwargs)
        (super(ServerProcess, self).__init__)(**processed_kwargs)


class RuntimeConfiguration(troposphere.gamelift.RuntimeConfiguration, Mixin):

    def __init__(self, title=None, GameSessionActivationTimeoutSeconds=NOTHING, MaxConcurrentGameSessionActivations=NOTHING, ServerProcesses=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         GameSessionActivationTimeoutSeconds=GameSessionActivationTimeoutSeconds, 
         MaxConcurrentGameSessionActivations=MaxConcurrentGameSessionActivations, 
         ServerProcesses=ServerProcesses, **kwargs)
        (super(RuntimeConfiguration, self).__init__)(**processed_kwargs)


class Fleet(troposphere.gamelift.Fleet, Mixin):

    def __init__(self, title, template=None, validation=True, EC2InstanceType=REQUIRED, Name=REQUIRED, BuildId=NOTHING, CertificateConfiguration=NOTHING, Description=NOTHING, DesiredEC2Instances=NOTHING, EC2InboundPermissions=NOTHING, FleetType=NOTHING, InstanceRoleARN=NOTHING, LogPaths=NOTHING, MaxSize=NOTHING, MetricGroups=NOTHING, MinSize=NOTHING, NewGameSessionProtectionPolicy=NOTHING, PeerVpcAwsAccountId=NOTHING, PeerVpcId=NOTHING, ResourceCreationLimitPolicy=NOTHING, RuntimeConfiguration=NOTHING, ScriptId=NOTHING, ServerLaunchParameters=NOTHING, ServerLaunchPath=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         EC2InstanceType=EC2InstanceType, 
         Name=Name, 
         BuildId=BuildId, 
         CertificateConfiguration=CertificateConfiguration, 
         Description=Description, 
         DesiredEC2Instances=DesiredEC2Instances, 
         EC2InboundPermissions=EC2InboundPermissions, 
         FleetType=FleetType, 
         InstanceRoleARN=InstanceRoleARN, 
         LogPaths=LogPaths, 
         MaxSize=MaxSize, 
         MetricGroups=MetricGroups, 
         MinSize=MinSize, 
         NewGameSessionProtectionPolicy=NewGameSessionProtectionPolicy, 
         PeerVpcAwsAccountId=PeerVpcAwsAccountId, 
         PeerVpcId=PeerVpcId, 
         ResourceCreationLimitPolicy=ResourceCreationLimitPolicy, 
         RuntimeConfiguration=RuntimeConfiguration, 
         ScriptId=ScriptId, 
         ServerLaunchParameters=ServerLaunchParameters, 
         ServerLaunchPath=ServerLaunchPath, **kwargs)
        (super(Fleet, self).__init__)(**processed_kwargs)