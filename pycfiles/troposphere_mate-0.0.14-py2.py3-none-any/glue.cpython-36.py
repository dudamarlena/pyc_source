# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/glue.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 42481 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.glue
from troposphere.glue import Action as _Action, CatalogTarget as _CatalogTarget, CloudWatchEncryption as _CloudWatchEncryption, Column as _Column, Condition as _Condition, ConnectionInput as _ConnectionInput, ConnectionPasswordEncryption as _ConnectionPasswordEncryption, ConnectionsList as _ConnectionsList, CsvClassifier as _CsvClassifier, DataCatalogEncryptionSettingsProperty as _DataCatalogEncryptionSettingsProperty, DatabaseInput as _DatabaseInput, DynamoDBTarget as _DynamoDBTarget, EncryptionAtRest as _EncryptionAtRest, EncryptionConfiguration as _EncryptionConfiguration, ExecutionProperty as _ExecutionProperty, FindMatchesParameters as _FindMatchesParameters, GlueTables as _GlueTables, GrokClassifier as _GrokClassifier, InputRecordTables as _InputRecordTables, JdbcTarget as _JdbcTarget, JobBookmarksEncryption as _JobBookmarksEncryption, JobCommand as _JobCommand, JsonClassifier as _JsonClassifier, NotificationProperty as _NotificationProperty, Order as _Order, PartitionInput as _PartitionInput, PhysicalConnectionRequirements as _PhysicalConnectionRequirements, Predicate as _Predicate, S3Encryptions as _S3Encryptions, S3Target as _S3Target, Schedule as _Schedule, SchemaChangePolicy as _SchemaChangePolicy, SerdeInfo as _SerdeInfo, SkewedInfo as _SkewedInfo, StorageDescriptor as _StorageDescriptor, TableInput as _TableInput, Targets as _Targets, TransformParameters as _TransformParameters, XMLClassifier as _XMLClassifier
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class CsvClassifier(troposphere.glue.CsvClassifier, Mixin):

    def __init__(self, title=None, AllowSingleColumn=NOTHING, ContainsHeader=NOTHING, Delimiter=NOTHING, DisableValueTrimming=NOTHING, Header=NOTHING, Name=NOTHING, QuoteSymbol=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AllowSingleColumn=AllowSingleColumn, 
         ContainsHeader=ContainsHeader, 
         Delimiter=Delimiter, 
         DisableValueTrimming=DisableValueTrimming, 
         Header=Header, 
         Name=Name, 
         QuoteSymbol=QuoteSymbol, **kwargs)
        (super(CsvClassifier, self).__init__)(**processed_kwargs)


class GrokClassifier(troposphere.glue.GrokClassifier, Mixin):

    def __init__(self, title=None, Classification=REQUIRED, GrokPattern=REQUIRED, CustomPatterns=NOTHING, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Classification=Classification, 
         GrokPattern=GrokPattern, 
         CustomPatterns=CustomPatterns, 
         Name=Name, **kwargs)
        (super(GrokClassifier, self).__init__)(**processed_kwargs)


class JsonClassifier(troposphere.glue.JsonClassifier, Mixin):

    def __init__(self, title=None, JsonPath=REQUIRED, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         JsonPath=JsonPath, 
         Name=Name, **kwargs)
        (super(JsonClassifier, self).__init__)(**processed_kwargs)


class XMLClassifier(troposphere.glue.XMLClassifier, Mixin):

    def __init__(self, title=None, Classification=REQUIRED, RowTag=REQUIRED, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Classification=Classification, 
         RowTag=RowTag, 
         Name=Name, **kwargs)
        (super(XMLClassifier, self).__init__)(**processed_kwargs)


class Classifier(troposphere.glue.Classifier, Mixin):

    def __init__(self, title, template=None, validation=True, CsvClassifier=NOTHING, GrokClassifier=NOTHING, JsonClassifier=NOTHING, XMLClassifier=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CsvClassifier=CsvClassifier, 
         GrokClassifier=GrokClassifier, 
         JsonClassifier=JsonClassifier, 
         XMLClassifier=XMLClassifier, **kwargs)
        (super(Classifier, self).__init__)(**processed_kwargs)


class PhysicalConnectionRequirements(troposphere.glue.PhysicalConnectionRequirements, Mixin):

    def __init__(self, title=None, AvailabilityZone=NOTHING, SecurityGroupIdList=NOTHING, SubnetId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AvailabilityZone=AvailabilityZone, 
         SecurityGroupIdList=SecurityGroupIdList, 
         SubnetId=SubnetId, **kwargs)
        (super(PhysicalConnectionRequirements, self).__init__)(**processed_kwargs)


