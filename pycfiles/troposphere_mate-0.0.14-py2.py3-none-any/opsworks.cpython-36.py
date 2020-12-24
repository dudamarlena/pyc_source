# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/opsworks.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 28823 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.opsworks
from troposphere.opsworks import AutoScalingThresholds as _AutoScalingThresholds, BlockDeviceMapping as _BlockDeviceMapping, ChefConfiguration as _ChefConfiguration, DataSource as _DataSource, EbsBlockDevice as _EbsBlockDevice, ElasticIp as _ElasticIp, EngineAttribute as _EngineAttribute, Environment as _Environment, LifeCycleConfiguration as _LifeCycleConfiguration, LoadBasedAutoScaling as _LoadBasedAutoScaling, RdsDbInstance as _RdsDbInstance, Recipes as _Recipes, ShutdownEventConfiguration as _ShutdownEventConfiguration, Source as _Source, SslConfiguration as _SslConfiguration, StackConfigurationManager as _StackConfigurationManager, Tags as _Tags, TimeBasedAutoScaling as _TimeBasedAutoScaling, VolumeConfiguration as _VolumeConfiguration
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Source(troposphere.opsworks.Source, Mixin):

    def __init__(self, title=None, Password=NOTHING, Revision=NOTHING, SshKey=NOTHING, Type=NOTHING, Url=NOTHING, Username=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Password=Password, 
         Revision=Revision, 
         SshKey=SshKey, 
         Type=Type, 
         Url=Url, 
         Username=Username, **kwargs)
        (super(Source, self).__init__)(**processed_kwargs)


class SslConfiguration(troposphere.opsworks.SslConfiguration, Mixin):

    def __init__(self, title=None, Certificate=REQUIRED, PrivateKey=REQUIRED, Chain=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Certificate=Certificate, 
         PrivateKey=PrivateKey, 
         Chain=Chain, **kwargs)
        (super(SslConfiguration, self).__init__)(**processed_kwargs)


class ChefConfiguration(troposphere.opsworks.ChefConfiguration, Mixin):

    def __init__(self, title=None, BerkshelfVersion=NOTHING, ManageBerkshelf=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BerkshelfVersion=BerkshelfVersion, 
         ManageBerkshelf=ManageBerkshelf, **kwargs)
        (super(ChefConfiguration, self).__init__)(**processed_kwargs)


class Recipes(troposphere.opsworks.Recipes, Mixin):

    def __init__(self, title=None, Configure=NOTHING, Deploy=NOTHING, Setup=NOTHING, Shutdown=NOTHING, Undeploy=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Configure=Configure, 
         Deploy=Deploy, 
         Setup=Setup, 
         Shutdown=Shutdown, 
         Undeploy=Undeploy, **kwargs)
        (super(Recipes, self).__init__)(**processed_kwargs)


class VolumeConfiguration(troposphere.opsworks.VolumeConfiguration, Mixin):

    def __init__(self, title=None, MountPoint=REQUIRED, NumberOfDisks=REQUIRED, Size=REQUIRED, Encrypted=NOTHING, Iops=NOTHING, RaidLevel=NOTHING, VolumeType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MountPoint=MountPoint, 
         NumberOfDisks=NumberOfDisks, 
         Size=Size, 
         Encrypted=Encrypted, 
         Iops=Iops, 
         RaidLevel=RaidLevel, 
         VolumeType=VolumeType, **kwargs)
        (super(VolumeConfiguration, self).__init__)(**processed_kwargs)


class StackConfigurationManager(troposphere.opsworks.StackConfigurationManager, Mixin):

    def __init__(self, title=None, Name=NOTHING, Version=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Version=Version, **kwargs)
        (super(StackConfigurationManager, self).__init__)(**processed_kwargs)


class TimeBasedAutoScaling(troposphere.opsworks.TimeBasedAutoScaling, Mixin):

    def __init__(self, title=None, Monday=NOTHING, Tuesday=NOTHING, Wednesday=NOTHING, Thursday=NOTHING, Friday=NOTHING, Saturday=NOTHING, Sunday=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Monday=Monday, 
         Tuesday=Tuesday, 
         Wednesday=Wednesday, 
         Thursday=Thursday, 
         Friday=Friday, 
         Saturday=Saturday, 
         Sunday=Sunday, **kwargs)
        (super(TimeBasedAutoScaling, self).__init__)(**processed_kwargs)


