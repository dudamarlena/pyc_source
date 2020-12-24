# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/iot.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 16136 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.iot
from troposphere.iot import Action as _Action, CloudwatchAlarmAction as _CloudwatchAlarmAction, CloudwatchMetricAction as _CloudwatchMetricAction, DynamoDBAction as _DynamoDBAction, DynamoDBv2Action as _DynamoDBv2Action, ElasticsearchAction as _ElasticsearchAction, FirehoseAction as _FirehoseAction, KinesisAction as _KinesisAction, LambdaAction as _LambdaAction, PutItemInput as _PutItemInput, RepublishAction as _RepublishAction, S3Action as _S3Action, SnsAction as _SnsAction, SqsAction as _SqsAction, TopicRulePayload as _TopicRulePayload
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class CloudwatchAlarmAction(troposphere.iot.CloudwatchAlarmAction, Mixin):

    def __init__(self, title=None, AlarmName=REQUIRED, RoleArn=REQUIRED, StateReason=REQUIRED, StateValue=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AlarmName=AlarmName, 
         RoleArn=RoleArn, 
         StateReason=StateReason, 
         StateValue=StateValue, **kwargs)
        (super(CloudwatchAlarmAction, self).__init__)(**processed_kwargs)


class CloudwatchMetricAction(troposphere.iot.CloudwatchMetricAction, Mixin):

    def __init__(self, title=None, MetricName=REQUIRED, MetricNamespace=REQUIRED, MetricUnit=REQUIRED, MetricValue=REQUIRED, RoleArn=REQUIRED, MetricTimestamp=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MetricName=MetricName, 
         MetricNamespace=MetricNamespace, 
         MetricUnit=MetricUnit, 
         MetricValue=MetricValue, 
         RoleArn=RoleArn, 
         MetricTimestamp=MetricTimestamp, **kwargs)
        (super(CloudwatchMetricAction, self).__init__)(**processed_kwargs)


class DynamoDBAction(troposphere.iot.DynamoDBAction, Mixin):

    def __init__(self, title=None, HashKeyField=REQUIRED, HashKeyValue=REQUIRED, RoleArn=REQUIRED, TableName=REQUIRED, HashKeyType=NOTHING, PayloadField=NOTHING, RangeKeyField=NOTHING, RangeKeyType=NOTHING, RangeKeyValue=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HashKeyField=HashKeyField, 
         HashKeyValue=HashKeyValue, 
         RoleArn=RoleArn, 
         TableName=TableName, 
         HashKeyType=HashKeyType, 
         PayloadField=PayloadField, 
         RangeKeyField=RangeKeyField, 
         RangeKeyType=RangeKeyType, 
         RangeKeyValue=RangeKeyValue, **kwargs)
        (super(DynamoDBAction, self).__init__)(**processed_kwargs)


class PutItemInput(troposphere.iot.PutItemInput, Mixin):

    def __init__(self, title=None, TableName=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TableName=TableName, **kwargs)
        (super(PutItemInput, self).__init__)(**processed_kwargs)


class DynamoDBv2Action(troposphere.iot.DynamoDBv2Action, Mixin):

    def __init__(self, title=None, PutItem=NOTHING, RoleArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PutItem=PutItem, 
         RoleArn=RoleArn, **kwargs)
        (super(DynamoDBv2Action, self).__init__)(**processed_kwargs)


class ElasticsearchAction(troposphere.iot.ElasticsearchAction, Mixin):

    def __init__(self, title=None, Endpoint=REQUIRED, Id=REQUIRED, Index=REQUIRED, RoleArn=REQUIRED, Type=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Endpoint=Endpoint, 
         Id=Id, 
         Index=Index, 
         RoleArn=RoleArn, 
         Type=Type, **kwargs)
        (super(ElasticsearchAction, self).__init__)(**processed_kwargs)


class FirehoseAction(troposphere.iot.FirehoseAction, Mixin):

    def __init__(self, title=None, DeliveryStreamName=REQUIRED, RoleArn=REQUIRED, Separator=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeliveryStreamName=DeliveryStreamName, 
         RoleArn=RoleArn, 
         Separator=Separator, **kwargs)
        (super(FirehoseAction, self).__init__)(**processed_kwargs)


class KinesisAction(troposphere.iot.KinesisAction, Mixin):

    def __init__(self, title=None, RoleArn=REQUIRED, StreamName=REQUIRED, PartitionKey=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RoleArn=RoleArn, 
         StreamName=StreamName, 
         PartitionKey=PartitionKey, **kwargs)
        (super(KinesisAction, self).__init__)(**processed_kwargs)


class LambdaAction(troposphere.iot.LambdaAction, Mixin):

    def __init__(self, title=None, FunctionArn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FunctionArn=FunctionArn, **kwargs)
        (super(LambdaAction, self).__init__)(**processed_kwargs)