class ConnectionInput(troposphere.glue.ConnectionInput, Mixin):

    def __init__(self, title=None, ConnectionProperties=REQUIRED, ConnectionType=REQUIRED, Description=NOTHING, MatchCriteria=NOTHING, Name=NOTHING, PhysicalConnectionRequirements=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ConnectionProperties=ConnectionProperties, 
         ConnectionType=ConnectionType, 
         Description=Description, 
         MatchCriteria=MatchCriteria, 
         Name=Name, 
         PhysicalConnectionRequirements=PhysicalConnectionRequirements, **kwargs)
        (super(ConnectionInput, self).__init__)(**processed_kwargs)


class Connection(troposphere.glue.Connection, Mixin):

    def __init__(self, title, template=None, validation=True, CatalogId=REQUIRED, ConnectionInput=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CatalogId=CatalogId, 
         ConnectionInput=ConnectionInput, **kwargs)
        (super(Connection, self).__init__)(**processed_kwargs)


class Schedule(troposphere.glue.Schedule, Mixin):

    def __init__(self, title=None, ScheduleExpression=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ScheduleExpression=ScheduleExpression, **kwargs)
        (super(Schedule, self).__init__)(**processed_kwargs)


class SchemaChangePolicy(troposphere.glue.SchemaChangePolicy, Mixin):

    def __init__(self, title=None, DeleteBehavior=NOTHING, UpdateBehavior=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeleteBehavior=DeleteBehavior, 
         UpdateBehavior=UpdateBehavior, **kwargs)
        (super(SchemaChangePolicy, self).__init__)(**processed_kwargs)


class CatalogTarget(troposphere.glue.CatalogTarget, Mixin):

    def __init__(self, title=None, DatabaseName=NOTHING, Tables=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DatabaseName=DatabaseName, 
         Tables=Tables, **kwargs)
        (super(CatalogTarget, self).__init__)(**processed_kwargs)


class DynamoDBTarget(troposphere.glue.DynamoDBTarget, Mixin):

    def __init__(self, title=None, Path=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Path=Path, **kwargs)
        (super(DynamoDBTarget, self).__init__)(**processed_kwargs)


class JdbcTarget(troposphere.glue.JdbcTarget, Mixin):

    def __init__(self, title=None, ConnectionName=NOTHING, Exclusions=NOTHING, Path=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ConnectionName=ConnectionName, 
         Exclusions=Exclusions, 
         Path=Path, **kwargs)
        (super(JdbcTarget, self).__init__)(**processed_kwargs)


class S3Target(troposphere.glue.S3Target, Mixin):

    def __init__(self, title=None, Exclusions=NOTHING, Path=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Exclusions=Exclusions, 
         Path=Path, **kwargs)
        (super(S3Target, self).__init__)(**processed_kwargs)


class Targets(troposphere.glue.Targets, Mixin):

    def __init__(self, title=None, CatalogTargets=NOTHING, DynamoDBTargets=NOTHING, JdbcTargets=NOTHING, S3Targets=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CatalogTargets=CatalogTargets, 
         DynamoDBTargets=DynamoDBTargets, 
         JdbcTargets=JdbcTargets, 
         S3Targets=S3Targets, **kwargs)
        (super(Targets, self).__init__)(**processed_kwargs)


class Crawler(troposphere.glue.Crawler, Mixin):

    def __init__(self, title, template=None, validation=True, DatabaseName=REQUIRED, Role=REQUIRED, Targets=REQUIRED, Classifiers=NOTHING, Configuration=NOTHING, CrawlerSecurityConfiguration=NOTHING, Description=NOTHING, Name=NOTHING, Schedule=NOTHING, SchemaChangePolicy=NOTHING, TablePrefix=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DatabaseName=DatabaseName, 
         Role=Role, 
         Targets=Targets, 
         Classifiers=Classifiers, 
         Configuration=Configuration, 
         CrawlerSecurityConfiguration=CrawlerSecurityConfiguration, 
         Description=Description, 
         Name=Name, 
         Schedule=Schedule, 
         SchemaChangePolicy=SchemaChangePolicy, 
         TablePrefix=TablePrefix, 
         Tags=Tags, **kwargs)
        (super(Crawler, self).__init__)(**processed_kwargs)


