# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/dms.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 14711 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.dms
from troposphere.dms import DynamoDbSettings as _DynamoDbSettings, ElasticsearchSettings as _ElasticsearchSettings, KinesisSettings as _KinesisSettings, MongoDbSettings as _MongoDbSettings, S3Settings as _S3Settings, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Certificate(troposphere.dms.Certificate, Mixin):

    def __init__(self, title, template=None, validation=True, CertificateIdentifier=NOTHING, CertificatePem=NOTHING, CertificateWallet=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CertificateIdentifier=CertificateIdentifier, 
         CertificatePem=CertificatePem, 
         CertificateWallet=CertificateWallet, **kwargs)
        (super(Certificate, self).__init__)(**processed_kwargs)


class DynamoDbSettings(troposphere.dms.DynamoDbSettings, Mixin):

    def __init__(self, title=None, ServiceAccessRoleArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ServiceAccessRoleArn=ServiceAccessRoleArn, **kwargs)
        (super(DynamoDbSettings, self).__init__)(**processed_kwargs)


class ElasticsearchSettings(troposphere.dms.ElasticsearchSettings, Mixin):

    def __init__(self, title=None, EndpointUri=NOTHING, ErrorRetryDuration=NOTHING, FullLoadErrorPercentage=NOTHING, ServiceAccessRoleArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EndpointUri=EndpointUri, 
         ErrorRetryDuration=ErrorRetryDuration, 
         FullLoadErrorPercentage=FullLoadErrorPercentage, 
         ServiceAccessRoleArn=ServiceAccessRoleArn, **kwargs)
        (super(ElasticsearchSettings, self).__init__)(**processed_kwargs)


class KinesisSettings(troposphere.dms.KinesisSettings, Mixin):

    def __init__(self, title=None, MessageFormat=NOTHING, ServiceAccessRoleArn=NOTHING, StreamArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MessageFormat=MessageFormat, 
         ServiceAccessRoleArn=ServiceAccessRoleArn, 
         StreamArn=StreamArn, **kwargs)
        (super(KinesisSettings, self).__init__)(**processed_kwargs)


class MongoDbSettings(troposphere.dms.MongoDbSettings, Mixin):

    def __init__(self, title=None, AuthMechanism=NOTHING, AuthSource=NOTHING, AuthType=NOTHING, DatabaseName=NOTHING, DocsToInvestigate=NOTHING, ExtractDocId=NOTHING, NestingLevel=NOTHING, Password=NOTHING, Port=NOTHING, ServerName=NOTHING, Username=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AuthMechanism=AuthMechanism, 
         AuthSource=AuthSource, 
         AuthType=AuthType, 
         DatabaseName=DatabaseName, 
         DocsToInvestigate=DocsToInvestigate, 
         ExtractDocId=ExtractDocId, 
         NestingLevel=NestingLevel, 
         Password=Password, 
         Port=Port, 
         ServerName=ServerName, 
         Username=Username, **kwargs)
        (super(MongoDbSettings, self).__init__)(**processed_kwargs)


class S3Settings(troposphere.dms.S3Settings, Mixin):

    def __init__(self, title=None, BucketFolder=NOTHING, BucketName=NOTHING, CompressionType=NOTHING, CsvDelimiter=NOTHING, CsvRowDelimiter=NOTHING, ExternalTableDefinition=NOTHING, ServiceAccessRoleArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BucketFolder=BucketFolder, 
         BucketName=BucketName, 
         CompressionType=CompressionType, 
         CsvDelimiter=CsvDelimiter, 
         CsvRowDelimiter=CsvRowDelimiter, 
         ExternalTableDefinition=ExternalTableDefinition, 
         ServiceAccessRoleArn=ServiceAccessRoleArn, **kwargs)
        (super(S3Settings, self).__init__)(**processed_kwargs)


class Endpoint(troposphere.dms.Endpoint, Mixin):

    def __init__(self, title, template=None, validation=True, EndpointType=REQUIRED, EngineName=REQUIRED, CertificateArn=NOTHING, DatabaseName=NOTHING, DynamoDbSettings=NOTHING, ElasticsearchSettings=NOTHING, EndpointIdentifier=NOTHING, ExtraConnectionAttributes=NOTHING, KinesisSettings=NOTHING, KmsKeyId=NOTHING, MongoDbSettings=NOTHING, Password=NOTHING, Port=NOTHING, S3Settings=NOTHING, ServerName=NOTHING, SslMode=NOTHING, Tags=NOTHING, Username=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         EndpointType=EndpointType, 
         EngineName=EngineName, 
         CertificateArn=CertificateArn, 
         DatabaseName=DatabaseName, 
         DynamoDbSettings=DynamoDbSettings, 
         ElasticsearchSettings=ElasticsearchSettings, 
         EndpointIdentifier=EndpointIdentifier, 
         ExtraConnectionAttributes=ExtraConnectionAttributes, 
         KinesisSettings=KinesisSettings, 
         KmsKeyId=KmsKeyId, 
         MongoDbSettings=MongoDbSettings, 
         Password=Password, 
         Port=Port, 
         S3Settings=S3Settings, 
         ServerName=ServerName, 
         SslMode=SslMode, 
         Tags=Tags, 
         Username=Username, **kwargs)
        (super(Endpoint, self).__init__)(**processed_kwargs)


