# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/greengrass.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 33766 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.greengrass
from troposphere.greengrass import Connector as _Connector, ConnectorDefinitionVersion as _ConnectorDefinitionVersion, Core as _Core, CoreDefinitionVersion as _CoreDefinitionVersion, DefaultConfig as _DefaultConfig, Device as _Device, DeviceDefinitionVersion as _DeviceDefinitionVersion, Environment as _Environment, Execution as _Execution, Function as _Function, FunctionConfiguration as _FunctionConfiguration, FunctionDefinitionVersion as _FunctionDefinitionVersion, GroupOwnerSetting as _GroupOwnerSetting, GroupVersion as _GroupVersion, LocalDeviceResourceData as _LocalDeviceResourceData, LocalVolumeResourceData as _LocalVolumeResourceData, Logger as _Logger, LoggerDefinitionVersion as _LoggerDefinitionVersion, ResourceAccessPolicy as _ResourceAccessPolicy, ResourceDataContainer as _ResourceDataContainer, ResourceDefinitionVersion as _ResourceDefinitionVersion, ResourceInstance as _ResourceInstance, RunAs as _RunAs, S3MachineLearningModelResourceData as _S3MachineLearningModelResourceData, SageMakerMachineLearningModelResourceData as _SageMakerMachineLearningModelResourceData, SecretsManagerSecretResourceData as _SecretsManagerSecretResourceData, Subscription as _Subscription, SubscriptionDefinitionVersionProperty as _SubscriptionDefinitionVersionProperty
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Connector(troposphere.greengrass.Connector, Mixin):

    def __init__(self, title=None, ConnectorArn=REQUIRED, Id=REQUIRED, Parameters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ConnectorArn=ConnectorArn, 
         Id=Id, 
         Parameters=Parameters, **kwargs)
        (super(Connector, self).__init__)(**processed_kwargs)


class ConnectorDefinitionVersion(troposphere.greengrass.ConnectorDefinitionVersion, Mixin):

    def __init__(self, title=None, ConnectorDefinitionId=REQUIRED, Connectors=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ConnectorDefinitionId=ConnectorDefinitionId, 
         Connectors=Connectors, **kwargs)
        (super(ConnectorDefinitionVersion, self).__init__)(**processed_kwargs)


class ConnectorDefinition(troposphere.greengrass.ConnectorDefinition, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, InitialVersion=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         InitialVersion=InitialVersion, 
         Tags=Tags, **kwargs)
        (super(ConnectorDefinition, self).__init__)(**processed_kwargs)


class ConnectorDefinitionVersion(troposphere.greengrass.ConnectorDefinitionVersion, Mixin):

    def __init__(self, title, template=None, validation=True, ConnectorDefinitionId=REQUIRED, Connectors=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ConnectorDefinitionId=ConnectorDefinitionId, 
         Connectors=Connectors, **kwargs)
        (super(ConnectorDefinitionVersion, self).__init__)(**processed_kwargs)


class Core(troposphere.greengrass.Core, Mixin):

    def __init__(self, title=None, CertificateArn=REQUIRED, Id=REQUIRED, ThingArn=REQUIRED, SyncShadow=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CertificateArn=CertificateArn, 
         Id=Id, 
         ThingArn=ThingArn, 
         SyncShadow=SyncShadow, **kwargs)
        (super(Core, self).__init__)(**processed_kwargs)


class CoreDefinitionVersion(troposphere.greengrass.CoreDefinitionVersion, Mixin):

    def __init__(self, title=None, CoreDefinitionId=REQUIRED, Cores=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CoreDefinitionId=CoreDefinitionId, 
         Cores=Cores, **kwargs)
        (super(CoreDefinitionVersion, self).__init__)(**processed_kwargs)


class CoreDefinition(troposphere.greengrass.CoreDefinition, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, InitialVersion=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         InitialVersion=InitialVersion, 
         Tags=Tags, **kwargs)
        (super(CoreDefinition, self).__init__)(**processed_kwargs)


