# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/autoscaling.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 23910 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.autoscaling
from troposphere.autoscaling import CustomizedMetricSpecification as _CustomizedMetricSpecification, EBSBlockDevice as _EBSBlockDevice, InstancesDistribution as _InstancesDistribution, LaunchTemplate as _LaunchTemplate, LaunchTemplateOverrides as _LaunchTemplateOverrides, LaunchTemplateSpecification as _LaunchTemplateSpecification, LifecycleHookSpecification as _LifecycleHookSpecification, Metadata as _Metadata, MetricDimension as _MetricDimension, MetricsCollection as _MetricsCollection, MixedInstancesPolicy as _MixedInstancesPolicy, NotificationConfigurations as _NotificationConfigurations, PredefinedMetricSpecification as _PredefinedMetricSpecification, StepAdjustments as _StepAdjustments, Tags as _Tags, TargetTrackingConfiguration as _TargetTrackingConfiguration
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class LifecycleHookSpecification(troposphere.autoscaling.LifecycleHookSpecification, Mixin):

    def __init__(self, title=None, LifecycleHookName=REQUIRED, LifecycleTransition=REQUIRED, DefaultResult=NOTHING, HeartbeatTimeout=NOTHING, NotificationMetadata=NOTHING, NotificationTargetARN=NOTHING, RoleARN=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LifecycleHookName=LifecycleHookName, 
         LifecycleTransition=LifecycleTransition, 
         DefaultResult=DefaultResult, 
         HeartbeatTimeout=HeartbeatTimeout, 
         NotificationMetadata=NotificationMetadata, 
         NotificationTargetARN=NotificationTargetARN, 
         RoleARN=RoleARN, **kwargs)
        (super(LifecycleHookSpecification, self).__init__)(**processed_kwargs)


class NotificationConfigurations(troposphere.autoscaling.NotificationConfigurations, Mixin):

    def __init__(self, title=None, TopicARN=REQUIRED, NotificationTypes=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TopicARN=TopicARN, 
         NotificationTypes=NotificationTypes, **kwargs)
        (super(NotificationConfigurations, self).__init__)(**processed_kwargs)


class MetricsCollection(troposphere.autoscaling.MetricsCollection, Mixin):

    def __init__(self, title=None, Granularity=REQUIRED, Metrics=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Granularity=Granularity, 
         Metrics=Metrics, **kwargs)
        (super(MetricsCollection, self).__init__)(**processed_kwargs)


class LaunchTemplateSpecification(troposphere.autoscaling.LaunchTemplateSpecification, Mixin):

    def __init__(self, title=None, Version=REQUIRED, LaunchTemplateId=NOTHING, LaunchTemplateName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Version=Version, 
         LaunchTemplateId=LaunchTemplateId, 
         LaunchTemplateName=LaunchTemplateName, **kwargs)
        (super(LaunchTemplateSpecification, self).__init__)(**processed_kwargs)


class InstancesDistribution(troposphere.autoscaling.InstancesDistribution, Mixin):

    def __init__(self, title=None, OnDemandAllocationStrategy=NOTHING, OnDemandBaseCapacity=NOTHING, OnDemandPercentageAboveBaseCapacity=NOTHING, SpotAllocationStrategy=NOTHING, SpotInstancePools=NOTHING, SpotMaxPrice=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         OnDemandAllocationStrategy=OnDemandAllocationStrategy, 
         OnDemandBaseCapacity=OnDemandBaseCapacity, 
         OnDemandPercentageAboveBaseCapacity=OnDemandPercentageAboveBaseCapacity, 
         SpotAllocationStrategy=SpotAllocationStrategy, 
         SpotInstancePools=SpotInstancePools, 
         SpotMaxPrice=SpotMaxPrice, **kwargs)
        (super(InstancesDistribution, self).__init__)(**processed_kwargs)


class LaunchTemplateOverrides(troposphere.autoscaling.LaunchTemplateOverrides, Mixin):

    def __init__(self, title=None, InstanceType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         InstanceType=InstanceType, **kwargs)
        (super(LaunchTemplateOverrides, self).__init__)(**processed_kwargs)


