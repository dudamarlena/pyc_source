# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/emr.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 27453 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.emr
from troposphere.emr import Application as _Application, AutoScalingPolicy as _AutoScalingPolicy, BootstrapActionConfig as _BootstrapActionConfig, CloudWatchAlarmDefinition as _CloudWatchAlarmDefinition, Configuration as _Configuration, EbsBlockDeviceConfigs as _EbsBlockDeviceConfigs, EbsConfiguration as _EbsConfiguration, HadoopJarStepConfig as _HadoopJarStepConfig, InstanceFleetConfigProperty as _InstanceFleetConfigProperty, InstanceFleetProvisioningSpecifications as _InstanceFleetProvisioningSpecifications, InstanceGroupConfigProperty as _InstanceGroupConfigProperty, InstanceTypeConfig as _InstanceTypeConfig, JobFlowInstancesConfig as _JobFlowInstancesConfig, KerberosAttributes as _KerberosAttributes, KeyValue as _KeyValue, PlacementType as _PlacementType, ScalingAction as _ScalingAction, ScalingConstraints as _ScalingConstraints, ScalingRule as _ScalingRule, ScalingTrigger as _ScalingTrigger, ScriptBootstrapActionConfig as _ScriptBootstrapActionConfig, SimpleScalingPolicyConfiguration as _SimpleScalingPolicyConfiguration, SpotProvisioningSpecification as _SpotProvisioningSpecification, StepConfig as _StepConfig, Tags as _Tags, VolumeSpecification as _VolumeSpecification
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class KeyValue(troposphere.emr.KeyValue, Mixin):

    def __init__(self, title=None, Key=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Value=Value, **kwargs)
        (super(KeyValue, self).__init__)(**processed_kwargs)


class SecurityConfiguration(troposphere.emr.SecurityConfiguration, Mixin):

    def __init__(self, title, template=None, validation=True, SecurityConfiguration=REQUIRED, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         SecurityConfiguration=SecurityConfiguration, 
         Name=Name, **kwargs)
        (super(SecurityConfiguration, self).__init__)(**processed_kwargs)


class Application(troposphere.emr.Application, Mixin):

    def __init__(self, title=None, AdditionalInfo=NOTHING, Args=NOTHING, Name=NOTHING, Version=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AdditionalInfo=AdditionalInfo, 
         Args=Args, 
         Name=Name, 
         Version=Version, **kwargs)
        (super(Application, self).__init__)(**processed_kwargs)


class ScriptBootstrapActionConfig(troposphere.emr.ScriptBootstrapActionConfig, Mixin):

    def __init__(self, title=None, Path=REQUIRED, Args=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Path=Path, 
         Args=Args, **kwargs)
        (super(ScriptBootstrapActionConfig, self).__init__)(**processed_kwargs)


class BootstrapActionConfig(troposphere.emr.BootstrapActionConfig, Mixin):

    def __init__(self, title=None, Name=REQUIRED, ScriptBootstrapAction=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         ScriptBootstrapAction=ScriptBootstrapAction, **kwargs)
        (super(BootstrapActionConfig, self).__init__)(**processed_kwargs)


class Configuration(troposphere.emr.Configuration, Mixin):

    def __init__(self, title=None, Classification=NOTHING, ConfigurationProperties=NOTHING, Configurations=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Classification=Classification, 
         ConfigurationProperties=ConfigurationProperties, 
         Configurations=Configurations, **kwargs)
        (super(Configuration, self).__init__)(**processed_kwargs)


class VolumeSpecification(troposphere.emr.VolumeSpecification, Mixin):

    def __init__(self, title=None, SizeInGB=REQUIRED, VolumeType=REQUIRED, Iops=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SizeInGB=SizeInGB, 
         VolumeType=VolumeType, 
         Iops=Iops, **kwargs)
        (super(VolumeSpecification, self).__init__)(**processed_kwargs)


class EbsBlockDeviceConfigs(troposphere.emr.EbsBlockDeviceConfigs, Mixin):

    def __init__(self, title=None, VolumeSpecification=REQUIRED, VolumesPerInstance=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         VolumeSpecification=VolumeSpecification, 
         VolumesPerInstance=VolumesPerInstance, **kwargs)
        (super(EbsBlockDeviceConfigs, self).__init__)(**processed_kwargs)


class EbsConfiguration(troposphere.emr.EbsConfiguration, Mixin):

    def __init__(self, title=None, EbsBlockDeviceConfigs=NOTHING, EbsOptimized=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EbsBlockDeviceConfigs=EbsBlockDeviceConfigs, 
         EbsOptimized=EbsOptimized, **kwargs)
        (super(EbsConfiguration, self).__init__)(**processed_kwargs)