class CoreDefinitionVersion(troposphere.greengrass.CoreDefinitionVersion, Mixin):

    def __init__(self, title, template=None, validation=True, CoreDefinitionId=REQUIRED, Cores=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CoreDefinitionId=CoreDefinitionId, 
         Cores=Cores, **kwargs)
        (super(CoreDefinitionVersion, self).__init__)(**processed_kwargs)


class Device(troposphere.greengrass.Device, Mixin):

    def __init__(self, title=None, CertificateArn=REQUIRED, Id=REQUIRED, ThingArn=REQUIRED, SyncShadow=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CertificateArn=CertificateArn, 
         Id=Id, 
         ThingArn=ThingArn, 
         SyncShadow=SyncShadow, **kwargs)
        (super(Device, self).__init__)(**processed_kwargs)


class DeviceDefinitionVersion(troposphere.greengrass.DeviceDefinitionVersion, Mixin):

    def __init__(self, title=None, DeviceDefinitionId=REQUIRED, Devices=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeviceDefinitionId=DeviceDefinitionId, 
         Devices=Devices, **kwargs)
        (super(DeviceDefinitionVersion, self).__init__)(**processed_kwargs)


class DeviceDefinition(troposphere.greengrass.DeviceDefinition, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, InitialVersion=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         InitialVersion=InitialVersion, 
         Tags=Tags, **kwargs)
        (super(DeviceDefinition, self).__init__)(**processed_kwargs)


class DeviceDefinitionVersion(troposphere.greengrass.DeviceDefinitionVersion, Mixin):

    def __init__(self, title, template=None, validation=True, DeviceDefinitionId=REQUIRED, Devices=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DeviceDefinitionId=DeviceDefinitionId, 
         Devices=Devices, **kwargs)
        (super(DeviceDefinitionVersion, self).__init__)(**processed_kwargs)


class RunAs(troposphere.greengrass.RunAs, Mixin):

    def __init__(self, title=None, Gid=NOTHING, Uid=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Gid=Gid, 
         Uid=Uid, **kwargs)
        (super(RunAs, self).__init__)(**processed_kwargs)


class Execution(troposphere.greengrass.Execution, Mixin):

    def __init__(self, title=None, IsolationMode=NOTHING, RunAs=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         IsolationMode=IsolationMode, 
         RunAs=RunAs, **kwargs)
        (super(Execution, self).__init__)(**processed_kwargs)


class DefaultConfig(troposphere.greengrass.DefaultConfig, Mixin):

    def __init__(self, title=None, Execution=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Execution=Execution, **kwargs)
        (super(DefaultConfig, self).__init__)(**processed_kwargs)


class ResourceAccessPolicy(troposphere.greengrass.ResourceAccessPolicy, Mixin):

    def __init__(self, title=None, ResourceId=REQUIRED, Permission=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ResourceId=ResourceId, 
         Permission=Permission, **kwargs)
        (super(ResourceAccessPolicy, self).__init__)(**processed_kwargs)


class Environment(troposphere.greengrass.Environment, Mixin):

    def __init__(self, title=None, AccessSysfs=NOTHING, Execution=NOTHING, ResourceAccessPolicies=NOTHING, Variables=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AccessSysfs=AccessSysfs, 
         Execution=Execution, 
         ResourceAccessPolicies=ResourceAccessPolicies, 
         Variables=Variables, **kwargs)
        (super(Environment, self).__init__)(**processed_kwargs)


class FunctionConfiguration(troposphere.greengrass.FunctionConfiguration, Mixin):

    def __init__(self, title=None, EncodingType=NOTHING, Environment=NOTHING, ExecArgs=NOTHING, Executable=NOTHING, MemorySize=NOTHING, Pinned=NOTHING, Timeout=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EncodingType=EncodingType, 
         Environment=Environment, 
         ExecArgs=ExecArgs, 
         Executable=Executable, 
         MemorySize=MemorySize, 
         Pinned=Pinned, 
         Timeout=Timeout, **kwargs)
        (super(FunctionConfiguration, self).__init__)(**processed_kwargs)