class ConnectionPasswordEncryption(troposphere.glue.ConnectionPasswordEncryption, Mixin):

    def __init__(self, title=None, KmsKeyId=NOTHING, ReturnConnectionPasswordEncrypted=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         KmsKeyId=KmsKeyId, 
         ReturnConnectionPasswordEncrypted=ReturnConnectionPasswordEncrypted, **kwargs)
        (super(ConnectionPasswordEncryption, self).__init__)(**processed_kwargs)


class EncryptionAtRest(troposphere.glue.EncryptionAtRest, Mixin):

    def __init__(self, title=None, CatalogEncryptionMode=NOTHING, SseAwsKmsKeyId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CatalogEncryptionMode=CatalogEncryptionMode, 
         SseAwsKmsKeyId=SseAwsKmsKeyId, **kwargs)
        (super(EncryptionAtRest, self).__init__)(**processed_kwargs)


class DataCatalogEncryptionSettingsProperty(troposphere.glue.DataCatalogEncryptionSettingsProperty, Mixin):

    def __init__(self, title=None, ConnectionPasswordEncryption=NOTHING, EncryptionAtRest=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ConnectionPasswordEncryption=ConnectionPasswordEncryption, 
         EncryptionAtRest=EncryptionAtRest, **kwargs)
        (super(DataCatalogEncryptionSettingsProperty, self).__init__)(**processed_kwargs)


class DataCatalogEncryptionSettings(troposphere.glue.DataCatalogEncryptionSettings, Mixin):

    def __init__(self, title, template=None, validation=True, CatalogId=REQUIRED, DataCatalogEncryptionSettings=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CatalogId=CatalogId, 
         DataCatalogEncryptionSettings=DataCatalogEncryptionSettings, **kwargs)
        (super(DataCatalogEncryptionSettings, self).__init__)(**processed_kwargs)


class DatabaseInput(troposphere.glue.DatabaseInput, Mixin):

    def __init__(self, title=None, Description=NOTHING, LocationUri=NOTHING, Name=NOTHING, Parameters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Description=Description, 
         LocationUri=LocationUri, 
         Name=Name, 
         Parameters=Parameters, **kwargs)
        (super(DatabaseInput, self).__init__)(**processed_kwargs)


class Database(troposphere.glue.Database, Mixin):

    def __init__(self, title, template=None, validation=True, CatalogId=REQUIRED, DatabaseInput=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CatalogId=CatalogId, 
         DatabaseInput=DatabaseInput, **kwargs)
        (super(Database, self).__init__)(**processed_kwargs)


class DevEndpoint(troposphere.glue.DevEndpoint, Mixin):

    def __init__(self, title, template=None, validation=True, RoleArn=REQUIRED, Arguments=NOTHING, EndpointName=NOTHING, ExtraJarsS3Path=NOTHING, ExtraPythonLibsS3Path=NOTHING, GlueVersion=NOTHING, NumberOfNodes=NOTHING, NumberOfWorkers=NOTHING, PublicKey=NOTHING, SecurityConfiguration=NOTHING, SecurityGroupIds=NOTHING, SubnetId=NOTHING, Tags=NOTHING, WorkerType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         RoleArn=RoleArn, 
         Arguments=Arguments, 
         EndpointName=EndpointName, 
         ExtraJarsS3Path=ExtraJarsS3Path, 
         ExtraPythonLibsS3Path=ExtraPythonLibsS3Path, 
         GlueVersion=GlueVersion, 
         NumberOfNodes=NumberOfNodes, 
         NumberOfWorkers=NumberOfWorkers, 
         PublicKey=PublicKey, 
         SecurityConfiguration=SecurityConfiguration, 
         SecurityGroupIds=SecurityGroupIds, 
         SubnetId=SubnetId, 
         Tags=Tags, 
         WorkerType=WorkerType, **kwargs)
        (super(DevEndpoint, self).__init__)(**processed_kwargs)


class ConnectionsList(troposphere.glue.ConnectionsList, Mixin):

    def __init__(self, title=None, Connections=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Connections=Connections, **kwargs)
        (super(ConnectionsList, self).__init__)(**processed_kwargs)


class ExecutionProperty(troposphere.glue.ExecutionProperty, Mixin):

    def __init__(self, title=None, MaxConcurrentRuns=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MaxConcurrentRuns=MaxConcurrentRuns, **kwargs)
        (super(ExecutionProperty, self).__init__)(**processed_kwargs)