class LaunchTemplate(troposphere.autoscaling.LaunchTemplate, Mixin):

    def __init__(self, title=None, LaunchTemplateSpecification=REQUIRED, Overrides=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LaunchTemplateSpecification=LaunchTemplateSpecification, 
         Overrides=Overrides, **kwargs)
        (super(LaunchTemplate, self).__init__)(**processed_kwargs)


class MixedInstancesPolicy(troposphere.autoscaling.MixedInstancesPolicy, Mixin):

    def __init__(self, title=None, LaunchTemplate=REQUIRED, InstancesDistribution=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LaunchTemplate=LaunchTemplate, 
         InstancesDistribution=InstancesDistribution, **kwargs)
        (super(MixedInstancesPolicy, self).__init__)(**processed_kwargs)


class AutoScalingGroup(troposphere.autoscaling.AutoScalingGroup, Mixin):

    def __init__(self, title, template=None, validation=True, MaxSize=REQUIRED, MinSize=REQUIRED, AutoScalingGroupName=NOTHING, AvailabilityZones=NOTHING, Cooldown=NOTHING, DesiredCapacity=NOTHING, HealthCheckGracePeriod=NOTHING, HealthCheckType=NOTHING, InstanceId=NOTHING, LaunchConfigurationName=NOTHING, LaunchTemplate=NOTHING, LifecycleHookSpecificationList=NOTHING, LoadBalancerNames=NOTHING, MetricsCollection=NOTHING, MixedInstancesPolicy=NOTHING, NotificationConfigurations=NOTHING, PlacementGroup=NOTHING, ServiceLinkedRoleARN=NOTHING, Tags=NOTHING, TargetGroupARNs=NOTHING, TerminationPolicies=NOTHING, VPCZoneIdentifier=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         MaxSize=MaxSize, 
         MinSize=MinSize, 
         AutoScalingGroupName=AutoScalingGroupName, 
         AvailabilityZones=AvailabilityZones, 
         Cooldown=Cooldown, 
         DesiredCapacity=DesiredCapacity, 
         HealthCheckGracePeriod=HealthCheckGracePeriod, 
         HealthCheckType=HealthCheckType, 
         InstanceId=InstanceId, 
         LaunchConfigurationName=LaunchConfigurationName, 
         LaunchTemplate=LaunchTemplate, 
         LifecycleHookSpecificationList=LifecycleHookSpecificationList, 
         LoadBalancerNames=LoadBalancerNames, 
         MetricsCollection=MetricsCollection, 
         MixedInstancesPolicy=MixedInstancesPolicy, 
         NotificationConfigurations=NotificationConfigurations, 
         PlacementGroup=PlacementGroup, 
         ServiceLinkedRoleARN=ServiceLinkedRoleARN, 
         Tags=Tags, 
         TargetGroupARNs=TargetGroupARNs, 
         TerminationPolicies=TerminationPolicies, 
         VPCZoneIdentifier=VPCZoneIdentifier, **kwargs)
        (super(AutoScalingGroup, self).__init__)(**processed_kwargs)


class LaunchConfiguration(troposphere.autoscaling.LaunchConfiguration, Mixin):

    def __init__(self, title, template=None, validation=True, ImageId=REQUIRED, InstanceType=REQUIRED, AssociatePublicIpAddress=NOTHING, BlockDeviceMappings=NOTHING, ClassicLinkVPCId=NOTHING, ClassicLinkVPCSecurityGroups=NOTHING, EbsOptimized=NOTHING, IamInstanceProfile=NOTHING, InstanceId=NOTHING, InstanceMonitoring=NOTHING, KernelId=NOTHING, KeyName=NOTHING, LaunchConfigurationName=NOTHING, Metadata=NOTHING, PlacementTenancy=NOTHING, RamDiskId=NOTHING, SecurityGroups=NOTHING, SpotPrice=NOTHING, UserData=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ImageId=ImageId, 
         InstanceType=InstanceType, 
         AssociatePublicIpAddress=AssociatePublicIpAddress, 
         BlockDeviceMappings=BlockDeviceMappings, 
         ClassicLinkVPCId=ClassicLinkVPCId, 
         ClassicLinkVPCSecurityGroups=ClassicLinkVPCSecurityGroups, 
         EbsOptimized=EbsOptimized, 
         IamInstanceProfile=IamInstanceProfile, 
         InstanceId=InstanceId, 
         InstanceMonitoring=InstanceMonitoring, 
         KernelId=KernelId, 
         KeyName=KeyName, 
         LaunchConfigurationName=LaunchConfigurationName, 
         Metadata=Metadata, 
         PlacementTenancy=PlacementTenancy, 
         RamDiskId=RamDiskId, 
         SecurityGroups=SecurityGroups, 
         SpotPrice=SpotPrice, 
         UserData=UserData, **kwargs)
        (super(LaunchConfiguration, self).__init__)(**processed_kwargs)