class Function(troposphere.greengrass.Function, Mixin):

    def __init__(self, title=None, FunctionArn=REQUIRED, FunctionConfiguration=REQUIRED, Id=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FunctionArn=FunctionArn, 
         FunctionConfiguration=FunctionConfiguration, 
         Id=Id, **kwargs)
        (super(Function, self).__init__)(**processed_kwargs)


class FunctionDefinitionVersion(troposphere.greengrass.FunctionDefinitionVersion, Mixin):

    def __init__(self, title=None, FunctionDefinitionId=REQUIRED, Functions=REQUIRED, DefaultConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FunctionDefinitionId=FunctionDefinitionId, 
         Functions=Functions, 
         DefaultConfig=DefaultConfig, **kwargs)
        (super(FunctionDefinitionVersion, self).__init__)(**processed_kwargs)


class FunctionDefinition(troposphere.greengrass.FunctionDefinition, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, InitialVersion=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         InitialVersion=InitialVersion, 
         Tags=Tags, **kwargs)
        (super(FunctionDefinition, self).__init__)(**processed_kwargs)


class FunctionDefinitionVersion(troposphere.greengrass.FunctionDefinitionVersion, Mixin):

    def __init__(self, title, template=None, validation=True, FunctionDefinitionId=REQUIRED, Functions=REQUIRED, DefaultConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         FunctionDefinitionId=FunctionDefinitionId, 
         Functions=Functions, 
         DefaultConfig=DefaultConfig, **kwargs)
        (super(FunctionDefinitionVersion, self).__init__)(**processed_kwargs)


class GroupVersion(troposphere.greengrass.GroupVersion, Mixin):

    def __init__(self, title=None, GroupId=REQUIRED, ConnectorDefinitionVersionArn=NOTHING, CoreDefinitionVersionArn=NOTHING, DeviceDefinitionVersionArn=NOTHING, FunctionDefinitionVersionArn=NOTHING, LoggerDefinitionVersionArn=NOTHING, ResourceDefinitionVersionArn=NOTHING, SubscriptionDefinitionVersionArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         GroupId=GroupId, 
         ConnectorDefinitionVersionArn=ConnectorDefinitionVersionArn, 
         CoreDefinitionVersionArn=CoreDefinitionVersionArn, 
         DeviceDefinitionVersionArn=DeviceDefinitionVersionArn, 
         FunctionDefinitionVersionArn=FunctionDefinitionVersionArn, 
         LoggerDefinitionVersionArn=LoggerDefinitionVersionArn, 
         ResourceDefinitionVersionArn=ResourceDefinitionVersionArn, 
         SubscriptionDefinitionVersionArn=SubscriptionDefinitionVersionArn, **kwargs)
        (super(GroupVersion, self).__init__)(**processed_kwargs)


class Group(troposphere.greengrass.Group, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, InitialVersion=NOTHING, RoleArn=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         InitialVersion=InitialVersion, 
         RoleArn=RoleArn, 
         Tags=Tags, **kwargs)
        (super(Group, self).__init__)(**processed_kwargs)


class GroupVersion(troposphere.greengrass.GroupVersion, Mixin):

    def __init__(self, title, template=None, validation=True, GroupId=REQUIRED, ConnectorDefinitionVersionArn=NOTHING, CoreDefinitionVersionArn=NOTHING, DeviceDefinitionVersionArn=NOTHING, FunctionDefinitionVersionArn=NOTHING, LoggerDefinitionVersionArn=NOTHING, ResourceDefinitionVersionArn=NOTHING, SubscriptionDefinitionVersionArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         GroupId=GroupId, 
         ConnectorDefinitionVersionArn=ConnectorDefinitionVersionArn, 
         CoreDefinitionVersionArn=CoreDefinitionVersionArn, 
         DeviceDefinitionVersionArn=DeviceDefinitionVersionArn, 
         FunctionDefinitionVersionArn=FunctionDefinitionVersionArn, 
         LoggerDefinitionVersionArn=LoggerDefinitionVersionArn, 
         ResourceDefinitionVersionArn=ResourceDefinitionVersionArn, 
         SubscriptionDefinitionVersionArn=SubscriptionDefinitionVersionArn, **kwargs)
        (super(GroupVersion, self).__init__)(**processed_kwargs)