class AutoScalingThresholds(troposphere.opsworks.AutoScalingThresholds, Mixin):

    def __init__(self, title=None, CpuThreshold=NOTHING, IgnoreMetricsTime=NOTHING, InstanceCount=NOTHING, LoadThreshold=NOTHING, MemoryThreshold=NOTHING, ThresholdsWaitTime=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CpuThreshold=CpuThreshold, 
         IgnoreMetricsTime=IgnoreMetricsTime, 
         InstanceCount=InstanceCount, 
         LoadThreshold=LoadThreshold, 
         MemoryThreshold=MemoryThreshold, 
         ThresholdsWaitTime=ThresholdsWaitTime, **kwargs)
        (super(AutoScalingThresholds, self).__init__)(**processed_kwargs)


class Environment(troposphere.opsworks.Environment, Mixin):

    def __init__(self, title=None, Key=REQUIRED, Value=REQUIRED, Secure=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Value=Value, 
         Secure=Secure, **kwargs)
        (super(Environment, self).__init__)(**processed_kwargs)


class LoadBasedAutoScaling(troposphere.opsworks.LoadBasedAutoScaling, Mixin):

    def __init__(self, title=None, DownScaling=NOTHING, Enable=NOTHING, UpScaling=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DownScaling=DownScaling, 
         Enable=Enable, 
         UpScaling=UpScaling, **kwargs)
        (super(LoadBasedAutoScaling, self).__init__)(**processed_kwargs)


class DataSource(troposphere.opsworks.DataSource, Mixin):

    def __init__(self, title=None, Arn=NOTHING, DatabaseName=NOTHING, Type=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Arn=Arn, 
         DatabaseName=DatabaseName, 
         Type=Type, **kwargs)
        (super(DataSource, self).__init__)(**processed_kwargs)


class App(troposphere.opsworks.App, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, StackId=REQUIRED, Type=REQUIRED, AppSource=NOTHING, Attributes=NOTHING, DataSources=NOTHING, Description=NOTHING, Domains=NOTHING, EnableSsl=NOTHING, Environment=NOTHING, Shortname=NOTHING, SslConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         StackId=StackId, 
         Type=Type, 
         AppSource=AppSource, 
         Attributes=Attributes, 
         DataSources=DataSources, 
         Description=Description, 
         Domains=Domains, 
         EnableSsl=EnableSsl, 
         Environment=Environment, 
         Shortname=Shortname, 
         SslConfiguration=SslConfiguration, **kwargs)
        (super(App, self).__init__)(**processed_kwargs)


class ElasticLoadBalancerAttachment(troposphere.opsworks.ElasticLoadBalancerAttachment, Mixin):

    def __init__(self, title, template=None, validation=True, ElasticLoadBalancerName=REQUIRED, LayerId=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ElasticLoadBalancerName=ElasticLoadBalancerName, 
         LayerId=LayerId, 
         Tags=Tags, **kwargs)
        (super(ElasticLoadBalancerAttachment, self).__init__)(**processed_kwargs)


class EbsBlockDevice(troposphere.opsworks.EbsBlockDevice, Mixin):

    def __init__(self, title=None, DeleteOnTermination=NOTHING, Iops=NOTHING, SnapshotId=NOTHING, VolumeSize=NOTHING, VolumeType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeleteOnTermination=DeleteOnTermination, 
         Iops=Iops, 
         SnapshotId=SnapshotId, 
         VolumeSize=VolumeSize, 
         VolumeType=VolumeType, **kwargs)
        (super(EbsBlockDevice, self).__init__)(**processed_kwargs)


class BlockDeviceMapping(troposphere.opsworks.BlockDeviceMapping, Mixin):

    def __init__(self, title=None, DeviceName=NOTHING, Ebs=NOTHING, NoDevice=NOTHING, VirtualName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeviceName=DeviceName, 
         Ebs=Ebs, 
         NoDevice=NoDevice, 
         VirtualName=VirtualName, **kwargs)
        (super(BlockDeviceMapping, self).__init__)(**processed_kwargs)


class Instance(troposphere.opsworks.Instance, Mixin):

    def __init__(self, title, template=None, validation=True, InstanceType=REQUIRED, LayerIds=REQUIRED, StackId=REQUIRED, AgentVersion=NOTHING, AmiId=NOTHING, Architecture=NOTHING, AutoScalingType=NOTHING, AvailabilityZone=NOTHING, BlockDeviceMappings=NOTHING, EbsOptimized=NOTHING, ElasticIps=NOTHING, Hostname=NOTHING, InstallUpdatesOnBoot=NOTHING, Os=NOTHING, RootDeviceType=NOTHING, SshKeyName=NOTHING, SubnetId=NOTHING, Tenancy=NOTHING, TimeBasedAutoScaling=NOTHING, VirtualizationType=NOTHING, Volumes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         InstanceType=InstanceType, 
         LayerIds=LayerIds, 
         StackId=StackId, 
         AgentVersion=AgentVersion, 
         AmiId=AmiId, 
         Architecture=Architecture, 
         AutoScalingType=AutoScalingType, 
         AvailabilityZone=AvailabilityZone, 
         BlockDeviceMappings=BlockDeviceMappings, 
         EbsOptimized=EbsOptimized, 
         ElasticIps=ElasticIps, 
         Hostname=Hostname, 
         InstallUpdatesOnBoot=InstallUpdatesOnBoot, 
         Os=Os, 
         RootDeviceType=RootDeviceType, 
         SshKeyName=SshKeyName, 
         SubnetId=SubnetId, 
         Tenancy=Tenancy, 
         TimeBasedAutoScaling=TimeBasedAutoScaling, 
         VirtualizationType=VirtualizationType, 
         Volumes=Volumes, **kwargs)
        (super(Instance, self).__init__)(**processed_kwargs)