class ScalingConstraints(troposphere.emr.ScalingConstraints, Mixin):

    def __init__(self, title=None, MinCapacity=REQUIRED, MaxCapacity=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MinCapacity=MinCapacity, 
         MaxCapacity=MaxCapacity, **kwargs)
        (super(ScalingConstraints, self).__init__)(**processed_kwargs)


class CloudWatchAlarmDefinition(troposphere.emr.CloudWatchAlarmDefinition, Mixin):

    def __init__(self, title=None, ComparisonOperator=REQUIRED, MetricName=REQUIRED, Period=REQUIRED, Threshold=REQUIRED, Dimensions=NOTHING, EvaluationPeriods=NOTHING, Namespace=NOTHING, Statistic=NOTHING, Unit=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ComparisonOperator=ComparisonOperator, 
         MetricName=MetricName, 
         Period=Period, 
         Threshold=Threshold, 
         Dimensions=Dimensions, 
         EvaluationPeriods=EvaluationPeriods, 
         Namespace=Namespace, 
         Statistic=Statistic, 
         Unit=Unit, **kwargs)
        (super(CloudWatchAlarmDefinition, self).__init__)(**processed_kwargs)


class ScalingTrigger(troposphere.emr.ScalingTrigger, Mixin):

    def __init__(self, title=None, CloudWatchAlarmDefinition=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CloudWatchAlarmDefinition=CloudWatchAlarmDefinition, **kwargs)
        (super(ScalingTrigger, self).__init__)(**processed_kwargs)


class SimpleScalingPolicyConfiguration(troposphere.emr.SimpleScalingPolicyConfiguration, Mixin):

    def __init__(self, title=None, ScalingAdjustment=REQUIRED, AdjustmentType=NOTHING, CoolDown=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ScalingAdjustment=ScalingAdjustment, 
         AdjustmentType=AdjustmentType, 
         CoolDown=CoolDown, **kwargs)
        (super(SimpleScalingPolicyConfiguration, self).__init__)(**processed_kwargs)


class ScalingAction(troposphere.emr.ScalingAction, Mixin):

    def __init__(self, title=None, SimpleScalingPolicyConfiguration=REQUIRED, Market=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SimpleScalingPolicyConfiguration=SimpleScalingPolicyConfiguration, 
         Market=Market, **kwargs)
        (super(ScalingAction, self).__init__)(**processed_kwargs)


class ScalingRule(troposphere.emr.ScalingRule, Mixin):

    def __init__(self, title=None, Action=REQUIRED, Name=REQUIRED, Trigger=REQUIRED, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Action=Action, 
         Name=Name, 
         Trigger=Trigger, 
         Description=Description, **kwargs)
        (super(ScalingRule, self).__init__)(**processed_kwargs)


class AutoScalingPolicy(troposphere.emr.AutoScalingPolicy, Mixin):

    def __init__(self, title=None, Constraints=REQUIRED, Rules=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Constraints=Constraints, 
         Rules=Rules, **kwargs)
        (super(AutoScalingPolicy, self).__init__)(**processed_kwargs)


class InstanceGroupConfigProperty(troposphere.emr.InstanceGroupConfigProperty, Mixin):

    def __init__(self, title=None, InstanceCount=REQUIRED, InstanceType=REQUIRED, AutoScalingPolicy=NOTHING, BidPrice=NOTHING, Configurations=NOTHING, EbsConfiguration=NOTHING, Market=NOTHING, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         InstanceCount=InstanceCount, 
         InstanceType=InstanceType, 
         AutoScalingPolicy=AutoScalingPolicy, 
         BidPrice=BidPrice, 
         Configurations=Configurations, 
         EbsConfiguration=EbsConfiguration, 
         Market=Market, 
         Name=Name, **kwargs)
        (super(InstanceGroupConfigProperty, self).__init__)(**processed_kwargs)


class SpotProvisioningSpecification(troposphere.emr.SpotProvisioningSpecification, Mixin):

    def __init__(self, title=None, TimeoutAction=REQUIRED, TimeoutDurationMinutes=REQUIRED, BlockDurationMinutes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TimeoutAction=TimeoutAction, 
         TimeoutDurationMinutes=TimeoutDurationMinutes, 
         BlockDurationMinutes=BlockDurationMinutes, **kwargs)
        (super(SpotProvisioningSpecification, self).__init__)(**processed_kwargs)


class InstanceFleetProvisioningSpecifications(troposphere.emr.InstanceFleetProvisioningSpecifications, Mixin):

    def __init__(self, title=None, SpotSpecification=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SpotSpecification=SpotSpecification, **kwargs)
        (super(InstanceFleetProvisioningSpecifications, self).__init__)(**processed_kwargs)


