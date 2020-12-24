# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/logs.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 5372 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.logs
from troposphere.logs import MetricTransformation as _MetricTransformation
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Destination(troposphere.logs.Destination, Mixin):

    def __init__(self, title, template=None, validation=True, DestinationName=REQUIRED, DestinationPolicy=REQUIRED, RoleArn=REQUIRED, TargetArn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DestinationName=DestinationName, 
         DestinationPolicy=DestinationPolicy, 
         RoleArn=RoleArn, 
         TargetArn=TargetArn, **kwargs)
        (super(Destination, self).__init__)(**processed_kwargs)


class LogGroup(troposphere.logs.LogGroup, Mixin):

    def __init__(self, title, template=None, validation=True, LogGroupName=NOTHING, RetentionInDays=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         LogGroupName=LogGroupName, 
         RetentionInDays=RetentionInDays, **kwargs)
        (super(LogGroup, self).__init__)(**processed_kwargs)


class LogStream(troposphere.logs.LogStream, Mixin):

    def __init__(self, title, template=None, validation=True, LogGroupName=REQUIRED, LogStreamName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         LogGroupName=LogGroupName, 
         LogStreamName=LogStreamName, **kwargs)
        (super(LogStream, self).__init__)(**processed_kwargs)


class MetricTransformation(troposphere.logs.MetricTransformation, Mixin):

    def __init__(self, title=None, MetricName=REQUIRED, MetricNamespace=REQUIRED, MetricValue=REQUIRED, DefaultValue=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MetricName=MetricName, 
         MetricNamespace=MetricNamespace, 
         MetricValue=MetricValue, 
         DefaultValue=DefaultValue, **kwargs)
        (super(MetricTransformation, self).__init__)(**processed_kwargs)


class MetricFilter(troposphere.logs.MetricFilter, Mixin):

    def __init__(self, title, template=None, validation=True, FilterPattern=REQUIRED, LogGroupName=REQUIRED, MetricTransformations=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         FilterPattern=FilterPattern, 
         LogGroupName=LogGroupName, 
         MetricTransformations=MetricTransformations, **kwargs)
        (super(MetricFilter, self).__init__)(**processed_kwargs)


class SubscriptionFilter(troposphere.logs.SubscriptionFilter, Mixin):

    def __init__(self, title, template=None, validation=True, DestinationArn=REQUIRED, FilterPattern=REQUIRED, LogGroupName=REQUIRED, RoleArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DestinationArn=DestinationArn, 
         FilterPattern=FilterPattern, 
         LogGroupName=LogGroupName, 
         RoleArn=RoleArn, **kwargs)
        (super(SubscriptionFilter, self).__init__)(**processed_kwargs)