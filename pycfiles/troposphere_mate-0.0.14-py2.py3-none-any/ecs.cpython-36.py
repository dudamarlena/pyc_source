# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/ecs.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 32294 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.ecs
from troposphere.ecs import AwsvpcConfiguration as _AwsvpcConfiguration, ClusterSetting as _ClusterSetting, ContainerDefinition as _ContainerDefinition, ContainerDependency as _ContainerDependency, DeploymentConfiguration as _DeploymentConfiguration, DeploymentController as _DeploymentController, Device as _Device, DockerVolumeConfiguration as _DockerVolumeConfiguration, Environment as _Environment, FirelensConfiguration as _FirelensConfiguration, HealthCheck as _HealthCheck, Host as _Host, HostEntry as _HostEntry, InferenceAccelerator as _InferenceAccelerator, KernelCapabilities as _KernelCapabilities, LinuxParameters as _LinuxParameters, LoadBalancer as _LoadBalancer, LogConfiguration as _LogConfiguration, MountPoint as _MountPoint, NetworkConfiguration as _NetworkConfiguration, PlacementConstraint as _PlacementConstraint, PlacementStrategy as _PlacementStrategy, PortMapping as _PortMapping, ProxyConfiguration as _ProxyConfiguration, RepositoryCredentials as _RepositoryCredentials, ResourceRequirement as _ResourceRequirement, Scale as _Scale, Secret as _Secret, ServiceRegistry as _ServiceRegistry, SystemControl as _SystemControl, Tags as _Tags, Tmpfs as _Tmpfs, Ulimit as _Ulimit, Volume as _Volume, VolumesFrom as _VolumesFrom
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class ClusterSetting(troposphere.ecs.ClusterSetting, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Value=Value, **kwargs)
        (super(ClusterSetting, self).__init__)(**processed_kwargs)


class Cluster(troposphere.ecs.Cluster, Mixin):

    def __init__(self, title, template=None, validation=True, ClusterName=NOTHING, ClusterSettings=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ClusterName=ClusterName, 
         ClusterSettings=ClusterSettings, 
         Tags=Tags, **kwargs)
        (super(Cluster, self).__init__)(**processed_kwargs)


class PrimaryTaskSet(troposphere.ecs.PrimaryTaskSet, Mixin):

    def __init__(self, title, template=None, validation=True, Cluster=REQUIRED, Service=REQUIRED, TaskSetId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Cluster=Cluster, 
         Service=Service, 
         TaskSetId=TaskSetId, **kwargs)
        (super(PrimaryTaskSet, self).__init__)(**processed_kwargs)


class LoadBalancer(troposphere.ecs.LoadBalancer, Mixin):

    def __init__(self, title=None, ContainerPort=REQUIRED, ContainerName=NOTHING, LoadBalancerName=NOTHING, TargetGroupArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ContainerPort=ContainerPort, 
         ContainerName=ContainerName, 
         LoadBalancerName=LoadBalancerName, 
         TargetGroupArn=TargetGroupArn, **kwargs)
        (super(LoadBalancer, self).__init__)(**processed_kwargs)


class DeploymentConfiguration(troposphere.ecs.DeploymentConfiguration, Mixin):

    def __init__(self, title=None, MaximumPercent=NOTHING, MinimumHealthyPercent=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MaximumPercent=MaximumPercent, 
         MinimumHealthyPercent=MinimumHealthyPercent, **kwargs)
        (super(DeploymentConfiguration, self).__init__)(**processed_kwargs)


class DeploymentController(troposphere.ecs.DeploymentController, Mixin):

    def __init__(self, title=None, Type=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, **kwargs)
        (super(DeploymentController, self).__init__)(**processed_kwargs)


class PlacementConstraint(troposphere.ecs.PlacementConstraint, Mixin):

    def __init__(self, title=None, Type=REQUIRED, Expression=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         Expression=Expression, **kwargs)
        (super(PlacementConstraint, self).__init__)(**processed_kwargs)