class StepAdjustments(troposphere.autoscaling.StepAdjustments, Mixin):

    def __init__(self, title=None, ScalingAdjustment=REQUIRED, MetricIntervalLowerBound=NOTHING, MetricIntervalUpperBound=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ScalingAdjustment=ScalingAdjustment, 
         MetricIntervalLowerBound=MetricIntervalLowerBound, 
         MetricIntervalUpperBound=MetricIntervalUpperBound, **kwargs)
        (super(StepAdjustments, self).__init__)(**processed_kwargs)


class MetricDimension(troposphere.autoscaling.MetricDimension, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Value=Value, **kwargs)
        (super(MetricDimension, self).__init__)(**processed_kwargs)


class CustomizedMetricSpecification(troposphere.autoscaling.CustomizedMetricSpecification, Mixin):

    def __init__(self, title=None, MetricName=REQUIRED, Namespace=REQUIRED, Statistic=REQUIRED, Dimensions=NOTHING, Unit=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MetricName=MetricName, 
         Namespace=Namespace, 
         Statistic=Statistic, 
         Dimensions=Dimensions, 
         Unit=Unit, **kwargs)
        (super(CustomizedMetricSpecification, self).__init__)(**processed_kwargs)


class PredefinedMetricSpecification(troposphere.autoscaling.PredefinedMetricSpecification, Mixin):

    def __init__(self, title=None, PredefinedMetricType=REQUIRED, ResourceLabel=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PredefinedMetricType=PredefinedMetricType, 
         ResourceLabel=ResourceLabel, **kwargs)
        (super(PredefinedMetricSpecification, self).__init__)(**processed_kwargs)


class TargetTrackingConfiguration(troposphere.autoscaling.TargetTrackingConfiguration, Mixin):

    def __init__(self, title=None, TargetValue=REQUIRED, CustomizedMetricSpecification=NOTHING, DisableScaleIn=NOTHING, PredefinedMetricSpecification=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TargetValue=TargetValue, 
         CustomizedMetricSpecification=CustomizedMetricSpecification, 
         DisableScaleIn=DisableScaleIn, 
         PredefinedMetricSpecification=PredefinedMetricSpecification, **kwargs)
        (super(TargetTrackingConfiguration, self).__init__)(**processed_kwargs)


class ScalingPolicy(troposphere.autoscaling.ScalingPolicy, Mixin):

    def __init__(self, title, template=None, validation=True, AutoScalingGroupName=REQUIRED, AdjustmentType=NOTHING, Cooldown=NOTHING, EstimatedInstanceWarmup=NOTHING, MetricAggregationType=NOTHING, MinAdjustmentMagnitude=NOTHING, PolicyType=NOTHING, ScalingAdjustment=NOTHING, StepAdjustments=NOTHING, TargetTrackingConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AutoScalingGroupName=AutoScalingGroupName, 
         AdjustmentType=AdjustmentType, 
         Cooldown=Cooldown, 
         EstimatedInstanceWarmup=EstimatedInstanceWarmup, 
         MetricAggregationType=MetricAggregationType, 
         MinAdjustmentMagnitude=MinAdjustmentMagnitude, 
         PolicyType=PolicyType, 
         ScalingAdjustment=ScalingAdjustment, 
         StepAdjustments=StepAdjustments, 
         TargetTrackingConfiguration=TargetTrackingConfiguration, **kwargs)
        (super(ScalingPolicy, self).__init__)(**processed_kwargs)


