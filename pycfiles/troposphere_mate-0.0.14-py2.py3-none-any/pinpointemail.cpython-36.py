# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/pinpointemail.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 10891 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.pinpointemail
from troposphere.pinpointemail import CloudWatchDestination as _CloudWatchDestination, DeliveryOptions as _DeliveryOptions, DimensionConfiguration as _DimensionConfiguration, EventDestination as _EventDestination, KinesisFirehoseDestination as _KinesisFirehoseDestination, MailFromAttributes as _MailFromAttributes, PinpointDestination as _PinpointDestination, ReputationOptions as _ReputationOptions, SendingOptions as _SendingOptions, SnsDestination as _SnsDestination, Tags as _Tags, TrackingOptions as _TrackingOptions
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class DeliveryOptions(troposphere.pinpointemail.DeliveryOptions, Mixin):

    def __init__(self, title=None, SendingPoolName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SendingPoolName=SendingPoolName, **kwargs)
        (super(DeliveryOptions, self).__init__)(**processed_kwargs)


class ReputationOptions(troposphere.pinpointemail.ReputationOptions, Mixin):

    def __init__(self, title=None, ReputationMetricsEnabled=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ReputationMetricsEnabled=ReputationMetricsEnabled, **kwargs)
        (super(ReputationOptions, self).__init__)(**processed_kwargs)


class SendingOptions(troposphere.pinpointemail.SendingOptions, Mixin):

    def __init__(self, title=None, SendingEnabled=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SendingEnabled=SendingEnabled, **kwargs)
        (super(SendingOptions, self).__init__)(**processed_kwargs)


class TrackingOptions(troposphere.pinpointemail.TrackingOptions, Mixin):

    def __init__(self, title=None, CustomRedirectDomain=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CustomRedirectDomain=CustomRedirectDomain, **kwargs)
        (super(TrackingOptions, self).__init__)(**processed_kwargs)


class ConfigurationSet(troposphere.pinpointemail.ConfigurationSet, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, DeliveryOptions=NOTHING, ReputationOptions=NOTHING, SendingOptions=NOTHING, Tags=NOTHING, TrackingOptions=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         DeliveryOptions=DeliveryOptions, 
         ReputationOptions=ReputationOptions, 
         SendingOptions=SendingOptions, 
         Tags=Tags, 
         TrackingOptions=TrackingOptions, **kwargs)
        (super(ConfigurationSet, self).__init__)(**processed_kwargs)


class DimensionConfiguration(troposphere.pinpointemail.DimensionConfiguration, Mixin):

    def __init__(self, title=None, DefaultDimensionValue=REQUIRED, DimensionName=REQUIRED, DimensionValueSource=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DefaultDimensionValue=DefaultDimensionValue, 
         DimensionName=DimensionName, 
         DimensionValueSource=DimensionValueSource, **kwargs)
        (super(DimensionConfiguration, self).__init__)(**processed_kwargs)


class CloudWatchDestination(troposphere.pinpointemail.CloudWatchDestination, Mixin):

    def __init__(self, title=None, DimensionConfigurations=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DimensionConfigurations=DimensionConfigurations, **kwargs)
        (super(CloudWatchDestination, self).__init__)(**processed_kwargs)


class KinesisFirehoseDestination(troposphere.pinpointemail.KinesisFirehoseDestination, Mixin):

    def __init__(self, title=None, DeliveryStreamArn=REQUIRED, IamRoleArn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeliveryStreamArn=DeliveryStreamArn, 
         IamRoleArn=IamRoleArn, **kwargs)
        (super(KinesisFirehoseDestination, self).__init__)(**processed_kwargs)


class PinpointDestination(troposphere.pinpointemail.PinpointDestination, Mixin):

    def __init__(self, title=None, ApplicationArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ApplicationArn=ApplicationArn, **kwargs)
        (super(PinpointDestination, self).__init__)(**processed_kwargs)


class SnsDestination(troposphere.pinpointemail.SnsDestination, Mixin):

    def __init__(self, title=None, TopicArn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TopicArn=TopicArn, **kwargs)
        (super(SnsDestination, self).__init__)(**processed_kwargs)


class EventDestination(troposphere.pinpointemail.EventDestination, Mixin):

    def __init__(self, title=None, MatchingEventTypes=REQUIRED, CloudWatchDestination=NOTHING, Enabled=NOTHING, KinesisFirehoseDestination=NOTHING, PinpointDestination=NOTHING, SnsDestination=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MatchingEventTypes=MatchingEventTypes, 
         CloudWatchDestination=CloudWatchDestination, 
         Enabled=Enabled, 
         KinesisFirehoseDestination=KinesisFirehoseDestination, 
         PinpointDestination=PinpointDestination, 
         SnsDestination=SnsDestination, **kwargs)
        (super(EventDestination, self).__init__)(**processed_kwargs)


class ConfigurationSetEventDestination(troposphere.pinpointemail.ConfigurationSetEventDestination, Mixin):

    def __init__(self, title, template=None, validation=True, ConfigurationSetName=REQUIRED, EventDestinationName=REQUIRED, EventDestination=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ConfigurationSetName=ConfigurationSetName, 
         EventDestinationName=EventDestinationName, 
         EventDestination=EventDestination, **kwargs)
        (super(ConfigurationSetEventDestination, self).__init__)(**processed_kwargs)


class DedicatedIpPool(troposphere.pinpointemail.DedicatedIpPool, Mixin):

    def __init__(self, title, template=None, validation=True, PoolName=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PoolName=PoolName, 
         Tags=Tags, **kwargs)
        (super(DedicatedIpPool, self).__init__)(**processed_kwargs)


class MailFromAttributes(troposphere.pinpointemail.MailFromAttributes, Mixin):

    def __init__(self, title=None, BehaviorOnMxFailure=NOTHING, MailFromDomain=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BehaviorOnMxFailure=BehaviorOnMxFailure, 
         MailFromDomain=MailFromDomain, **kwargs)
        (super(MailFromAttributes, self).__init__)(**processed_kwargs)


class Identity(troposphere.pinpointemail.Identity, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, DkimSigningEnabled=NOTHING, FeedbackForwardingEnabled=NOTHING, MailFromAttributes=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         DkimSigningEnabled=DkimSigningEnabled, 
         FeedbackForwardingEnabled=FeedbackForwardingEnabled, 
         MailFromAttributes=MailFromAttributes, 
         Tags=Tags, **kwargs)
        (super(Identity, self).__init__)(**processed_kwargs)