class PlacementStrategy(troposphere.ecs.PlacementStrategy, Mixin):

    def __init__(self, title=None, Type=REQUIRED, Field=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         Field=Field, **kwargs)
        (super(PlacementStrategy, self).__init__)(**processed_kwargs)


class AwsvpcConfiguration(troposphere.ecs.AwsvpcConfiguration, Mixin):

    def __init__(self, title=None, Subnets=REQUIRED, AssignPublicIp=NOTHING, SecurityGroups=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Subnets=Subnets, 
         AssignPublicIp=AssignPublicIp, 
         SecurityGroups=SecurityGroups, **kwargs)
        (super(AwsvpcConfiguration, self).__init__)(**processed_kwargs)


class NetworkConfiguration(troposphere.ecs.NetworkConfiguration, Mixin):

    def __init__(self, title=None, AwsvpcConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AwsvpcConfiguration=AwsvpcConfiguration, **kwargs)
        (super(NetworkConfiguration, self).__init__)(**processed_kwargs)


class ServiceRegistry(troposphere.ecs.ServiceRegistry, Mixin):

    def __init__(self, title=None, ContainerName=NOTHING, ContainerPort=NOTHING, Port=NOTHING, RegistryArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ContainerName=ContainerName, 
         ContainerPort=ContainerPort, 
         Port=Port, 
         RegistryArn=RegistryArn, **kwargs)
        (super(ServiceRegistry, self).__init__)(**processed_kwargs)


class Service(troposphere.ecs.Service, Mixin):

    def __init__(self, title, template=None, validation=True, TaskDefinition=REQUIRED, Cluster=NOTHING, DeploymentConfiguration=NOTHING, DeploymentController=NOTHING, DesiredCount=NOTHING, EnableECSManagedTags=NOTHING, HealthCheckGracePeriodSeconds=NOTHING, LaunchType=NOTHING, LoadBalancers=NOTHING, NetworkConfiguration=NOTHING, Role=NOTHING, PlacementConstraints=NOTHING, PlacementStrategies=NOTHING, PlatformVersion=NOTHING, PropagateTags=NOTHING, SchedulingStrategy=NOTHING, ServiceName=NOTHING, ServiceRegistries=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         TaskDefinition=TaskDefinition, 
         Cluster=Cluster, 
         DeploymentConfiguration=DeploymentConfiguration, 
         DeploymentController=DeploymentController, 
         DesiredCount=DesiredCount, 
         EnableECSManagedTags=EnableECSManagedTags, 
         HealthCheckGracePeriodSeconds=HealthCheckGracePeriodSeconds, 
         LaunchType=LaunchType, 
         LoadBalancers=LoadBalancers, 
         NetworkConfiguration=NetworkConfiguration, 
         Role=Role, 
         PlacementConstraints=PlacementConstraints, 
         PlacementStrategies=PlacementStrategies, 
         PlatformVersion=PlatformVersion, 
         PropagateTags=PropagateTags, 
         SchedulingStrategy=SchedulingStrategy, 
         ServiceName=ServiceName, 
         ServiceRegistries=ServiceRegistries, 
         Tags=Tags, **kwargs)
        (super(Service, self).__init__)(**processed_kwargs)


class Environment(troposphere.ecs.Environment, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Value=Value, **kwargs)
        (super(Environment, self).__init__)(**processed_kwargs)


class MountPoint(troposphere.ecs.MountPoint, Mixin):

    def __init__(self, title=None, ContainerPath=REQUIRED, SourceVolume=REQUIRED, ReadOnly=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ContainerPath=ContainerPath, 
         SourceVolume=SourceVolume, 
         ReadOnly=ReadOnly, **kwargs)
        (super(MountPoint, self).__init__)(**processed_kwargs)


class PortMapping(troposphere.ecs.PortMapping, Mixin):

    def __init__(self, title=None, ContainerPort=REQUIRED, HostPort=NOTHING, Protocol=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ContainerPort=ContainerPort, 
         HostPort=HostPort, 
         Protocol=Protocol, **kwargs)
        (super(PortMapping, self).__init__)(**processed_kwargs)