class EventSubscription(troposphere.dms.EventSubscription, Mixin):

    def __init__(self, title, template=None, validation=True, SnsTopicArn=REQUIRED, Enabled=NOTHING, EventCategories=NOTHING, SourceIds=NOTHING, SourceType=NOTHING, SubscriptionName=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         SnsTopicArn=SnsTopicArn, 
         Enabled=Enabled, 
         EventCategories=EventCategories, 
         SourceIds=SourceIds, 
         SourceType=SourceType, 
         SubscriptionName=SubscriptionName, 
         Tags=Tags, **kwargs)
        (super(EventSubscription, self).__init__)(**processed_kwargs)


class ReplicationInstance(troposphere.dms.ReplicationInstance, Mixin):

    def __init__(self, title, template=None, validation=True, ReplicationInstanceClass=REQUIRED, AllocatedStorage=NOTHING, AllowMajorVersionUpgrade=NOTHING, AutoMinorVersionUpgrade=NOTHING, AvailabilityZone=NOTHING, EngineVersion=NOTHING, KmsKeyId=NOTHING, MultiAZ=NOTHING, PreferredMaintenanceWindow=NOTHING, PubliclyAccessible=NOTHING, ReplicationInstanceIdentifier=NOTHING, ReplicationSubnetGroupIdentifier=NOTHING, Tags=NOTHING, VpcSecurityGroupIds=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ReplicationInstanceClass=ReplicationInstanceClass, 
         AllocatedStorage=AllocatedStorage, 
         AllowMajorVersionUpgrade=AllowMajorVersionUpgrade, 
         AutoMinorVersionUpgrade=AutoMinorVersionUpgrade, 
         AvailabilityZone=AvailabilityZone, 
         EngineVersion=EngineVersion, 
         KmsKeyId=KmsKeyId, 
         MultiAZ=MultiAZ, 
         PreferredMaintenanceWindow=PreferredMaintenanceWindow, 
         PubliclyAccessible=PubliclyAccessible, 
         ReplicationInstanceIdentifier=ReplicationInstanceIdentifier, 
         ReplicationSubnetGroupIdentifier=ReplicationSubnetGroupIdentifier, 
         Tags=Tags, 
         VpcSecurityGroupIds=VpcSecurityGroupIds, **kwargs)
        (super(ReplicationInstance, self).__init__)(**processed_kwargs)


class ReplicationSubnetGroup(troposphere.dms.ReplicationSubnetGroup, Mixin):

    def __init__(self, title, template=None, validation=True, ReplicationSubnetGroupDescription=REQUIRED, SubnetIds=REQUIRED, ReplicationSubnetGroupIdentifier=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ReplicationSubnetGroupDescription=ReplicationSubnetGroupDescription, 
         SubnetIds=SubnetIds, 
         ReplicationSubnetGroupIdentifier=ReplicationSubnetGroupIdentifier, 
         Tags=Tags, **kwargs)
        (super(ReplicationSubnetGroup, self).__init__)(**processed_kwargs)


class ReplicationTask(troposphere.dms.ReplicationTask, Mixin):

    def __init__(self, title, template=None, validation=True, MigrationType=REQUIRED, ReplicationInstanceArn=REQUIRED, SourceEndpointArn=REQUIRED, TableMappings=REQUIRED, TargetEndpointArn=REQUIRED, CdcStartPosition=NOTHING, CdcStartTime=NOTHING, CdcStopPosition=NOTHING, ReplicationTaskIdentifier=NOTHING, ReplicationTaskSettings=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         MigrationType=MigrationType, 
         ReplicationInstanceArn=ReplicationInstanceArn, 
         SourceEndpointArn=SourceEndpointArn, 
         TableMappings=TableMappings, 
         TargetEndpointArn=TargetEndpointArn, 
         CdcStartPosition=CdcStartPosition, 
         CdcStartTime=CdcStartTime, 
         CdcStopPosition=CdcStopPosition, 
         ReplicationTaskIdentifier=ReplicationTaskIdentifier, 
         ReplicationTaskSettings=ReplicationTaskSettings, 
         Tags=Tags, **kwargs)
        (super(ReplicationTask, self).__init__)(**processed_kwargs)