class RepublishAction(troposphere.iot.RepublishAction, Mixin):

    def __init__(self, title=None, RoleArn=REQUIRED, Topic=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RoleArn=RoleArn, 
         Topic=Topic, **kwargs)
        (super(RepublishAction, self).__init__)(**processed_kwargs)


class S3Action(troposphere.iot.S3Action, Mixin):

    def __init__(self, title=None, BucketName=REQUIRED, Key=REQUIRED, RoleArn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BucketName=BucketName, 
         Key=Key, 
         RoleArn=RoleArn, **kwargs)
        (super(S3Action, self).__init__)(**processed_kwargs)


class SnsAction(troposphere.iot.SnsAction, Mixin):

    def __init__(self, title=None, RoleArn=REQUIRED, TargetArn=REQUIRED, MessageFormat=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RoleArn=RoleArn, 
         TargetArn=TargetArn, 
         MessageFormat=MessageFormat, **kwargs)
        (super(SnsAction, self).__init__)(**processed_kwargs)


class SqsAction(troposphere.iot.SqsAction, Mixin):

    def __init__(self, title=None, QueueUrl=REQUIRED, RoleArn=REQUIRED, UseBase64=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         QueueUrl=QueueUrl, 
         RoleArn=RoleArn, 
         UseBase64=UseBase64, **kwargs)
        (super(SqsAction, self).__init__)(**processed_kwargs)


class Action(troposphere.iot.Action, Mixin):

    def __init__(self, title=None, CloudwatchAlarm=NOTHING, CloudwatchMetric=NOTHING, DynamoDB=NOTHING, DynamoDBv2=NOTHING, Elasticsearch=NOTHING, Firehose=NOTHING, Kinesis=NOTHING, Lambda=NOTHING, Republish=NOTHING, S3=NOTHING, Sns=NOTHING, Sqs=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CloudwatchAlarm=CloudwatchAlarm, 
         CloudwatchMetric=CloudwatchMetric, 
         DynamoDB=DynamoDB, 
         DynamoDBv2=DynamoDBv2, 
         Elasticsearch=Elasticsearch, 
         Firehose=Firehose, 
         Kinesis=Kinesis, 
         Lambda=Lambda, 
         Republish=Republish, 
         S3=S3, 
         Sns=Sns, 
         Sqs=Sqs, **kwargs)
        (super(Action, self).__init__)(**processed_kwargs)


class TopicRulePayload(troposphere.iot.TopicRulePayload, Mixin):

    def __init__(self, title=None, Actions=REQUIRED, RuleDisabled=REQUIRED, Sql=REQUIRED, AwsIotSqlVersion=NOTHING, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Actions=Actions, 
         RuleDisabled=RuleDisabled, 
         Sql=Sql, 
         AwsIotSqlVersion=AwsIotSqlVersion, 
         Description=Description, **kwargs)
        (super(TopicRulePayload, self).__init__)(**processed_kwargs)


class TopicRule(troposphere.iot.TopicRule, Mixin):

    def __init__(self, title, template=None, validation=True, TopicRulePayload=REQUIRED, RuleName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         TopicRulePayload=TopicRulePayload, 
         RuleName=RuleName, **kwargs)
        (super(TopicRule, self).__init__)(**processed_kwargs)


class ThingPrincipalAttachment(troposphere.iot.ThingPrincipalAttachment, Mixin):

    def __init__(self, title, template=None, validation=True, Principal=REQUIRED, ThingName=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Principal=Principal, 
         ThingName=ThingName, **kwargs)
        (super(ThingPrincipalAttachment, self).__init__)(**processed_kwargs)


class Thing(troposphere.iot.Thing, Mixin):

    def __init__(self, title, template=None, validation=True, AttributePayload=NOTHING, ThingName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AttributePayload=AttributePayload, 
         ThingName=ThingName, **kwargs)
        (super(Thing, self).__init__)(**processed_kwargs)


class PolicyPrincipalAttachment(troposphere.iot.PolicyPrincipalAttachment, Mixin):

    def __init__(self, title, template=None, validation=True, PolicyName=REQUIRED, Principal=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PolicyName=PolicyName, 
         Principal=Principal, **kwargs)
        (super(PolicyPrincipalAttachment, self).__init__)(**processed_kwargs)


class Policy(troposphere.iot.Policy, Mixin):

    def __init__(self, title, template=None, validation=True, PolicyDocument=REQUIRED, PolicyName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PolicyDocument=PolicyDocument, 
         PolicyName=PolicyName, **kwargs)
        (super(Policy, self).__init__)(**processed_kwargs)


class Certificate(troposphere.iot.Certificate, Mixin):

    def __init__(self, title, template=None, validation=True, CertificateSigningRequest=REQUIRED, Status=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CertificateSigningRequest=CertificateSigningRequest, 
         Status=Status, **kwargs)
        (super(Certificate, self).__init__)(**processed_kwargs)