class VolumesFrom(troposphere.ecs.VolumesFrom, Mixin):

    def __init__(self, title=None, SourceContainer=REQUIRED, ReadOnly=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SourceContainer=SourceContainer, 
         ReadOnly=ReadOnly, **kwargs)
        (super(VolumesFrom, self).__init__)(**processed_kwargs)


class HostEntry(troposphere.ecs.HostEntry, Mixin):

    def __init__(self, title=None, Hostname=REQUIRED, IpAddress=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Hostname=Hostname, 
         IpAddress=IpAddress, **kwargs)
        (super(HostEntry, self).__init__)(**processed_kwargs)


class Device(troposphere.ecs.Device, Mixin):

    def __init__(self, title=None, ContainerPath=NOTHING, HostPath=NOTHING, Permissions=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ContainerPath=ContainerPath, 
         HostPath=HostPath, 
         Permissions=Permissions, **kwargs)
        (super(Device, self).__init__)(**processed_kwargs)


class FirelensConfiguration(troposphere.ecs.FirelensConfiguration, Mixin):

    def __init__(self, title=None, Type=REQUIRED, Options=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         Options=Options, **kwargs)
        (super(FirelensConfiguration, self).__init__)(**processed_kwargs)


class HealthCheck(troposphere.ecs.HealthCheck, Mixin):

    def __init__(self, title=None, Command=REQUIRED, Interval=NOTHING, Retries=NOTHING, StartPeriod=NOTHING, Timeout=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Command=Command, 
         Interval=Interval, 
         Retries=Retries, 
         StartPeriod=StartPeriod, 
         Timeout=Timeout, **kwargs)
        (super(HealthCheck, self).__init__)(**processed_kwargs)


class KernelCapabilities(troposphere.ecs.KernelCapabilities, Mixin):

    def __init__(self, title=None, Add=NOTHING, Drop=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Add=Add, 
         Drop=Drop, **kwargs)
        (super(KernelCapabilities, self).__init__)(**processed_kwargs)


class Tmpfs(troposphere.ecs.Tmpfs, Mixin):

    def __init__(self, title=None, ContainerPath=NOTHING, MountOptions=NOTHING, Size=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ContainerPath=ContainerPath, 
         MountOptions=MountOptions, 
         Size=Size, **kwargs)
        (super(Tmpfs, self).__init__)(**processed_kwargs)


class LinuxParameters(troposphere.ecs.LinuxParameters, Mixin):

    def __init__(self, title=None, Capabilities=NOTHING, Devices=NOTHING, InitProcessEnabled=NOTHING, SharedMemorySize=NOTHING, Tmpfs=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Capabilities=Capabilities, 
         Devices=Devices, 
         InitProcessEnabled=InitProcessEnabled, 
         SharedMemorySize=SharedMemorySize, 
         Tmpfs=Tmpfs, **kwargs)
        (super(LinuxParameters, self).__init__)(**processed_kwargs)


class Secret(troposphere.ecs.Secret, Mixin):

    def __init__(self, title=None, Name=REQUIRED, ValueFrom=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         ValueFrom=ValueFrom, **kwargs)
        (super(Secret, self).__init__)(**processed_kwargs)


class LogConfiguration(troposphere.ecs.LogConfiguration, Mixin):

    def __init__(self, title=None, LogDriver=REQUIRED, Options=NOTHING, SecretOptions=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LogDriver=LogDriver, 
         Options=Options, 
         SecretOptions=SecretOptions, **kwargs)
        (super(LogConfiguration, self).__init__)(**processed_kwargs)


class RepositoryCredentials(troposphere.ecs.RepositoryCredentials, Mixin):

    def __init__(self, title=None, CredentialsParameter=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CredentialsParameter=CredentialsParameter, **kwargs)
        (super(RepositoryCredentials, self).__init__)(**processed_kwargs)