class ShutdownEventConfiguration(troposphere.opsworks.ShutdownEventConfiguration, Mixin):

    def __init__(self, title=None, DelayUntilElbConnectionsDrained=NOTHING, ExecutionTimeout=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DelayUntilElbConnectionsDrained=DelayUntilElbConnectionsDrained, 
         ExecutionTimeout=ExecutionTimeout, **kwargs)
        (super(ShutdownEventConfiguration, self).__init__)(**processed_kwargs)


class LifeCycleConfiguration(troposphere.opsworks.LifeCycleConfiguration, Mixin):

    def __init__(self, title=None, ShutdownEventConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ShutdownEventConfiguration=ShutdownEventConfiguration, **kwargs)
        (super(LifeCycleConfiguration, self).__init__)(**processed_kwargs)


class Layer(troposphere.opsworks.Layer, Mixin):

    def __init__(self, title, template=None, validation=True, AutoAssignElasticIps=REQUIRED, AutoAssignPublicIps=REQUIRED, EnableAutoHealing=REQUIRED, Name=REQUIRED, Shortname=REQUIRED, StackId=REQUIRED, Type=REQUIRED, Attributes=NOTHING, CustomInstanceProfileArn=NOTHING, CustomJson=NOTHING, CustomRecipes=NOTHING, CustomSecurityGroupIds=NOTHING, InstallUpdatesOnBoot=NOTHING, LifecycleEventConfiguration=NOTHING, LoadBasedAutoScaling=NOTHING, Packages=NOTHING, VolumeConfigurations=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AutoAssignElasticIps=AutoAssignElasticIps, 
         AutoAssignPublicIps=AutoAssignPublicIps, 
         EnableAutoHealing=EnableAutoHealing, 
         Name=Name, 
         Shortname=Shortname, 
         StackId=StackId, 
         Type=Type, 
         Attributes=Attributes, 
         CustomInstanceProfileArn=CustomInstanceProfileArn, 
         CustomJson=CustomJson, 
         CustomRecipes=CustomRecipes, 
         CustomSecurityGroupIds=CustomSecurityGroupIds, 
         InstallUpdatesOnBoot=InstallUpdatesOnBoot, 
         LifecycleEventConfiguration=LifecycleEventConfiguration, 
         LoadBasedAutoScaling=LoadBasedAutoScaling, 
         Packages=Packages, 
         VolumeConfigurations=VolumeConfigurations, **kwargs)
        (super(Layer, self).__init__)(**processed_kwargs)


class RdsDbInstance(troposphere.opsworks.RdsDbInstance, Mixin):

    def __init__(self, title=None, DbPassword=REQUIRED, DbUser=REQUIRED, RdsDbInstanceArn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DbPassword=DbPassword, 
         DbUser=DbUser, 
         RdsDbInstanceArn=RdsDbInstanceArn, **kwargs)
        (super(RdsDbInstance, self).__init__)(**processed_kwargs)


class ElasticIp(troposphere.opsworks.ElasticIp, Mixin):

    def __init__(self, title=None, Ip=REQUIRED, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Ip=Ip, 
         Name=Name, **kwargs)
        (super(ElasticIp, self).__init__)(**processed_kwargs)