class JobCommand(troposphere.glue.JobCommand, Mixin):

    def __init__(self, title=None, Name=NOTHING, PythonVersion=NOTHING, ScriptLocation=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         PythonVersion=PythonVersion, 
         ScriptLocation=ScriptLocation, **kwargs)
        (super(JobCommand, self).__init__)(**processed_kwargs)


class NotificationProperty(troposphere.glue.NotificationProperty, Mixin):

    def __init__(self, title=None, NotifyDelayAfter=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         NotifyDelayAfter=NotifyDelayAfter, **kwargs)
        (super(NotificationProperty, self).__init__)(**processed_kwargs)


class Job(troposphere.glue.Job, Mixin):

    def __init__(self, title, template=None, validation=True, Command=REQUIRED, Role=REQUIRED, AllocatedCapacity=NOTHING, Connections=NOTHING, DefaultArguments=NOTHING, Description=NOTHING, ExecutionProperty=NOTHING, GlueVersion=NOTHING, LogUri=NOTHING, MaxCapacity=NOTHING, MaxRetries=NOTHING, Name=NOTHING, NotificationProperty=NOTHING, NumberOfWorkers=NOTHING, SecurityConfiguration=NOTHING, Tags=NOTHING, Timeout=NOTHING, WorkerType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Command=Command, 
         Role=Role, 
         AllocatedCapacity=AllocatedCapacity, 
         Connections=Connections, 
         DefaultArguments=DefaultArguments, 
         Description=Description, 
         ExecutionProperty=ExecutionProperty, 
         GlueVersion=GlueVersion, 
         LogUri=LogUri, 
         MaxCapacity=MaxCapacity, 
         MaxRetries=MaxRetries, 
         Name=Name, 
         NotificationProperty=NotificationProperty, 
         NumberOfWorkers=NumberOfWorkers, 
         SecurityConfiguration=SecurityConfiguration, 
         Tags=Tags, 
         Timeout=Timeout, 
         WorkerType=WorkerType, **kwargs)
        (super(Job, self).__init__)(**processed_kwargs)


class GlueTables(troposphere.glue.GlueTables, Mixin):

    def __init__(self, title=None, DatabaseName=REQUIRED, TableName=REQUIRED, CatalogId=NOTHING, ConnectionName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DatabaseName=DatabaseName, 
         TableName=TableName, 
         CatalogId=CatalogId, 
         ConnectionName=ConnectionName, **kwargs)
        (super(GlueTables, self).__init__)(**processed_kwargs)


class InputRecordTables(troposphere.glue.InputRecordTables, Mixin):

    def __init__(self, title=None, GlueTables=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         GlueTables=GlueTables, **kwargs)
        (super(InputRecordTables, self).__init__)(**processed_kwargs)


class FindMatchesParameters(troposphere.glue.FindMatchesParameters, Mixin):

    def __init__(self, title=None, PrimaryKeyColumnName=REQUIRED, AccuracyCostTradeoff=NOTHING, EnforceProvidedLabels=NOTHING, PrecisionRecallTradeoff=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PrimaryKeyColumnName=PrimaryKeyColumnName, 
         AccuracyCostTradeoff=AccuracyCostTradeoff, 
         EnforceProvidedLabels=EnforceProvidedLabels, 
         PrecisionRecallTradeoff=PrecisionRecallTradeoff, **kwargs)
        (super(FindMatchesParameters, self).__init__)(**processed_kwargs)


class TransformParameters(troposphere.glue.TransformParameters, Mixin):

    def __init__(self, title=None, TransformType=REQUIRED, FindMatchesParameters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TransformType=TransformType, 
         FindMatchesParameters=FindMatchesParameters, **kwargs)
        (super(TransformParameters, self).__init__)(**processed_kwargs)


class MLTransform(troposphere.glue.MLTransform, Mixin):

    def __init__(self, title, template=None, validation=True, InputRecordTables=REQUIRED, Role=REQUIRED, TransformParameters=REQUIRED, Description=NOTHING, GlueVersion=NOTHING, MaxCapacity=NOTHING, MaxRetries=NOTHING, Name=NOTHING, NumberOfWorkers=NOTHING, Timeout=NOTHING, WorkerType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         InputRecordTables=InputRecordTables, 
         Role=Role, 
         TransformParameters=TransformParameters, 
         Description=Description, 
         GlueVersion=GlueVersion, 
         MaxCapacity=MaxCapacity, 
         MaxRetries=MaxRetries, 
         Name=Name, 
         NumberOfWorkers=NumberOfWorkers, 
         Timeout=Timeout, 
         WorkerType=WorkerType, **kwargs)
        (super(MLTransform, self).__init__)(**processed_kwargs)


