# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/sqs.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 3501 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.sqs
from troposphere.sqs import RedrivePolicy as _RedrivePolicy, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class RedrivePolicy(troposphere.sqs.RedrivePolicy, Mixin):

    def __init__(self, title=None, deadLetterTargetArn=NOTHING, maxReceiveCount=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         deadLetterTargetArn=deadLetterTargetArn, 
         maxReceiveCount=maxReceiveCount, **kwargs)
        (super(RedrivePolicy, self).__init__)(**processed_kwargs)


class Queue(troposphere.sqs.Queue, Mixin):

    def __init__(self, title, template=None, validation=True, ContentBasedDeduplication=NOTHING, DelaySeconds=NOTHING, FifoQueue=NOTHING, KmsMasterKeyId=NOTHING, KmsDataKeyReusePeriodSeconds=NOTHING, MaximumMessageSize=NOTHING, MessageRetentionPeriod=NOTHING, QueueName=NOTHING, ReceiveMessageWaitTimeSeconds=NOTHING, RedrivePolicy=NOTHING, Tags=NOTHING, VisibilityTimeout=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ContentBasedDeduplication=ContentBasedDeduplication, 
         DelaySeconds=DelaySeconds, 
         FifoQueue=FifoQueue, 
         KmsMasterKeyId=KmsMasterKeyId, 
         KmsDataKeyReusePeriodSeconds=KmsDataKeyReusePeriodSeconds, 
         MaximumMessageSize=MaximumMessageSize, 
         MessageRetentionPeriod=MessageRetentionPeriod, 
         QueueName=QueueName, 
         ReceiveMessageWaitTimeSeconds=ReceiveMessageWaitTimeSeconds, 
         RedrivePolicy=RedrivePolicy, 
         Tags=Tags, 
         VisibilityTimeout=VisibilityTimeout, **kwargs)
        (super(Queue, self).__init__)(**processed_kwargs)


class QueuePolicy(troposphere.sqs.QueuePolicy, Mixin):

    def __init__(self, title, template=None, validation=True, Queues=REQUIRED, PolicyDocument=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Queues=Queues, 
         PolicyDocument=PolicyDocument, **kwargs)
        (super(QueuePolicy, self).__init__)(**processed_kwargs)