class Stack(troposphere.opsworks.Stack, Mixin):

    def __init__(self, title, template=None, validation=True, DefaultInstanceProfileArn=REQUIRED, Name=REQUIRED, ServiceRoleArn=REQUIRED, AgentVersion=NOTHING, Attributes=NOTHING, ChefConfiguration=NOTHING, CloneAppIds=NOTHING, ClonePermissions=NOTHING, ConfigurationManager=NOTHING, CustomCookbooksSource=NOTHING, CustomJson=NOTHING, DefaultAvailabilityZone=NOTHING, DefaultOs=NOTHING, DefaultRootDeviceType=NOTHING, DefaultSshKeyName=NOTHING, DefaultSubnetId=NOTHING, EcsClusterArn=NOTHING, ElasticIps=NOTHING, HostnameTheme=NOTHING, RdsDbInstances=NOTHING, SourceStackId=NOTHING, Tags=NOTHING, UseCustomCookbooks=NOTHING, UseOpsworksSecurityGroups=NOTHING, VpcId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DefaultInstanceProfileArn=DefaultInstanceProfileArn, 
         Name=Name, 
         ServiceRoleArn=ServiceRoleArn, 
         AgentVersion=AgentVersion, 
         Attributes=Attributes, 
         ChefConfiguration=ChefConfiguration, 
         CloneAppIds=CloneAppIds, 
         ClonePermissions=ClonePermissions, 
         ConfigurationManager=ConfigurationManager, 
         CustomCookbooksSource=CustomCookbooksSource, 
         CustomJson=CustomJson, 
         DefaultAvailabilityZone=DefaultAvailabilityZone, 
         DefaultOs=DefaultOs, 
         DefaultRootDeviceType=DefaultRootDeviceType, 
         DefaultSshKeyName=DefaultSshKeyName, 
         DefaultSubnetId=DefaultSubnetId, 
         EcsClusterArn=EcsClusterArn, 
         ElasticIps=ElasticIps, 
         HostnameTheme=HostnameTheme, 
         RdsDbInstances=RdsDbInstances, 
         SourceStackId=SourceStackId, 
         Tags=Tags, 
         UseCustomCookbooks=UseCustomCookbooks, 
         UseOpsworksSecurityGroups=UseOpsworksSecurityGroups, 
         VpcId=VpcId, **kwargs)
        (super(Stack, self).__init__)(**processed_kwargs)


class UserProfile(troposphere.opsworks.UserProfile, Mixin):

    def __init__(self, title, template=None, validation=True, IamUserArn=REQUIRED, AllowSelfManagement=NOTHING, SshPublicKey=NOTHING, SshUsername=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         IamUserArn=IamUserArn, 
         AllowSelfManagement=AllowSelfManagement, 
         SshPublicKey=SshPublicKey, 
         SshUsername=SshUsername, **kwargs)
        (super(UserProfile, self).__init__)(**processed_kwargs)


class Volume(troposphere.opsworks.Volume, Mixin):

    def __init__(self, title, template=None, validation=True, Ec2VolumeId=REQUIRED, StackId=REQUIRED, MountPoint=NOTHING, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Ec2VolumeId=Ec2VolumeId, 
         StackId=StackId, 
         MountPoint=MountPoint, 
         Name=Name, **kwargs)
        (super(Volume, self).__init__)(**processed_kwargs)


class EngineAttribute(troposphere.opsworks.EngineAttribute, Mixin):

    def __init__(self, title=None, Name=NOTHING, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Value=Value, **kwargs)
        (super(EngineAttribute, self).__init__)(**processed_kwargs)


class Server(troposphere.opsworks.Server, Mixin):

    def __init__(self, title, template=None, validation=True, InstanceProfileArn=REQUIRED, InstanceType=REQUIRED, ServiceRoleArn=REQUIRED, AssociatePublicIpAddress=NOTHING, BackupId=NOTHING, BackupRetentionCount=NOTHING, CustomCertificate=NOTHING, CustomDomain=NOTHING, CustomPrivateKey=NOTHING, DisableAutomatedBackup=NOTHING, Engine=NOTHING, EngineAttributes=NOTHING, EngineModel=NOTHING, EngineVersion=NOTHING, KeyPair=NOTHING, PreferredBackupWindow=NOTHING, PreferredMaintenanceWindow=NOTHING, SecurityGroupIds=NOTHING, ServerName=NOTHING, SubnetIds=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         InstanceProfileArn=InstanceProfileArn, 
         InstanceType=InstanceType, 
         ServiceRoleArn=ServiceRoleArn, 
         AssociatePublicIpAddress=AssociatePublicIpAddress, 
         BackupId=BackupId, 
         BackupRetentionCount=BackupRetentionCount, 
         CustomCertificate=CustomCertificate, 
         CustomDomain=CustomDomain, 
         CustomPrivateKey=CustomPrivateKey, 
         DisableAutomatedBackup=DisableAutomatedBackup, 
         Engine=Engine, 
         EngineAttributes=EngineAttributes, 
         EngineModel=EngineModel, 
         EngineVersion=EngineVersion, 
         KeyPair=KeyPair, 
         PreferredBackupWindow=PreferredBackupWindow, 
         PreferredMaintenanceWindow=PreferredMaintenanceWindow, 
         SecurityGroupIds=SecurityGroupIds, 
         ServerName=ServerName, 
         SubnetIds=SubnetIds, **kwargs)
        (super(Server, self).__init__)(**processed_kwargs)