class Logger(troposphere.greengrass.Logger, Mixin):

    def __init__(self, title=None, Component=REQUIRED, Id=REQUIRED, Level=REQUIRED, Type=REQUIRED, Space=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Component=Component, 
         Id=Id, 
         Level=Level, 
         Type=Type, 
         Space=Space, **kwargs)
        (super(Logger, self).__init__)(**processed_kwargs)


class LoggerDefinitionVersion(troposphere.greengrass.LoggerDefinitionVersion, Mixin):

    def __init__(self, title=None, LoggerDefinitionId=REQUIRED, Loggers=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LoggerDefinitionId=LoggerDefinitionId, 
         Loggers=Loggers, **kwargs)
        (super(LoggerDefinitionVersion, self).__init__)(**processed_kwargs)


class LoggerDefinition(troposphere.greengrass.LoggerDefinition, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, InitialVersion=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         InitialVersion=InitialVersion, 
         Tags=Tags, **kwargs)
        (super(LoggerDefinition, self).__init__)(**processed_kwargs)


class LoggerDefinitionVersion(troposphere.greengrass.LoggerDefinitionVersion, Mixin):

    def __init__(self, title, template=None, validation=True, LoggerDefinitionId=REQUIRED, Loggers=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         LoggerDefinitionId=LoggerDefinitionId, 
         Loggers=Loggers, **kwargs)
        (super(LoggerDefinitionVersion, self).__init__)(**processed_kwargs)


class GroupOwnerSetting(troposphere.greengrass.GroupOwnerSetting, Mixin):

    def __init__(self, title=None, AutoAddGroupOwner=REQUIRED, GroupOwner=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AutoAddGroupOwner=AutoAddGroupOwner, 
         GroupOwner=GroupOwner, **kwargs)
        (super(GroupOwnerSetting, self).__init__)(**processed_kwargs)


class LocalDeviceResourceData(troposphere.greengrass.LocalDeviceResourceData, Mixin):

    def __init__(self, title=None, SourcePath=REQUIRED, GroupOwnerSetting=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SourcePath=SourcePath, 
         GroupOwnerSetting=GroupOwnerSetting, **kwargs)
        (super(LocalDeviceResourceData, self).__init__)(**processed_kwargs)


class LocalVolumeResourceData(troposphere.greengrass.LocalVolumeResourceData, Mixin):

    def __init__(self, title=None, DestinationPath=REQUIRED, SourcePath=REQUIRED, GroupOwnerSetting=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DestinationPath=DestinationPath, 
         SourcePath=SourcePath, 
         GroupOwnerSetting=GroupOwnerSetting, **kwargs)
        (super(LocalVolumeResourceData, self).__init__)(**processed_kwargs)


class S3MachineLearningModelResourceData(troposphere.greengrass.S3MachineLearningModelResourceData, Mixin):

    def __init__(self, title=None, DestinationPath=REQUIRED, S3Uri=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DestinationPath=DestinationPath, 
         S3Uri=S3Uri, **kwargs)
        (super(S3MachineLearningModelResourceData, self).__init__)(**processed_kwargs)


class SageMakerMachineLearningModelResourceData(troposphere.greengrass.SageMakerMachineLearningModelResourceData, Mixin):

    def __init__(self, title=None, DestinationPath=REQUIRED, SageMakerJobArn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DestinationPath=DestinationPath, 
         SageMakerJobArn=SageMakerJobArn, **kwargs)
        (super(SageMakerMachineLearningModelResourceData, self).__init__)(**processed_kwargs)


