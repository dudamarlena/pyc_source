# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/batch.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 13848 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.batch
from troposphere.batch import ComputeEnvironmentOrder as _ComputeEnvironmentOrder, ComputeResources as _ComputeResources, ContainerProperties as _ContainerProperties, Device as _Device, Environment as _Environment, LaunchTemplateSpecification as _LaunchTemplateSpecification, LinuxParameters as _LinuxParameters, MountPoints as _MountPoints, ResourceRequirement as _ResourceRequirement, RetryStrategy as _RetryStrategy, Timeout as _Timeout, Ulimit as _Ulimit, Volumes as _Volumes, VolumesHost as _VolumesHost
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class LaunchTemplateSpecification(troposphere.batch.LaunchTemplateSpecification, Mixin):

    def __init__(self, title=None, LaunchTemplateId=NOTHING, LaunchTemplateName=NOTHING, Version=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LaunchTemplateId=LaunchTemplateId, 
         LaunchTemplateName=LaunchTemplateName, 
         Version=Version, **kwargs)
        (super(LaunchTemplateSpecification, self).__init__)(**processed_kwargs)


class ComputeResources(troposphere.batch.ComputeResources, Mixin):

    def __init__(self, title=None, MaxvCpus=REQUIRED, SecurityGroupIds=REQUIRED, Type=REQUIRED, Subnets=REQUIRED, MinvCpus=REQUIRED, InstanceRole=REQUIRED, InstanceTypes=REQUIRED, AllocationStrategy=NOTHING, SpotIamFleetRole=NOTHING, BidPercentage=NOTHING, LaunchTemplate=NOTHING, ImageId=NOTHING, Ec2KeyPair=NOTHING, PlacementGroup=NOTHING, Tags=NOTHING, DesiredvCpus=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MaxvCpus=MaxvCpus, 
         SecurityGroupIds=SecurityGroupIds, 
         Type=Type, 
         Subnets=Subnets, 
         MinvCpus=MinvCpus, 
         InstanceRole=InstanceRole, 
         InstanceTypes=InstanceTypes, 
         AllocationStrategy=AllocationStrategy, 
         SpotIamFleetRole=SpotIamFleetRole, 
         BidPercentage=BidPercentage, 
         LaunchTemplate=LaunchTemplate, 
         ImageId=ImageId, 
         Ec2KeyPair=Ec2KeyPair, 
         PlacementGroup=PlacementGroup, 
         Tags=Tags, 
         DesiredvCpus=DesiredvCpus, **kwargs)
        (super(ComputeResources, self).__init__)(**processed_kwargs)


class Device(troposphere.batch.Device, Mixin):

    def __init__(self, title=None, ContainerPath=NOTHING, HostPath=NOTHING, Permissions=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ContainerPath=ContainerPath, 
         HostPath=HostPath, 
         Permissions=Permissions, **kwargs)
        (super(Device, self).__init__)(**processed_kwargs)


class LinuxParameters(troposphere.batch.LinuxParameters, Mixin):

    def __init__(self, title=None, Devices=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Devices=Devices, **kwargs)
        (super(LinuxParameters, self).__init__)(**processed_kwargs)


class MountPoints(troposphere.batch.MountPoints, Mixin):

    def __init__(self, title=None, ReadOnly=NOTHING, SourceVolume=NOTHING, ContainerPath=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ReadOnly=ReadOnly, 
         SourceVolume=SourceVolume, 
         ContainerPath=ContainerPath, **kwargs)
        (super(MountPoints, self).__init__)(**processed_kwargs)


class VolumesHost(troposphere.batch.VolumesHost, Mixin):

    def __init__(self, title=None, SourcePath=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SourcePath=SourcePath, **kwargs)
        (super(VolumesHost, self).__init__)(**processed_kwargs)


class Volumes(troposphere.batch.Volumes, Mixin):

    def __init__(self, title=None, Host=NOTHING, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Host=Host, 
         Name=Name, **kwargs)
        (super(Volumes, self).__init__)(**processed_kwargs)


class Environment(troposphere.batch.Environment, Mixin):

    def __init__(self, title=None, Value=NOTHING, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Value=Value, 
         Name=Name, **kwargs)
        (super(Environment, self).__init__)(**processed_kwargs)


