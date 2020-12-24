# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/cloudwatch.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 9515 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.cloudwatch
from troposphere.cloudwatch import Configuration as _Configuration, Metric as _Metric, MetricDataQuery as _MetricDataQuery, MetricDimension as _MetricDimension, MetricStat as _MetricStat, Range as _Range
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class MetricDimension(troposphere.cloudwatch.MetricDimension, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Value=Value, **kwargs)
        (super(MetricDimension, self).__init__)(**processed_kwargs)


class Metric(troposphere.cloudwatch.Metric, Mixin):

    def __init__(self, title=None, Dimensions=NOTHING, MetricName=NOTHING, Namespace=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Dimensions=Dimensions, 
         MetricName=MetricName, 
         Namespace=Namespace, **kwargs)
        (super(Metric, self).__init__)(**processed_kwargs)


class MetricStat(troposphere.cloudwatch.MetricStat, Mixin):

    def __init__(self, title=None, Metric=REQUIRED, Period=REQUIRED, Stat=REQUIRED, Unit=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Metric=Metric, 
         Period=Period, 
         Stat=Stat, 
         Unit=Unit, **kwargs)
        (super(MetricStat, self).__init__)(**processed_kwargs)


class MetricDataQuery(troposphere.cloudwatch.MetricDataQuery, Mixin):

    def __init__(self, title=None, Id=REQUIRED, Expression=NOTHING, Label=NOTHING, MetricStat=NOTHING, ReturnData=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Id=Id, 
         Expression=Expression, 
         Label=Label, 
         MetricStat=MetricStat, 
         ReturnData=ReturnData, **kwargs)
        (super(MetricDataQuery, self).__init__)(**processed_kwargs)


class Alarm(troposphere.cloudwatch.Alarm, Mixin):

    def __init__(self, title, template=None, validation=True, ComparisonOperator=REQUIRED, EvaluationPeriods=REQUIRED, ActionsEnabled=NOTHING, AlarmActions=NOTHING, AlarmDescription=NOTHING, AlarmName=NOTHING, DatapointsToAlarm=NOTHING, Dimensions=NOTHING, EvaluateLowSampleCountPercentile=NOTHING, ExtendedStatistic=NOTHING, InsufficientDataActions=NOTHING, MetricName=NOTHING, Metrics=NOTHING, Namespace=NOTHING, OKActions=NOTHING, Period=NOTHING, Statistic=NOTHING, Threshold=NOTHING, ThresholdMetricId=NOTHING, TreatMissingData=NOTHING, Unit=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ComparisonOperator=ComparisonOperator, 
         EvaluationPeriods=EvaluationPeriods, 
         ActionsEnabled=ActionsEnabled, 
         AlarmActions=AlarmActions, 
         AlarmDescription=AlarmDescription, 
         AlarmName=AlarmName, 
         DatapointsToAlarm=DatapointsToAlarm, 
         Dimensions=Dimensions, 
         EvaluateLowSampleCountPercentile=EvaluateLowSampleCountPercentile, 
         ExtendedStatistic=ExtendedStatistic, 
         InsufficientDataActions=InsufficientDataActions, 
         MetricName=MetricName, 
         Metrics=Metrics, 
         Namespace=Namespace, 
         OKActions=OKActions, 
         Period=Period, 
         Statistic=Statistic, 
         Threshold=Threshold, 
         ThresholdMetricId=ThresholdMetricId, 
         TreatMissingData=TreatMissingData, 
         Unit=Unit, **kwargs)
        (super(Alarm, self).__init__)(**processed_kwargs)


class Dashboard(troposphere.cloudwatch.Dashboard, Mixin):

    def __init__(self, title, template=None, validation=True, DashboardBody=REQUIRED, DashboardName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DashboardBody=DashboardBody, 
         DashboardName=DashboardName, **kwargs)
        (super(Dashboard, self).__init__)(**processed_kwargs)


class Range(troposphere.cloudwatch.Range, Mixin):

    def __init__(self, title=None, EndTime=REQUIRED, StartTime=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EndTime=EndTime, 
         StartTime=StartTime, **kwargs)
        (super(Range, self).__init__)(**processed_kwargs)


class Configuration(troposphere.cloudwatch.Configuration, Mixin):

    def __init__(self, title=None, ExcludedTimeRanges=NOTHING, MetricTimeZone=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ExcludedTimeRanges=ExcludedTimeRanges, 
         MetricTimeZone=MetricTimeZone, **kwargs)
        (super(Configuration, self).__init__)(**processed_kwargs)


class AnomalyDetector(troposphere.cloudwatch.AnomalyDetector, Mixin):

    def __init__(self, title, template=None, validation=True, MetricName=REQUIRED, Namespace=REQUIRED, Stat=REQUIRED, Configuration=NOTHING, Dimensions=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         MetricName=MetricName, 
         Namespace=Namespace, 
         Stat=Stat, 
         Configuration=Configuration, 
         Dimensions=Dimensions, **kwargs)
        (super(AnomalyDetector, self).__init__)(**processed_kwargs)


class InsightRule(troposphere.cloudwatch.InsightRule, Mixin):

    def __init__(self, title, template=None, validation=True, RuleBody=REQUIRED, RuleName=REQUIRED, RuleState=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         RuleBody=RuleBody, 
         RuleName=RuleName, 
         RuleState=RuleState, **kwargs)
        (super(InsightRule, self).__init__)(**processed_kwargs)