class SecretsManagerSecretResourceData(troposphere.greengrass.SecretsManagerSecretResourceData, Mixin):

    def __init__(self, title=None, ARN=REQUIRED, AdditionalStagingLabelsToDownload=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ARN=ARN, 
         AdditionalStagingLabelsToDownload=AdditionalStagingLabelsToDownload, **kwargs)
        (super(SecretsManagerSecretResourceData, self).__init__)(**processed_kwargs)


class ResourceDataContainer(troposphere.greengrass.ResourceDataContainer, Mixin):

    def __init__(self, title=None, LocalDeviceResourceData=NOTHING, LocalVolumeResourceData=NOTHING, S3MachineLearningModelResourceData=NOTHING, SageMakerMachineLearningModelResourceData=NOTHING, SecretsManagerSecretResourceData=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LocalDeviceResourceData=LocalDeviceResourceData, 
         LocalVolumeResourceData=LocalVolumeResourceData, 
         S3MachineLearningModelResourceData=S3MachineLearningModelResourceData, 
         SageMakerMachineLearningModelResourceData=SageMakerMachineLearningModelResourceData, 
         SecretsManagerSecretResourceData=SecretsManagerSecretResourceData, **kwargs)
        (super(ResourceDataContainer, self).__init__)(**processed_kwargs)


class ResourceInstance(troposphere.greengrass.ResourceInstance, Mixin):

    def __init__(self, title=None, Id=REQUIRED, Name=REQUIRED, ResourceDataContainer=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Id=Id, 
         Name=Name, 
         ResourceDataContainer=ResourceDataContainer, **kwargs)
        (super(ResourceInstance, self).__init__)(**processed_kwargs)


class ResourceDefinitionVersion(troposphere.greengrass.ResourceDefinitionVersion, Mixin):

    def __init__(self, title=None, ResourceDefinitionId=REQUIRED, Resources=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ResourceDefinitionId=ResourceDefinitionId, 
         Resources=Resources, **kwargs)
        (super(ResourceDefinitionVersion, self).__init__)(**processed_kwargs)


class ResourceDefinition(troposphere.greengrass.ResourceDefinition, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, InitialVersion=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         InitialVersion=InitialVersion, 
         Tags=Tags, **kwargs)
        (super(ResourceDefinition, self).__init__)(**processed_kwargs)


class ResourceDefinitionVersion(troposphere.greengrass.ResourceDefinitionVersion, Mixin):

    def __init__(self, title, template=None, validation=True, ResourceDefinitionId=REQUIRED, Resources=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ResourceDefinitionId=ResourceDefinitionId, 
         Resources=Resources, **kwargs)
        (super(ResourceDefinitionVersion, self).__init__)(**processed_kwargs)


class Subscription(troposphere.greengrass.Subscription, Mixin):

    def __init__(self, title=None, Id=REQUIRED, Source=REQUIRED, Subject=REQUIRED, Target=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Id=Id, 
         Source=Source, 
         Subject=Subject, 
         Target=Target, **kwargs)
        (super(Subscription, self).__init__)(**processed_kwargs)


class SubscriptionDefinitionVersionProperty(troposphere.greengrass.SubscriptionDefinitionVersionProperty, Mixin):

    def __init__(self, title=None, Subscriptions=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Subscriptions=Subscriptions, **kwargs)
        (super(SubscriptionDefinitionVersionProperty, self).__init__)(**processed_kwargs)


class SubscriptionDefinition(troposphere.greengrass.SubscriptionDefinition, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, InitialVersion=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         InitialVersion=InitialVersion, 
         Tags=Tags, **kwargs)
        (super(SubscriptionDefinition, self).__init__)(**processed_kwargs)


class SubscriptionDefinitionVersion(troposphere.greengrass.SubscriptionDefinitionVersion, Mixin):

    def __init__(self, title, template=None, validation=True, SubscriptionDefinitionId=REQUIRED, Subscriptions=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         SubscriptionDefinitionId=SubscriptionDefinitionId, 
         Subscriptions=Subscriptions, **kwargs)
        (super(SubscriptionDefinitionVersion, self).__init__)(**processed_kwargs)