class ResourceRequirement(troposphere.batch.ResourceRequirement, Mixin):

    def __init__(self, title=None, Type=NOTHING, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         Value=Value, **kwargs)
        (super(ResourceRequirement, self).__init__)(**processed_kwargs)


class Ulimit(troposphere.batch.Ulimit, Mixin):

    def __init__(self, title=None, SoftLimit=REQUIRED, HardLimit=REQUIRED, Name=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SoftLimit=SoftLimit, 
         HardLimit=HardLimit, 
         Name=Name, **kwargs)
        (super(Ulimit, self).__init__)(**processed_kwargs)


class ContainerProperties(troposphere.batch.ContainerProperties, Mixin):

    def __init__(self, title=None, Image=REQUIRED, Memory=REQUIRED, Vcpus=REQUIRED, Command=NOTHING, Environment=NOTHING, InstanceType=NOTHING, JobRoleArn=NOTHING, LinuxParameters=NOTHING, MountPoints=NOTHING, Privileged=NOTHING, ReadonlyRootFilesystem=NOTHING, ResourceRequirements=NOTHING, Ulimits=NOTHING, User=NOTHING, Volumes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Image=Image, 
         Memory=Memory, 
         Vcpus=Vcpus, 
         Command=Command, 
         Environment=Environment, 
         InstanceType=InstanceType, 
         JobRoleArn=JobRoleArn, 
         LinuxParameters=LinuxParameters, 
         MountPoints=MountPoints, 
         Privileged=Privileged, 
         ReadonlyRootFilesystem=ReadonlyRootFilesystem, 
         ResourceRequirements=ResourceRequirements, 
         Ulimits=Ulimits, 
         User=User, 
         Volumes=Volumes, **kwargs)
        (super(ContainerProperties, self).__init__)(**processed_kwargs)


class RetryStrategy(troposphere.batch.RetryStrategy, Mixin):

    def __init__(self, title=None, Attempts=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Attempts=Attempts, **kwargs)
        (super(RetryStrategy, self).__init__)(**processed_kwargs)


class Timeout(troposphere.batch.Timeout, Mixin):

    def __init__(self, title=None, AttemptDurationSeconds=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AttemptDurationSeconds=AttemptDurationSeconds, **kwargs)
        (super(Timeout, self).__init__)(**processed_kwargs)


class JobDefinition(troposphere.batch.JobDefinition, Mixin):

    def __init__(self, title, template=None, validation=True, ContainerProperties=REQUIRED, Type=REQUIRED, JobDefinitionName=NOTHING, Parameters=NOTHING, RetryStrategy=NOTHING, Timeout=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ContainerProperties=ContainerProperties, 
         Type=Type, 
         JobDefinitionName=JobDefinitionName, 
         Parameters=Parameters, 
         RetryStrategy=RetryStrategy, 
         Timeout=Timeout, **kwargs)
        (super(JobDefinition, self).__init__)(**processed_kwargs)


class ComputeEnvironment(troposphere.batch.ComputeEnvironment, Mixin):

    def __init__(self, title, template=None, validation=True, Type=REQUIRED, ServiceRole=REQUIRED, ComputeResources=REQUIRED, ComputeEnvironmentName=NOTHING, State=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Type=Type, 
         ServiceRole=ServiceRole, 
         ComputeResources=ComputeResources, 
         ComputeEnvironmentName=ComputeEnvironmentName, 
         State=State, **kwargs)
        (super(ComputeEnvironment, self).__init__)(**processed_kwargs)


class ComputeEnvironmentOrder(troposphere.batch.ComputeEnvironmentOrder, Mixin):

    def __init__(self, title=None, ComputeEnvironment=REQUIRED, Order=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ComputeEnvironment=ComputeEnvironment, 
         Order=Order, **kwargs)
        (super(ComputeEnvironmentOrder, self).__init__)(**processed_kwargs)


class JobQueue(troposphere.batch.JobQueue, Mixin):

    def __init__(self, title, template=None, validation=True, ComputeEnvironmentOrder=REQUIRED, Priority=REQUIRED, State=NOTHING, JobQueueName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ComputeEnvironmentOrder=ComputeEnvironmentOrder, 
         Priority=Priority, 
         State=State, 
         JobQueueName=JobQueueName, **kwargs)
        (super(JobQueue, self).__init__)(**processed_kwargs)