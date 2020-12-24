# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/dynamodb.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 8579 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.dynamodb
from troposphere.dynamodb import AttributeDefinition as _AttributeDefinition, GlobalSecondaryIndex as _GlobalSecondaryIndex, KeySchema as _KeySchema, LocalSecondaryIndex as _LocalSecondaryIndex, PointInTimeRecoverySpecification as _PointInTimeRecoverySpecification, Projection as _Projection, ProvisionedThroughput as _ProvisionedThroughput, SSESpecification as _SSESpecification, StreamSpecification as _StreamSpecification, Tags as _Tags, TimeToLiveSpecification as _TimeToLiveSpecification
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class AttributeDefinition(troposphere.dynamodb.AttributeDefinition, Mixin):

    def __init__(self, title=None, AttributeName=REQUIRED, AttributeType=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AttributeName=AttributeName, 
         AttributeType=AttributeType, **kwargs)
        (super(AttributeDefinition, self).__init__)(**processed_kwargs)


class KeySchema(troposphere.dynamodb.KeySchema, Mixin):

    def __init__(self, title=None, AttributeName=REQUIRED, KeyType=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AttributeName=AttributeName, 
         KeyType=KeyType, **kwargs)
        (super(KeySchema, self).__init__)(**processed_kwargs)


class ProvisionedThroughput(troposphere.dynamodb.ProvisionedThroughput, Mixin):

    def __init__(self, title=None, ReadCapacityUnits=REQUIRED, WriteCapacityUnits=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ReadCapacityUnits=ReadCapacityUnits, 
         WriteCapacityUnits=WriteCapacityUnits, **kwargs)
        (super(ProvisionedThroughput, self).__init__)(**processed_kwargs)


class Projection(troposphere.dynamodb.Projection, Mixin):

    def __init__(self, title=None, NonKeyAttributes=NOTHING, ProjectionType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         NonKeyAttributes=NonKeyAttributes, 
         ProjectionType=ProjectionType, **kwargs)
        (super(Projection, self).__init__)(**processed_kwargs)


class SSESpecification(troposphere.dynamodb.SSESpecification, Mixin):

    def __init__(self, title=None, SSEEnabled=REQUIRED, KMSMasterKeyId=NOTHING, SSEType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SSEEnabled=SSEEnabled, 
         KMSMasterKeyId=KMSMasterKeyId, 
         SSEType=SSEType, **kwargs)
        (super(SSESpecification, self).__init__)(**processed_kwargs)


class GlobalSecondaryIndex(troposphere.dynamodb.GlobalSecondaryIndex, Mixin):

    def __init__(self, title=None, IndexName=REQUIRED, KeySchema=REQUIRED, Projection=REQUIRED, ProvisionedThroughput=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         IndexName=IndexName, 
         KeySchema=KeySchema, 
         Projection=Projection, 
         ProvisionedThroughput=ProvisionedThroughput, **kwargs)
        (super(GlobalSecondaryIndex, self).__init__)(**processed_kwargs)


class LocalSecondaryIndex(troposphere.dynamodb.LocalSecondaryIndex, Mixin):

    def __init__(self, title=None, IndexName=REQUIRED, KeySchema=REQUIRED, Projection=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         IndexName=IndexName, 
         KeySchema=KeySchema, 
         Projection=Projection, **kwargs)
        (super(LocalSecondaryIndex, self).__init__)(**processed_kwargs)


class PointInTimeRecoverySpecification(troposphere.dynamodb.PointInTimeRecoverySpecification, Mixin):

    def __init__(self, title=None, PointInTimeRecoveryEnabled=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PointInTimeRecoveryEnabled=PointInTimeRecoveryEnabled, **kwargs)
        (super(PointInTimeRecoverySpecification, self).__init__)(**processed_kwargs)


class StreamSpecification(troposphere.dynamodb.StreamSpecification, Mixin):

    def __init__(self, title=None, StreamViewType=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         StreamViewType=StreamViewType, **kwargs)
        (super(StreamSpecification, self).__init__)(**processed_kwargs)


class TimeToLiveSpecification(troposphere.dynamodb.TimeToLiveSpecification, Mixin):

    def __init__(self, title=None, AttributeName=REQUIRED, Enabled=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AttributeName=AttributeName, 
         Enabled=Enabled, **kwargs)
        (super(TimeToLiveSpecification, self).__init__)(**processed_kwargs)


class Table(troposphere.dynamodb.Table, Mixin):

    def __init__(self, title, template=None, validation=True, AttributeDefinitions=REQUIRED, KeySchema=REQUIRED, BillingMode=NOTHING, GlobalSecondaryIndexes=NOTHING, LocalSecondaryIndexes=NOTHING, PointInTimeRecoverySpecification=NOTHING, ProvisionedThroughput=NOTHING, SSESpecification=NOTHING, StreamSpecification=NOTHING, TableName=NOTHING, Tags=NOTHING, TimeToLiveSpecification=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AttributeDefinitions=AttributeDefinitions, 
         KeySchema=KeySchema, 
         BillingMode=BillingMode, 
         GlobalSecondaryIndexes=GlobalSecondaryIndexes, 
         LocalSecondaryIndexes=LocalSecondaryIndexes, 
         PointInTimeRecoverySpecification=PointInTimeRecoverySpecification, 
         ProvisionedThroughput=ProvisionedThroughput, 
         SSESpecification=SSESpecification, 
         StreamSpecification=StreamSpecification, 
         TableName=TableName, 
         Tags=Tags, 
         TimeToLiveSpecification=TimeToLiveSpecification, **kwargs)
        (super(Table, self).__init__)(**processed_kwargs)