# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/applicationautoscaling.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 10903 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.applicationautoscaling
from troposphere.applicationautoscaling import CustomizedMetricSpecification as _CustomizedMetricSpecification, MetricDimension as _MetricDimension, PredefinedMetricSpecification as _PredefinedMetricSpecification, ScalableTargetAction as _ScalableTargetAction, ScheduledAction as _ScheduledAction, StepAdjustment as _StepAdjustment, StepScalingPolicyConfiguration as _StepScalingPolicyConfiguration, SuspendedState as _SuspendedState, TargetTrackingScalingPolicyConfiguration as _TargetTrackingScalingPolicyConfiguration
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class ScalableTargetAction(troposphere.applicationautoscaling.ScalableTargetAction, Mixin):

    def __init__(self, title=None, MaxCapacity=NOTHING, MinCapacity=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MaxCapacity=MaxCapacity, 
         MinCapacity=MinCapacity, **kwargs)
        (super(ScalableTargetAction, self).__init__)(**processed_kwargs)


class ScheduledAction(troposphere.applicationautoscaling.ScheduledAction, Mixin):

    def __init__(self, title=None, Schedule=REQUIRED, ScheduledActionName=REQUIRED, EndTime=NOTHING, ScalableTargetAction=NOTHING, StartTime=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Schedule=Schedule, 
         ScheduledActionName=ScheduledActionName, 
         EndTime=EndTime, 
         ScalableTargetAction=ScalableTargetAction, 
         StartTime=StartTime, **kwargs)
        (super(ScheduledAction, self).__init__)(**processed_kwargs)


class SuspendedState(troposphere.applicationautoscaling.SuspendedState, Mixin):

    def __init__(self, title=None, DynamicScalingInSuspended=NOTHING, DynamicScalingOutSuspended=NOTHING, ScheduledScalingSuspended=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DynamicScalingInSuspended=DynamicScalingInSuspended, 
         DynamicScalingOutSuspended=DynamicScalingOutSuspended, 
         ScheduledScalingSuspended=ScheduledScalingSuspended, **kwargs)
        (super(SuspendedState, self).__init__)(**processed_kwargs)


class ScalableTarget(troposphere.applicationautoscaling.ScalableTarget, Mixin):

    def __init__(self, title, template=None, validation=True, MaxCapacity=REQUIRED, MinCapacity=REQUIRED, ResourceId=REQUIRED, RoleARN=REQUIRED, ScalableDimension=REQUIRED, ServiceNamespace=REQUIRED, ScheduledActions=NOTHING, SuspendedState=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         MaxCapacity=MaxCapacity, 
         MinCapacity=MinCapacity, 
         ResourceId=ResourceId, 
         RoleARN=RoleARN, 
         ScalableDimension=ScalableDimension, 
         ServiceNamespace=ServiceNamespace, 
         ScheduledActions=ScheduledActions, 
         SuspendedState=SuspendedState, **kwargs)
        (super(ScalableTarget, self).__init__)(**processed_kwargs)


class StepAdjustment(troposphere.applicationautoscaling.StepAdjustment, Mixin):

    def __init__(self, title=None, ScalingAdjustment=REQUIRED, MetricIntervalLowerBound=NOTHING, MetricIntervalUpperBound=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ScalingAdjustment=ScalingAdjustment, 
         MetricIntervalLowerBound=MetricIntervalLowerBound, 
         MetricIntervalUpperBound=MetricIntervalUpperBound, **kwargs)
        (super(StepAdjustment, self).__init__)(**processed_kwargs)


class StepScalingPolicyConfiguration(troposphere.applicationautoscaling.StepScalingPolicyConfiguration, Mixin):

    def __init__(self, title=None, AdjustmentType=NOTHING, Cooldown=NOTHING, MetricAggregationType=NOTHING, MinAdjustmentMagnitude=NOTHING, StepAdjustments=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AdjustmentType=AdjustmentType, 
         Cooldown=Cooldown, 
         MetricAggregationType=MetricAggregationType, 
         MinAdjustmentMagnitude=MinAdjustmentMagnitude, 
         StepAdjustments=StepAdjustments, **kwargs)
        (super(StepScalingPolicyConfiguration, self).__init__)(**processed_kwargs)


class MetricDimension(troposphere.applicationautoscaling.MetricDimension, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Value=Value, **kwargs)
        (super(MetricDimension, self).__init__)(**processed_kwargs)


class CustomizedMetricSpecification(troposphere.applicationautoscaling.CustomizedMetricSpecification, Mixin):

    def __init__(self, title=None, Unit=REQUIRED, Dimensions=NOTHING, MetricName=NOTHING, Namespace=NOTHING, Statistic=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Unit=Unit, 
         Dimensions=Dimensions, 
         MetricName=MetricName, 
         Namespace=Namespace, 
         Statistic=Statistic, **kwargs)
        (super(CustomizedMetricSpecification, self).__init__)(**processed_kwargs)


class PredefinedMetricSpecification(troposphere.applicationautoscaling.PredefinedMetricSpecification, Mixin):

    def __init__(self, title=None, PredefinedMetricType=REQUIRED, ResourceLabel=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PredefinedMetricType=PredefinedMetricType, 
         ResourceLabel=ResourceLabel, **kwargs)
        (super(PredefinedMetricSpecification, self).__init__)(**processed_kwargs)


class TargetTrackingScalingPolicyConfiguration(troposphere.applicationautoscaling.TargetTrackingScalingPolicyConfiguration, Mixin):

    def __init__(self, title=None, TargetValue=REQUIRED, CustomizedMetricSpecification=NOTHING, DisableScaleIn=NOTHING, PredefinedMetricSpecification=NOTHING, ScaleInCooldown=NOTHING, ScaleOutCooldown=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TargetValue=TargetValue, 
         CustomizedMetricSpecification=CustomizedMetricSpecification, 
         DisableScaleIn=DisableScaleIn, 
         PredefinedMetricSpecification=PredefinedMetricSpecification, 
         ScaleInCooldown=ScaleInCooldown, 
         ScaleOutCooldown=ScaleOutCooldown, **kwargs)
        (super(TargetTrackingScalingPolicyConfiguration, self).__init__)(**processed_kwargs)


class ScalingPolicy(troposphere.applicationautoscaling.ScalingPolicy, Mixin):

    def __init__(self, title, template=None, validation=True, PolicyName=REQUIRED, PolicyType=NOTHING, ResourceId=NOTHING, ScalableDimension=NOTHING, ServiceNamespace=NOTHING, ScalingTargetId=NOTHING, StepScalingPolicyConfiguration=NOTHING, TargetTrackingScalingPolicyConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PolicyName=PolicyName, 
         PolicyType=PolicyType, 
         ResourceId=ResourceId, 
         ScalableDimension=ScalableDimension, 
         ServiceNamespace=ServiceNamespace, 
         ScalingTargetId=ScalingTargetId, 
         StepScalingPolicyConfiguration=StepScalingPolicyConfiguration, 
         TargetTrackingScalingPolicyConfiguration=TargetTrackingScalingPolicyConfiguration, **kwargs)
        (super(ScalingPolicy, self).__init__)(**processed_kwargs)