class ResourceRequirement(troposphere.ecs.ResourceRequirement, Mixin):

    def __init__(self, title=None, Type=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         Value=Value, **kwargs)
        (super(ResourceRequirement, self).__init__)(**processed_kwargs)


class SystemControl(troposphere.ecs.SystemControl, Mixin):

    def __init__(self, title=None, Namespace=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Namespace=Namespace, 
         Value=Value, **kwargs)
        (super(SystemControl, self).__init__)(**processed_kwargs)


class Ulimit(troposphere.ecs.Ulimit, Mixin):

    def __init__(self, title=None, HardLimit=REQUIRED, Name=REQUIRED, SoftLimit=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HardLimit=HardLimit, 
         Name=Name, 
         SoftLimit=SoftLimit, **kwargs)
        (super(Ulimit, self).__init__)(**processed_kwargs)


class ContainerDependency(troposphere.ecs.ContainerDependency, Mixin):

    def __init__(self, title=None, Condition=REQUIRED, ContainerName=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Condition=Condition, 
         ContainerName=ContainerName, **kwargs)
        (super(ContainerDependency, self).__init__)(**processed_kwargs)


class ContainerDefinition(troposphere.ecs.ContainerDefinition, Mixin):

    def __init__(self, title, Command, Cpu, DependsOn, DisableNetworking, DnsSearchDomains, DnsServers, DockerLabels, DockerSecurityOptions, EntryPoint, Environment, Essential, ExtraHosts, FirelensConfiguration, HealthCheck, Hostname, Image, Interactive, Links, LinuxParameters, LogConfiguration, Memory, MemoryReservation, MountPoints, Name, PortMappings, Privileged, PseudoTerminal, ReadonlyRootFilesystem, RepositoryCredentials, ResourceRequirements, Secrets=NoneNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHING, StartTimeout=NOTHING, StopTimeout=NOTHING, SystemControls=NOTHING, Ulimits=NOTHING, User=NOTHING, VolumesFrom=NOTHING, WorkingDirectory=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Command=Command, 
         Cpu=Cpu, 
         DependsOn=DependsOn, 
         DisableNetworking=DisableNetworking, 
         DnsSearchDomains=DnsSearchDomains, 
         DnsServers=DnsServers, 
         DockerLabels=DockerLabels, 
         DockerSecurityOptions=DockerSecurityOptions, 
         EntryPoint=EntryPoint, 
         Environment=Environment, 
         Essential=Essential, 
         ExtraHosts=ExtraHosts, 
         FirelensConfiguration=FirelensConfiguration, 
         HealthCheck=HealthCheck, 
         Hostname=Hostname, 
         Image=Image, 
         Interactive=Interactive, 
         Links=Links, 
         LinuxParameters=LinuxParameters, 
         LogConfiguration=LogConfiguration, 
         Memory=Memory, 
         MemoryReservation=MemoryReservation, 
         MountPoints=MountPoints, 
         Name=Name, 
         PortMappings=PortMappings, 
         Privileged=Privileged, 
         PseudoTerminal=PseudoTerminal, 
         ReadonlyRootFilesystem=ReadonlyRootFilesystem, 
         RepositoryCredentials=RepositoryCredentials, 
         ResourceRequirements=ResourceRequirements, 
         Secrets=Secrets, 
         StartTimeout=StartTimeout, 
         StopTimeout=StopTimeout, 
         SystemControls=SystemControls, 
         Ulimits=Ulimits, 
         User=User, 
         VolumesFrom=VolumesFrom, 
         WorkingDirectory=WorkingDirectory, **kwargs)
        (super(ContainerDefinition, self).__init__)(**processed_kwargs)


class Host(troposphere.ecs.Host, Mixin):

    def __init__(self, title=None, SourcePath=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SourcePath=SourcePath, **kwargs)
        (super(Host, self).__init__)(**processed_kwargs)