class Column(troposphere.glue.Column, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Comment=NOTHING, Type=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Comment=Comment, 
         Type=Type, **kwargs)
        (super(Column, self).__init__)(**processed_kwargs)


class Order(troposphere.glue.Order, Mixin):

    def __init__(self, title=None, Column=REQUIRED, SortOrder=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Column=Column, 
         SortOrder=SortOrder, **kwargs)
        (super(Order, self).__init__)(**processed_kwargs)


class SerdeInfo(troposphere.glue.SerdeInfo, Mixin):

    def __init__(self, title=None, Name=NOTHING, Parameters=NOTHING, SerializationLibrary=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Parameters=Parameters, 
         SerializationLibrary=SerializationLibrary, **kwargs)
        (super(SerdeInfo, self).__init__)(**processed_kwargs)


class SkewedInfo(troposphere.glue.SkewedInfo, Mixin):

    def __init__(self, title=None, SkewedColumnNames=NOTHING, SkewedColumnValues=NOTHING, SkewedColumnValueLocationMaps=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SkewedColumnNames=SkewedColumnNames, 
         SkewedColumnValues=SkewedColumnValues, 
         SkewedColumnValueLocationMaps=SkewedColumnValueLocationMaps, **kwargs)
        (super(SkewedInfo, self).__init__)(**processed_kwargs)


class StorageDescriptor(troposphere.glue.StorageDescriptor, Mixin):

    def __init__(self, title=None, BucketColumns=NOTHING, Columns=NOTHING, Compressed=NOTHING, InputFormat=NOTHING, Location=NOTHING, NumberOfBuckets=NOTHING, OutputFormat=NOTHING, Parameters=NOTHING, SerdeInfo=NOTHING, SkewedInfo=NOTHING, SortColumns=NOTHING, StoredAsSubDirectories=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BucketColumns=BucketColumns, 
         Columns=Columns, 
         Compressed=Compressed, 
         InputFormat=InputFormat, 
         Location=Location, 
         NumberOfBuckets=NumberOfBuckets, 
         OutputFormat=OutputFormat, 
         Parameters=Parameters, 
         SerdeInfo=SerdeInfo, 
         SkewedInfo=SkewedInfo, 
         SortColumns=SortColumns, 
         StoredAsSubDirectories=StoredAsSubDirectories, **kwargs)
        (super(StorageDescriptor, self).__init__)(**processed_kwargs)


class PartitionInput(troposphere.glue.PartitionInput, Mixin):

    def __init__(self, title=None, Values=REQUIRED, Parameters=NOTHING, StorageDescriptor=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Values=Values, 
         Parameters=Parameters, 
         StorageDescriptor=StorageDescriptor, **kwargs)
        (super(PartitionInput, self).__init__)(**processed_kwargs)


class Partition(troposphere.glue.Partition, Mixin):

    def __init__(self, title, template=None, validation=True, CatalogId=REQUIRED, DatabaseName=REQUIRED, PartitionInput=REQUIRED, TableName=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CatalogId=CatalogId, 
         DatabaseName=DatabaseName, 
         PartitionInput=PartitionInput, 
         TableName=TableName, **kwargs)
        (super(Partition, self).__init__)(**processed_kwargs)


class CloudWatchEncryption(troposphere.glue.CloudWatchEncryption, Mixin):

    def __init__(self, title=None, CloudWatchEncryptionMode=NOTHING, KmsKeyArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CloudWatchEncryptionMode=CloudWatchEncryptionMode, 
         KmsKeyArn=KmsKeyArn, **kwargs)
        (super(CloudWatchEncryption, self).__init__)(**processed_kwargs)


class JobBookmarksEncryption(troposphere.glue.JobBookmarksEncryption, Mixin):

    def __init__(self, title=None, JobBookmarksEncryptionMode=NOTHING, KmsKeyArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         JobBookmarksEncryptionMode=JobBookmarksEncryptionMode, 
         KmsKeyArn=KmsKeyArn, **kwargs)
        (super(JobBookmarksEncryption, self).__init__)(**processed_kwargs)


