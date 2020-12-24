# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/sns.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 3941 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.sns
from troposphere.sns import Subscription as _Subscription, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Subscription(troposphere.sns.Subscription, Mixin):

    def __init__(self, title=None, Endpoint=REQUIRED, Protocol=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Endpoint=Endpoint, 
         Protocol=Protocol, **kwargs)
        (super(Subscription, self).__init__)(**processed_kwargs)


class SubscriptionResource(troposphere.sns.SubscriptionResource, Mixin):

    def __init__(self, title, template=None, validation=True, Protocol=REQUIRED, TopicArn=REQUIRED, DeliveryPolicy=NOTHING, Endpoint=NOTHING, FilterPolicy=NOTHING, RawMessageDelivery=NOTHING, RedrivePolicy=NOTHING, Region=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Protocol=Protocol, 
         TopicArn=TopicArn, 
         DeliveryPolicy=DeliveryPolicy, 
         Endpoint=Endpoint, 
         FilterPolicy=FilterPolicy, 
         RawMessageDelivery=RawMessageDelivery, 
         RedrivePolicy=RedrivePolicy, 
         Region=Region, **kwargs)
        (super(SubscriptionResource, self).__init__)(**processed_kwargs)


class TopicPolicy(troposphere.sns.TopicPolicy, Mixin):

    def __init__(self, title, template=None, validation=True, PolicyDocument=REQUIRED, Topics=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PolicyDocument=PolicyDocument, 
         Topics=Topics, **kwargs)
        (super(TopicPolicy, self).__init__)(**processed_kwargs)


class Topic(troposphere.sns.Topic, Mixin):

    def __init__(self, title, template=None, validation=True, DisplayName=NOTHING, KmsMasterKeyId=NOTHING, Subscription=NOTHING, Tags=NOTHING, TopicName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DisplayName=DisplayName, 
         KmsMasterKeyId=KmsMasterKeyId, 
         Subscription=Subscription, 
         Tags=Tags, 
         TopicName=TopicName, **kwargs)
        (super(Topic, self).__init__)(**processed_kwargs)