class DockerVolumeConfiguration(troposphere.ecs.DockerVolumeConfiguration, Mixin):

    def __init__(self, title=None, Autoprovision=NOTHING, Driver=NOTHING, DriverOpts=NOTHING, Labels=NOTHING, Scope=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Autoprovision=Autoprovision, 
         Driver=Driver, 
         DriverOpts=DriverOpts, 
         Labels=Labels, 
         Scope=Scope, **kwargs)
        (super(DockerVolumeConfiguration, self).__init__)(**processed_kwargs)


class Volume(troposphere.ecs.Volume, Mixin):

    def __init__(self, title=None, Name=REQUIRED, DockerVolumeConfiguration=NOTHING, Host=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         DockerVolumeConfiguration=DockerVolumeConfiguration, 
         Host=Host, **kwargs)
        (super(Volume, self).__init__)(**processed_kwargs)


class InferenceAccelerator(troposphere.ecs.InferenceAccelerator, Mixin):

    def __init__(self, title=None, DeviceName=NOTHING, DeviceType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeviceName=DeviceName, 
         DeviceType=DeviceType, **kwargs)
        (super(InferenceAccelerator, self).__init__)(**processed_kwargs)


class ProxyConfiguration(troposphere.ecs.ProxyConfiguration, Mixin):

    def __init__(self, title=None, ContainerName=REQUIRED, ProxyConfigurationProperties=NOTHING, Type=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ContainerName=ContainerName, 
         ProxyConfigurationProperties=ProxyConfigurationProperties, 
         Type=Type, **kwargs)
        (super(ProxyConfiguration, self).__init__)(**processed_kwargs)


class TaskDefinition(troposphere.ecs.TaskDefinition, Mixin):

    def __init__(self, title, template=None, validation=True, ContainerDefinitions=NOTHING, Cpu=NOTHING, ExecutionRoleArn=NOTHING, Family=NOTHING, InferenceAccelerators=NOTHING, IpcMode=NOTHING, Memory=NOTHING, NetworkMode=NOTHING, PidMode=NOTHING, PlacementConstraints=NOTHING, ProxyConfiguration=NOTHING, RequiresCompatibilities=NOTHING, Tags=NOTHING, TaskRoleArn=NOTHING, Volumes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ContainerDefinitions=ContainerDefinitions, 
         Cpu=Cpu, 
         ExecutionRoleArn=ExecutionRoleArn, 
         Family=Family, 
         InferenceAccelerators=InferenceAccelerators, 
         IpcMode=IpcMode, 
         Memory=Memory, 
         NetworkMode=NetworkMode, 
         PidMode=PidMode, 
         PlacementConstraints=PlacementConstraints, 
         ProxyConfiguration=ProxyConfiguration, 
         RequiresCompatibilities=RequiresCompatibilities, 
         Tags=Tags, 
         TaskRoleArn=TaskRoleArn, 
         Volumes=Volumes, **kwargs)
        (super(TaskDefinition, self).__init__)(**processed_kwargs)


class Scale(troposphere.ecs.Scale, Mixin):

    def __init__(self, title=None, Unit=NOTHING, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Unit=Unit, 
         Value=Value, **kwargs)
        (super(Scale, self).__init__)(**processed_kwargs)


class TaskSet(troposphere.ecs.TaskSet, Mixin):

    def __init__(self, title, template=None, validation=True, Cluster=REQUIRED, Service=REQUIRED, TaskDefinition=REQUIRED, ExternalId=NOTHING, LaunchType=NOTHING, LoadBalancers=NOTHING, NetworkConfiguration=NOTHING, PlatformVersion=NOTHING, Scale=NOTHING, ServiceRegistries=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Cluster=Cluster, 
         Service=Service, 
         TaskDefinition=TaskDefinition, 
         ExternalId=ExternalId, 
         LaunchType=LaunchType, 
         LoadBalancers=LoadBalancers, 
         NetworkConfiguration=NetworkConfiguration, 
         PlatformVersion=PlatformVersion, 
         Scale=Scale, 
         ServiceRegistries=ServiceRegistries, **kwargs)
        (super(TaskSet, self).__init__)(**processed_kwargs)