class S3Encryptions(troposphere.glue.S3Encryptions, Mixin):

    def __init__(self, title=None, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, **kwargs)
        (super(S3Encryptions, self).__init__)(**processed_kwargs)


class EncryptionConfiguration(troposphere.glue.EncryptionConfiguration, Mixin):

    def __init__(self, title=None, CloudWatchEncryption=NOTHING, JobBookmarksEncryption=NOTHING, S3Encryptions=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CloudWatchEncryption=CloudWatchEncryption, 
         JobBookmarksEncryption=JobBookmarksEncryption, 
         S3Encryptions=S3Encryptions, **kwargs)
        (super(EncryptionConfiguration, self).__init__)(**processed_kwargs)


class SecurityConfiguration(troposphere.glue.SecurityConfiguration, Mixin):

    def __init__(self, title, template=None, validation=True, EncryptionConfiguration=REQUIRED, Name=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         EncryptionConfiguration=EncryptionConfiguration, 
         Name=Name, **kwargs)
        (super(SecurityConfiguration, self).__init__)(**processed_kwargs)


class TableInput(troposphere.glue.TableInput, Mixin):

    def __init__(self, title=None, Description=NOTHING, Name=NOTHING, Owner=NOTHING, Parameters=NOTHING, PartitionKeys=NOTHING, Retention=NOTHING, StorageDescriptor=NOTHING, TableType=NOTHING, ViewExpandedText=NOTHING, ViewOriginalText=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Description=Description, 
         Name=Name, 
         Owner=Owner, 
         Parameters=Parameters, 
         PartitionKeys=PartitionKeys, 
         Retention=Retention, 
         StorageDescriptor=StorageDescriptor, 
         TableType=TableType, 
         ViewExpandedText=ViewExpandedText, 
         ViewOriginalText=ViewOriginalText, **kwargs)
        (super(TableInput, self).__init__)(**processed_kwargs)


class Table(troposphere.glue.Table, Mixin):

    def __init__(self, title, template=None, validation=True, CatalogId=REQUIRED, DatabaseName=REQUIRED, TableInput=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CatalogId=CatalogId, 
         DatabaseName=DatabaseName, 
         TableInput=TableInput, **kwargs)
        (super(Table, self).__init__)(**processed_kwargs)


class Action(troposphere.glue.Action, Mixin):

    def __init__(self, title=None, Arguments=NOTHING, CrawlerName=NOTHING, JobName=NOTHING, SecurityConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Arguments=Arguments, 
         CrawlerName=CrawlerName, 
         JobName=JobName, 
         SecurityConfiguration=SecurityConfiguration, **kwargs)
        (super(Action, self).__init__)(**processed_kwargs)


class Condition(troposphere.glue.Condition, Mixin):

    def __init__(self, title=None, CrawlerName=NOTHING, CrawlState=NOTHING, JobName=NOTHING, LogicalOperator=NOTHING, State=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CrawlerName=CrawlerName, 
         CrawlState=CrawlState, 
         JobName=JobName, 
         LogicalOperator=LogicalOperator, 
         State=State, **kwargs)
        (super(Condition, self).__init__)(**processed_kwargs)


class Predicate(troposphere.glue.Predicate, Mixin):

    def __init__(self, title=None, Conditions=NOTHING, Logical=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Conditions=Conditions, 
         Logical=Logical, **kwargs)
        (super(Predicate, self).__init__)(**processed_kwargs)


class Trigger(troposphere.glue.Trigger, Mixin):

    def __init__(self, title, template=None, validation=True, Actions=REQUIRED, Type=REQUIRED, Description=NOTHING, Name=NOTHING, Predicate=NOTHING, Schedule=NOTHING, StartOnCreation=NOTHING, Tags=NOTHING, WorkflowName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Actions=Actions, 
         Type=Type, 
         Description=Description, 
         Name=Name, 
         Predicate=Predicate, 
         Schedule=Schedule, 
         StartOnCreation=StartOnCreation, 
         Tags=Tags, 
         WorkflowName=WorkflowName, **kwargs)
        (super(Trigger, self).__init__)(**processed_kwargs)


class Workflow(troposphere.glue.Workflow, Mixin):

    def __init__(self, title, template=None, validation=True, DefaultRunProperties=NOTHING, Description=NOTHING, Name=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DefaultRunProperties=DefaultRunProperties, 
         Description=Description, 
         Name=Name, 
         Tags=Tags, **kwargs)
        (super(Workflow, self).__init__)(**processed_kwargs)