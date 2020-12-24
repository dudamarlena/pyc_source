# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/autoscalingplans.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 10070 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.autoscalingplans
from troposphere.autoscalingplans import ApplicationSource as _ApplicationSource, CustomizedLoadMetricSpecification as _CustomizedLoadMetricSpecification, CustomizedScalingMetricSpecification as _CustomizedScalingMetricSpecification, MetricDimension as _MetricDimension, PredefinedLoadMetricSpecification as _PredefinedLoadMetricSpecification, PredefinedScalingMetricSpecification as _PredefinedScalingMetricSpecification, ScalingInstruction as _ScalingInstruction, TagFilter as _TagFilter, TargetTrackingConfiguration as _TargetTrackingConfiguration
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class TagFilter(troposphere.autoscalingplans.TagFilter, Mixin):

    def __init__(self, title=None, Key=REQUIRED, Values=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Values=Values, **kwargs)
        (super(TagFilter, self).__init__)(**processed_kwargs)


class ApplicationSource(troposphere.autoscalingplans.ApplicationSource, Mixin):

    def __init__(self, title=None, CloudFormationStackARN=NOTHING, TagFilters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CloudFormationStackARN=CloudFormationStackARN, 
         TagFilters=TagFilters, **kwargs)
        (super(ApplicationSource, self).__init__)(**processed_kwargs)


class PredefinedScalingMetricSpecification(troposphere.autoscalingplans.PredefinedScalingMetricSpecification, Mixin):

    def __init__(self, title=None, PredefinedScalingMetricType=REQUIRED, ResourceLabel=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PredefinedScalingMetricType=PredefinedScalingMetricType, 
         ResourceLabel=ResourceLabel, **kwargs)
        (super(PredefinedScalingMetricSpecification, self).__init__)(**processed_kwargs)


class MetricDimension(troposphere.autoscalingplans.MetricDimension, Mixin):

    def __init__(self, title=None, Value=REQUIRED, Name=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Value=Value, 
         Name=Name, **kwargs)
        (super(MetricDimension, self).__init__)(**processed_kwargs)


class CustomizedScalingMetricSpecification(troposphere.autoscalingplans.CustomizedScalingMetricSpecification, Mixin):

    def __init__(self, title=None, MetricName=REQUIRED, Statistic=REQUIRED, Namespace=REQUIRED, Dimensions=NOTHING, Unit=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MetricName=MetricName, 
         Statistic=Statistic, 
         Namespace=Namespace, 
         Dimensions=Dimensions, 
         Unit=Unit, **kwargs)
        (super(CustomizedScalingMetricSpecification, self).__init__)(**processed_kwargs)


class TargetTrackingConfiguration(troposphere.autoscalingplans.TargetTrackingConfiguration, Mixin):

    def __init__(self, title=None, TargetValue=REQUIRED, ScaleOutCooldown=NOTHING, PredefinedScalingMetricSpecification=NOTHING, DisableScaleIn=NOTHING, ScaleInCooldown=NOTHING, EstimatedInstanceWarmup=NOTHING, CustomizedScalingMetricSpecification=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TargetValue=TargetValue, 
         ScaleOutCooldown=ScaleOutCooldown, 
         PredefinedScalingMetricSpecification=PredefinedScalingMetricSpecification, 
         DisableScaleIn=DisableScaleIn, 
         ScaleInCooldown=ScaleInCooldown, 
         EstimatedInstanceWarmup=EstimatedInstanceWarmup, 
         CustomizedScalingMetricSpecification=CustomizedScalingMetricSpecification, **kwargs)
        (super(TargetTrackingConfiguration, self).__init__)(**processed_kwargs)


class CustomizedLoadMetricSpecification(troposphere.autoscalingplans.CustomizedLoadMetricSpecification, Mixin):

    def __init__(self, title, template=None, validation=True, MetricName=REQUIRED, Namespace=REQUIRED, Statistic=REQUIRED, Dimensions=NOTHING, Unit=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         MetricName=MetricName, 
         Namespace=Namespace, 
         Statistic=Statistic, 
         Dimensions=Dimensions, 
         Unit=Unit, **kwargs)
        (super(CustomizedLoadMetricSpecification, self).__init__)(**processed_kwargs)


class PredefinedLoadMetricSpecification(troposphere.autoscalingplans.PredefinedLoadMetricSpecification, Mixin):

    def __init__(self, title=None, PredefinedLoadMetricType=REQUIRED, ResourceLabel=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PredefinedLoadMetricType=PredefinedLoadMetricType, 
         ResourceLabel=ResourceLabel, **kwargs)
        (super(PredefinedLoadMetricSpecification, self).__init__)(**processed_kwargs)


class ScalingInstruction(troposphere.autoscalingplans.ScalingInstruction, Mixin):

    def __init__(self, title=None, MaxCapacity=REQUIRED, MinCapacity=REQUIRED, ResourceId=REQUIRED, ScalableDimension=REQUIRED, ServiceNamespace=REQUIRED, TargetTrackingConfigurations=REQUIRED, CustomizedLoadMetricSpecification=NOTHING, DisableDynamicScaling=NOTHING, PredefinedLoadMetricSpecification=NOTHING, PredictiveScalingMaxCapacityBehavior=NOTHING, PredictiveScalingMaxCapacityBuffer=NOTHING, PredictiveScalingMode=NOTHING, ScalingPolicyUpdateBehavior=NOTHING, ScheduledActionBufferTime=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MaxCapacity=MaxCapacity, 
         MinCapacity=MinCapacity, 
         ResourceId=ResourceId, 
         ScalableDimension=ScalableDimension, 
         ServiceNamespace=ServiceNamespace, 
         TargetTrackingConfigurations=TargetTrackingConfigurations, 
         CustomizedLoadMetricSpecification=CustomizedLoadMetricSpecification, 
         DisableDynamicScaling=DisableDynamicScaling, 
         PredefinedLoadMetricSpecification=PredefinedLoadMetricSpecification, 
         PredictiveScalingMaxCapacityBehavior=PredictiveScalingMaxCapacityBehavior, 
         PredictiveScalingMaxCapacityBuffer=PredictiveScalingMaxCapacityBuffer, 
         PredictiveScalingMode=PredictiveScalingMode, 
         ScalingPolicyUpdateBehavior=ScalingPolicyUpdateBehavior, 
         ScheduledActionBufferTime=ScheduledActionBufferTime, **kwargs)
        (super(ScalingInstruction, self).__init__)(**processed_kwargs)


class ScalingPlan(troposphere.autoscalingplans.ScalingPlan, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationSource=REQUIRED, ScalingInstructions=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationSource=ApplicationSource, 
         ScalingInstructions=ScalingInstructions, **kwargs)
        (super(ScalingPlan, self).__init__)(**processed_kwargs)