class InstanceTypeConfig(troposphere.emr.InstanceTypeConfig, Mixin):

    def __init__(self, title=None, InstanceType=REQUIRED, BidPrice=NOTHING, BidPriceAsPercentageOfOnDemandPrice=NOTHING, Configurations=NOTHING, EbsConfiguration=NOTHING, WeightedCapacity=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         InstanceType=InstanceType, 
         BidPrice=BidPrice, 
         BidPriceAsPercentageOfOnDemandPrice=BidPriceAsPercentageOfOnDemandPrice, 
         Configurations=Configurations, 
         EbsConfiguration=EbsConfiguration, 
         WeightedCapacity=WeightedCapacity, **kwargs)
        (super(InstanceTypeConfig, self).__init__)(**processed_kwargs)


class InstanceFleetConfigProperty(troposphere.emr.InstanceFleetConfigProperty, Mixin):

    def __init__(self, title=None, InstanceTypeConfigs=NOTHING, LaunchSpecifications=NOTHING, Name=NOTHING, TargetOnDemandCapacity=NOTHING, TargetSpotCapacity=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         InstanceTypeConfigs=InstanceTypeConfigs, 
         LaunchSpecifications=LaunchSpecifications, 
         Name=Name, 
         TargetOnDemandCapacity=TargetOnDemandCapacity, 
         TargetSpotCapacity=TargetSpotCapacity, **kwargs)
        (super(InstanceFleetConfigProperty, self).__init__)(**processed_kwargs)


class PlacementType(troposphere.emr.PlacementType, Mixin):

    def __init__(self, title=None, AvailabilityZone=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AvailabilityZone=AvailabilityZone, **kwargs)
        (super(PlacementType, self).__init__)(**processed_kwargs)


class JobFlowInstancesConfig(troposphere.emr.JobFlowInstancesConfig, Mixin):

    def __init__(self, title=None, AdditionalMasterSecurityGroups=NOTHING, AdditionalSlaveSecurityGroups=NOTHING, CoreInstanceFleet=NOTHING, CoreInstanceGroup=NOTHING, Ec2KeyName=NOTHING, Ec2SubnetId=NOTHING, Ec2SubnetIds=NOTHING, EmrManagedMasterSecurityGroup=NOTHING, EmrManagedSlaveSecurityGroup=NOTHING, HadoopVersion=NOTHING, KeepJobFlowAliveWhenNoSteps=NOTHING, MasterInstanceFleet=NOTHING, MasterInstanceGroup=NOTHING, Placement=NOTHING, ServiceAccessSecurityGroup=NOTHING, TerminationProtected=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AdditionalMasterSecurityGroups=AdditionalMasterSecurityGroups, 
         AdditionalSlaveSecurityGroups=AdditionalSlaveSecurityGroups, 
         CoreInstanceFleet=CoreInstanceFleet, 
         CoreInstanceGroup=CoreInstanceGroup, 
         Ec2KeyName=Ec2KeyName, 
         Ec2SubnetId=Ec2SubnetId, 
         Ec2SubnetIds=Ec2SubnetIds, 
         EmrManagedMasterSecurityGroup=EmrManagedMasterSecurityGroup, 
         EmrManagedSlaveSecurityGroup=EmrManagedSlaveSecurityGroup, 
         HadoopVersion=HadoopVersion, 
         KeepJobFlowAliveWhenNoSteps=KeepJobFlowAliveWhenNoSteps, 
         MasterInstanceFleet=MasterInstanceFleet, 
         MasterInstanceGroup=MasterInstanceGroup, 
         Placement=Placement, 
         ServiceAccessSecurityGroup=ServiceAccessSecurityGroup, 
         TerminationProtected=TerminationProtected, **kwargs)
        (super(JobFlowInstancesConfig, self).__init__)(**processed_kwargs)


class KerberosAttributes(troposphere.emr.KerberosAttributes, Mixin):

    def __init__(self, title=None, KdcAdminPassword=REQUIRED, Realm=REQUIRED, ADDomainJoinPassword=NOTHING, ADDomainJoinUser=NOTHING, CrossRealmTrustPrincipalPassword=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         KdcAdminPassword=KdcAdminPassword, 
         Realm=Realm, 
         ADDomainJoinPassword=ADDomainJoinPassword, 
         ADDomainJoinUser=ADDomainJoinUser, 
         CrossRealmTrustPrincipalPassword=CrossRealmTrustPrincipalPassword, **kwargs)
        (super(KerberosAttributes, self).__init__)(**processed_kwargs)