class ScheduledAction(troposphere.autoscaling.ScheduledAction, Mixin):

    def __init__(self, title, template=None, validation=True, AutoScalingGroupName=REQUIRED, DesiredCapacity=NOTHING, EndTime=NOTHING, MaxSize=NOTHING, MinSize=NOTHING, Recurrence=NOTHING, StartTime=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AutoScalingGroupName=AutoScalingGroupName, 
         DesiredCapacity=DesiredCapacity, 
         EndTime=EndTime, 
         MaxSize=MaxSize, 
         MinSize=MinSize, 
         Recurrence=Recurrence, 
         StartTime=StartTime, **kwargs)
        (super(ScheduledAction, self).__init__)(**processed_kwargs)


class LifecycleHook(troposphere.autoscaling.LifecycleHook, Mixin):

    def __init__(self, title, template=None, validation=True, AutoScalingGroupName=REQUIRED, LifecycleTransition=REQUIRED, DefaultResult=NOTHING, HeartbeatTimeout=NOTHING, LifecycleHookName=NOTHING, NotificationMetadata=NOTHING, NotificationTargetARN=NOTHING, RoleARN=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AutoScalingGroupName=AutoScalingGroupName, 
         LifecycleTransition=LifecycleTransition, 
         DefaultResult=DefaultResult, 
         HeartbeatTimeout=HeartbeatTimeout, 
         LifecycleHookName=LifecycleHookName, 
         NotificationMetadata=NotificationMetadata, 
         NotificationTargetARN=NotificationTargetARN, 
         RoleARN=RoleARN, **kwargs)
        (super(LifecycleHook, self).__init__)(**processed_kwargs)


class Trigger(troposphere.autoscaling.Trigger, Mixin):

    def __init__(self, title, template=None, validation=True, AutoScalingGroupName=REQUIRED, BreachDuration=REQUIRED, Dimensions=REQUIRED, LowerThreshold=REQUIRED, MetricName=REQUIRED, Namespace=REQUIRED, Period=REQUIRED, Statistic=REQUIRED, UpperThreshold=REQUIRED, LowerBreachScaleIncrement=NOTHING, Unit=NOTHING, UpperBreachScaleIncrement=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AutoScalingGroupName=AutoScalingGroupName, 
         BreachDuration=BreachDuration, 
         Dimensions=Dimensions, 
         LowerThreshold=LowerThreshold, 
         MetricName=MetricName, 
         Namespace=Namespace, 
         Period=Period, 
         Statistic=Statistic, 
         UpperThreshold=UpperThreshold, 
         LowerBreachScaleIncrement=LowerBreachScaleIncrement, 
         Unit=Unit, 
         UpperBreachScaleIncrement=UpperBreachScaleIncrement, **kwargs)
        (super(Trigger, self).__init__)(**processed_kwargs)


class EBSBlockDevice(troposphere.autoscaling.EBSBlockDevice, Mixin):

    def __init__(self, title=None, DeleteOnTermination=NOTHING, Encrypted=NOTHING, Iops=NOTHING, SnapshotId=NOTHING, VolumeSize=NOTHING, VolumeType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeleteOnTermination=DeleteOnTermination, 
         Encrypted=Encrypted, 
         Iops=Iops, 
         SnapshotId=SnapshotId, 
         VolumeSize=VolumeSize, 
         VolumeType=VolumeType, **kwargs)
        (super(EBSBlockDevice, self).__init__)(**processed_kwargs)


class BlockDeviceMapping(troposphere.autoscaling.BlockDeviceMapping, Mixin):

    def __init__(self, title=None, DeviceName=REQUIRED, Ebs=NOTHING, NoDevice=NOTHING, VirtualName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeviceName=DeviceName, 
         Ebs=Ebs, 
         NoDevice=NoDevice, 
         VirtualName=VirtualName, **kwargs)
        (super(BlockDeviceMapping, self).__init__)(**processed_kwargs)