class HadoopJarStepConfig(troposphere.emr.HadoopJarStepConfig, Mixin):

    def __init__(self, title=None, Jar=REQUIRED, Args=NOTHING, MainClass=NOTHING, StepProperties=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Jar=Jar, 
         Args=Args, 
         MainClass=MainClass, 
         StepProperties=StepProperties, **kwargs)
        (super(HadoopJarStepConfig, self).__init__)(**processed_kwargs)


class StepConfig(troposphere.emr.StepConfig, Mixin):

    def __init__(self, title=None, HadoopJarStep=REQUIRED, Name=REQUIRED, ActionOnFailure=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HadoopJarStep=HadoopJarStep, 
         Name=Name, 
         ActionOnFailure=ActionOnFailure, **kwargs)
        (super(StepConfig, self).__init__)(**processed_kwargs)


class Cluster(troposphere.emr.Cluster, Mixin):

    def __init__(self, title, template=None, validation=True, Instances=REQUIRED, JobFlowRole=REQUIRED, Name=REQUIRED, ServiceRole=REQUIRED, AdditionalInfo=NOTHING, Applications=NOTHING, AutoScalingRole=NOTHING, BootstrapActions=NOTHING, Configurations=NOTHING, CustomAmiId=NOTHING, EbsRootVolumeSize=NOTHING, KerberosAttributes=NOTHING, LogUri=NOTHING, ReleaseLabel=NOTHING, ScaleDownBehavior=NOTHING, SecurityConfiguration=NOTHING, Steps=NOTHING, Tags=NOTHING, VisibleToAllUsers=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Instances=Instances, 
         JobFlowRole=JobFlowRole, 
         Name=Name, 
         ServiceRole=ServiceRole, 
         AdditionalInfo=AdditionalInfo, 
         Applications=Applications, 
         AutoScalingRole=AutoScalingRole, 
         BootstrapActions=BootstrapActions, 
         Configurations=Configurations, 
         CustomAmiId=CustomAmiId, 
         EbsRootVolumeSize=EbsRootVolumeSize, 
         KerberosAttributes=KerberosAttributes, 
         LogUri=LogUri, 
         ReleaseLabel=ReleaseLabel, 
         ScaleDownBehavior=ScaleDownBehavior, 
         SecurityConfiguration=SecurityConfiguration, 
         Steps=Steps, 
         Tags=Tags, 
         VisibleToAllUsers=VisibleToAllUsers, **kwargs)
        (super(Cluster, self).__init__)(**processed_kwargs)


class InstanceFleetConfig(troposphere.emr.InstanceFleetConfig, Mixin):

    def __init__(self, title, template=None, validation=True, ClusterId=REQUIRED, InstanceFleetType=REQUIRED, InstanceTypeConfigs=NOTHING, LaunchSpecifications=NOTHING, Name=NOTHING, TargetOnDemandCapacity=NOTHING, TargetSpotCapacity=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ClusterId=ClusterId, 
         InstanceFleetType=InstanceFleetType, 
         InstanceTypeConfigs=InstanceTypeConfigs, 
         LaunchSpecifications=LaunchSpecifications, 
         Name=Name, 
         TargetOnDemandCapacity=TargetOnDemandCapacity, 
         TargetSpotCapacity=TargetSpotCapacity, **kwargs)
        (super(InstanceFleetConfig, self).__init__)(**processed_kwargs)


class InstanceGroupConfig(troposphere.emr.InstanceGroupConfig, Mixin):

    def __init__(self, title, template=None, validation=True, InstanceCount=REQUIRED, InstanceRole=REQUIRED, InstanceType=REQUIRED, JobFlowId=REQUIRED, AutoScalingPolicy=NOTHING, BidPrice=NOTHING, Configurations=NOTHING, EbsConfiguration=NOTHING, Market=NOTHING, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         InstanceCount=InstanceCount, 
         InstanceRole=InstanceRole, 
         InstanceType=InstanceType, 
         JobFlowId=JobFlowId, 
         AutoScalingPolicy=AutoScalingPolicy, 
         BidPrice=BidPrice, 
         Configurations=Configurations, 
         EbsConfiguration=EbsConfiguration, 
         Market=Market, 
         Name=Name, **kwargs)
        (super(InstanceGroupConfig, self).__init__)(**processed_kwargs)


class Step(troposphere.emr.Step, Mixin):

    def __init__(self, title, template=None, validation=True, ActionOnFailure=REQUIRED, HadoopJarStep=REQUIRED, JobFlowId=REQUIRED, Name=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ActionOnFailure=ActionOnFailure, 
         HadoopJarStep=HadoopJarStep, 
         JobFlowId=JobFlowId, 
         Name=Name, **kwargs)
        (super(Step, self).__init__)(**processed_kwargs)