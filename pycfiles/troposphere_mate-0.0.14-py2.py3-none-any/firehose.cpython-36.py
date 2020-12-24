# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/firehose.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 25530 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.firehose
from troposphere.firehose import BufferingHints as _BufferingHints, CloudWatchLoggingOptions as _CloudWatchLoggingOptions, CopyCommand as _CopyCommand, DataFormatConversionConfiguration as _DataFormatConversionConfiguration, Deserializer as _Deserializer, ElasticsearchDestinationConfiguration as _ElasticsearchDestinationConfiguration, EncryptionConfiguration as _EncryptionConfiguration, ExtendedS3DestinationConfiguration as _ExtendedS3DestinationConfiguration, HiveJsonSerDe as _HiveJsonSerDe, InputFormatConfiguration as _InputFormatConfiguration, KMSEncryptionConfig as _KMSEncryptionConfig, KinesisStreamSourceConfiguration as _KinesisStreamSourceConfiguration, OpenXJsonSerDe as _OpenXJsonSerDe, OrcSerDe as _OrcSerDe, OutputFormatConfiguration as _OutputFormatConfiguration, ParquetSerDe as _ParquetSerDe, ProcessingConfiguration as _ProcessingConfiguration, Processor as _Processor, ProcessorParameter as _ProcessorParameter, RedshiftDestinationConfiguration as _RedshiftDestinationConfiguration, RetryOptions as _RetryOptions, S3Configuration as _S3Configuration, S3DestinationConfiguration as _S3DestinationConfiguration, SchemaConfiguration as _SchemaConfiguration, Serializer as _Serializer, SplunkDestinationConfiguration as _SplunkDestinationConfiguration, SplunkRetryOptions as _SplunkRetryOptions
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class BufferingHints(troposphere.firehose.BufferingHints, Mixin):

    def __init__(self, title=None, IntervalInSeconds=REQUIRED, SizeInMBs=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         IntervalInSeconds=IntervalInSeconds, 
         SizeInMBs=SizeInMBs, **kwargs)
        (super(BufferingHints, self).__init__)(**processed_kwargs)


class CloudWatchLoggingOptions(troposphere.firehose.CloudWatchLoggingOptions, Mixin):

    def __init__(self, title=None, Enabled=NOTHING, LogGroupName=NOTHING, LogStreamName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Enabled=Enabled, 
         LogGroupName=LogGroupName, 
         LogStreamName=LogStreamName, **kwargs)
        (super(CloudWatchLoggingOptions, self).__init__)(**processed_kwargs)


class RetryOptions(troposphere.firehose.RetryOptions, Mixin):

    def __init__(self, title=None, DurationInSeconds=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DurationInSeconds=DurationInSeconds, **kwargs)
        (super(RetryOptions, self).__init__)(**processed_kwargs)


class KMSEncryptionConfig(troposphere.firehose.KMSEncryptionConfig, Mixin):

    def __init__(self, title=None, AWSKMSKeyARN=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AWSKMSKeyARN=AWSKMSKeyARN, **kwargs)
        (super(KMSEncryptionConfig, self).__init__)(**processed_kwargs)


class EncryptionConfiguration(troposphere.firehose.EncryptionConfiguration, Mixin):

    def __init__(self, title=None, KMSEncryptionConfig=NOTHING, NoEncryptionConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         KMSEncryptionConfig=KMSEncryptionConfig, 
         NoEncryptionConfig=NoEncryptionConfig, **kwargs)
        (super(EncryptionConfiguration, self).__init__)(**processed_kwargs)


class S3Configuration(troposphere.firehose.S3Configuration, Mixin):

    def __init__(self, title=None, BucketARN=REQUIRED, BufferingHints=REQUIRED, CompressionFormat=REQUIRED, RoleARN=REQUIRED, CloudWatchLoggingOptions=NOTHING, EncryptionConfiguration=NOTHING, Prefix=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BucketARN=BucketARN, 
         BufferingHints=BufferingHints, 
         CompressionFormat=CompressionFormat, 
         RoleARN=RoleARN, 
         CloudWatchLoggingOptions=CloudWatchLoggingOptions, 
         EncryptionConfiguration=EncryptionConfiguration, 
         Prefix=Prefix, **kwargs)
        (super(S3Configuration, self).__init__)(**processed_kwargs)


class CopyCommand(troposphere.firehose.CopyCommand, Mixin):

    def __init__(self, title=None, DataTableName=REQUIRED, CopyOptions=NOTHING, DataTableColumns=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DataTableName=DataTableName, 
         CopyOptions=CopyOptions, 
         DataTableColumns=DataTableColumns, **kwargs)
        (super(CopyCommand, self).__init__)(**processed_kwargs)


class ProcessorParameter(troposphere.firehose.ProcessorParameter, Mixin):

    def __init__(self, title=None, ParameterName=REQUIRED, ParameterValue=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ParameterName=ParameterName, 
         ParameterValue=ParameterValue, **kwargs)
        (super(ProcessorParameter, self).__init__)(**processed_kwargs)


class Processor(troposphere.firehose.Processor, Mixin):

    def __init__(self, title=None, Parameters=REQUIRED, Type=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Parameters=Parameters, 
         Type=Type, **kwargs)
        (super(Processor, self).__init__)(**processed_kwargs)


class ProcessingConfiguration(troposphere.firehose.ProcessingConfiguration, Mixin):

    def __init__(self, title=None, Enabled=REQUIRED, Processors=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Enabled=Enabled, 
         Processors=Processors, **kwargs)
        (super(ProcessingConfiguration, self).__init__)(**processed_kwargs)


class ElasticsearchDestinationConfiguration(troposphere.firehose.ElasticsearchDestinationConfiguration, Mixin):

    def __init__(self, title=None, BufferingHints=REQUIRED, DomainARN=REQUIRED, IndexName=REQUIRED, IndexRotationPeriod=REQUIRED, RoleARN=REQUIRED, S3BackupMode=REQUIRED, TypeName=REQUIRED, CloudWatchLoggingOptions=NOTHING, ProcessingConfiguration=NOTHING, RetryOptions=NOTHING, S3Configuration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BufferingHints=BufferingHints, 
         DomainARN=DomainARN, 
         IndexName=IndexName, 
         IndexRotationPeriod=IndexRotationPeriod, 
         RoleARN=RoleARN, 
         S3BackupMode=S3BackupMode, 
         TypeName=TypeName, 
         CloudWatchLoggingOptions=CloudWatchLoggingOptions, 
         ProcessingConfiguration=ProcessingConfiguration, 
         RetryOptions=RetryOptions, 
         S3Configuration=S3Configuration, **kwargs)
        (super(ElasticsearchDestinationConfiguration, self).__init__)(**processed_kwargs)


class RedshiftDestinationConfiguration(troposphere.firehose.RedshiftDestinationConfiguration, Mixin):

    def __init__(self, title=None, ClusterJDBCURL=REQUIRED, CopyCommand=REQUIRED, Password=REQUIRED, RoleARN=REQUIRED, S3Configuration=REQUIRED, Username=REQUIRED, CloudWatchLoggingOptions=NOTHING, ProcessingConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ClusterJDBCURL=ClusterJDBCURL, 
         CopyCommand=CopyCommand, 
         Password=Password, 
         RoleARN=RoleARN, 
         S3Configuration=S3Configuration, 
         Username=Username, 
         CloudWatchLoggingOptions=CloudWatchLoggingOptions, 
         ProcessingConfiguration=ProcessingConfiguration, **kwargs)
        (super(RedshiftDestinationConfiguration, self).__init__)(**processed_kwargs)


class S3DestinationConfiguration(troposphere.firehose.S3DestinationConfiguration, Mixin):

    def __init__(self, title=None, BucketARN=REQUIRED, BufferingHints=REQUIRED, CompressionFormat=REQUIRED, RoleARN=REQUIRED, CloudWatchLoggingOptions=NOTHING, EncryptionConfiguration=NOTHING, ErrorOutputPrefix=NOTHING, Prefix=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BucketARN=BucketARN, 
         BufferingHints=BufferingHints, 
         CompressionFormat=CompressionFormat, 
         RoleARN=RoleARN, 
         CloudWatchLoggingOptions=CloudWatchLoggingOptions, 
         EncryptionConfiguration=EncryptionConfiguration, 
         ErrorOutputPrefix=ErrorOutputPrefix, 
         Prefix=Prefix, **kwargs)
        (super(S3DestinationConfiguration, self).__init__)(**processed_kwargs)


class HiveJsonSerDe(troposphere.firehose.HiveJsonSerDe, Mixin):

    def __init__(self, title=None, TimestampFormats=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TimestampFormats=TimestampFormats, **kwargs)
        (super(HiveJsonSerDe, self).__init__)(**processed_kwargs)


class OpenXJsonSerDe(troposphere.firehose.OpenXJsonSerDe, Mixin):

    def __init__(self, title=None, CaseInsensitive=NOTHING, ColumnToJsonKeyMappings=NOTHING, ConvertDotsInJsonKeysToUnderscores=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CaseInsensitive=CaseInsensitive, 
         ColumnToJsonKeyMappings=ColumnToJsonKeyMappings, 
         ConvertDotsInJsonKeysToUnderscores=ConvertDotsInJsonKeysToUnderscores, **kwargs)
        (super(OpenXJsonSerDe, self).__init__)(**processed_kwargs)


class Deserializer(troposphere.firehose.Deserializer, Mixin):

    def __init__(self, title=None, HiveJsonSerDe=NOTHING, OpenXJsonSerDe=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HiveJsonSerDe=HiveJsonSerDe, 
         OpenXJsonSerDe=OpenXJsonSerDe, **kwargs)
        (super(Deserializer, self).__init__)(**processed_kwargs)


class InputFormatConfiguration(troposphere.firehose.InputFormatConfiguration, Mixin):

    def __init__(self, title=None, Deserializer=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Deserializer=Deserializer, **kwargs)
        (super(InputFormatConfiguration, self).__init__)(**processed_kwargs)


class OrcSerDe(troposphere.firehose.OrcSerDe, Mixin):

    def __init__(self, title=None, BlockSizeBytes=NOTHING, BloomFilterColumns=NOTHING, BloomFilterFalsePositiveProbability=NOTHING, Compression=NOTHING, DictionaryKeyThreshold=NOTHING, EnablePadding=NOTHING, FormatVersion=NOTHING, PaddingTolerance=NOTHING, RowIndexStride=NOTHING, StripeSizeBytes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BlockSizeBytes=BlockSizeBytes, 
         BloomFilterColumns=BloomFilterColumns, 
         BloomFilterFalsePositiveProbability=BloomFilterFalsePositiveProbability, 
         Compression=Compression, 
         DictionaryKeyThreshold=DictionaryKeyThreshold, 
         EnablePadding=EnablePadding, 
         FormatVersion=FormatVersion, 
         PaddingTolerance=PaddingTolerance, 
         RowIndexStride=RowIndexStride, 
         StripeSizeBytes=StripeSizeBytes, **kwargs)
        (super(OrcSerDe, self).__init__)(**processed_kwargs)


class ParquetSerDe(troposphere.firehose.ParquetSerDe, Mixin):

    def __init__(self, title=None, BlockSizeBytes=NOTHING, Compression=NOTHING, EnableDictionaryCompression=NOTHING, MaxPaddingBytes=NOTHING, PageSizeBytes=NOTHING, WriterVersion=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BlockSizeBytes=BlockSizeBytes, 
         Compression=Compression, 
         EnableDictionaryCompression=EnableDictionaryCompression, 
         MaxPaddingBytes=MaxPaddingBytes, 
         PageSizeBytes=PageSizeBytes, 
         WriterVersion=WriterVersion, **kwargs)
        (super(ParquetSerDe, self).__init__)(**processed_kwargs)


class Serializer(troposphere.firehose.Serializer, Mixin):

    def __init__(self, title=None, OrcSerDe=NOTHING, ParquetSerDe=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         OrcSerDe=OrcSerDe, 
         ParquetSerDe=ParquetSerDe, **kwargs)
        (super(Serializer, self).__init__)(**processed_kwargs)


class OutputFormatConfiguration(troposphere.firehose.OutputFormatConfiguration, Mixin):

    def __init__(self, title=None, Serializer=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Serializer=Serializer, **kwargs)
        (super(OutputFormatConfiguration, self).__init__)(**processed_kwargs)


class SchemaConfiguration(troposphere.firehose.SchemaConfiguration, Mixin):

    def __init__(self, title=None, CatalogId=REQUIRED, DatabaseName=REQUIRED, Region=REQUIRED, RoleARN=REQUIRED, TableName=REQUIRED, VersionId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CatalogId=CatalogId, 
         DatabaseName=DatabaseName, 
         Region=Region, 
         RoleARN=RoleARN, 
         TableName=TableName, 
         VersionId=VersionId, **kwargs)
        (super(SchemaConfiguration, self).__init__)(**processed_kwargs)


class DataFormatConversionConfiguration(troposphere.firehose.DataFormatConversionConfiguration, Mixin):

    def __init__(self, title=None, Enabled=REQUIRED, InputFormatConfiguration=REQUIRED, OutputFormatConfiguration=REQUIRED, SchemaConfiguration=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Enabled=Enabled, 
         InputFormatConfiguration=InputFormatConfiguration, 
         OutputFormatConfiguration=OutputFormatConfiguration, 
         SchemaConfiguration=SchemaConfiguration, **kwargs)
        (super(DataFormatConversionConfiguration, self).__init__)(**processed_kwargs)


class ExtendedS3DestinationConfiguration(troposphere.firehose.ExtendedS3DestinationConfiguration, Mixin):

    def __init__(self, title=None, BucketARN=REQUIRED, BufferingHints=REQUIRED, CompressionFormat=REQUIRED, RoleARN=REQUIRED, CloudWatchLoggingOptions=NOTHING, DataFormatConversionConfiguration=NOTHING, EncryptionConfiguration=NOTHING, ErrorOutputPrefix=NOTHING, Prefix=NOTHING, ProcessingConfiguration=NOTHING, S3BackupConfiguration=NOTHING, S3BackupMode=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BucketARN=BucketARN, 
         BufferingHints=BufferingHints, 
         CompressionFormat=CompressionFormat, 
         RoleARN=RoleARN, 
         CloudWatchLoggingOptions=CloudWatchLoggingOptions, 
         DataFormatConversionConfiguration=DataFormatConversionConfiguration, 
         EncryptionConfiguration=EncryptionConfiguration, 
         ErrorOutputPrefix=ErrorOutputPrefix, 
         Prefix=Prefix, 
         ProcessingConfiguration=ProcessingConfiguration, 
         S3BackupConfiguration=S3BackupConfiguration, 
         S3BackupMode=S3BackupMode, **kwargs)
        (super(ExtendedS3DestinationConfiguration, self).__init__)(**processed_kwargs)


class KinesisStreamSourceConfiguration(troposphere.firehose.KinesisStreamSourceConfiguration, Mixin):

    def __init__(self, title=None, KinesisStreamARN=REQUIRED, RoleARN=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         KinesisStreamARN=KinesisStreamARN, 
         RoleARN=RoleARN, **kwargs)
        (super(KinesisStreamSourceConfiguration, self).__init__)(**processed_kwargs)


class SplunkRetryOptions(troposphere.firehose.SplunkRetryOptions, Mixin):

    def __init__(self, title=None, DurationInSeconds=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DurationInSeconds=DurationInSeconds, **kwargs)
        (super(SplunkRetryOptions, self).__init__)(**processed_kwargs)


class SplunkDestinationConfiguration(troposphere.firehose.SplunkDestinationConfiguration, Mixin):

    def __init__(self, title=None, HECEndpoint=REQUIRED, HECEndpointType=REQUIRED, HECToken=REQUIRED, S3Configuration=REQUIRED, CloudWatchLoggingOptions=NOTHING, HECAcknowledgmentTimeoutInSeconds=NOTHING, ProcessingConfiguration=NOTHING, RetryOptions=NOTHING, S3BackupMode=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HECEndpoint=HECEndpoint, 
         HECEndpointType=HECEndpointType, 
         HECToken=HECToken, 
         S3Configuration=S3Configuration, 
         CloudWatchLoggingOptions=CloudWatchLoggingOptions, 
         HECAcknowledgmentTimeoutInSeconds=HECAcknowledgmentTimeoutInSeconds, 
         ProcessingConfiguration=ProcessingConfiguration, 
         RetryOptions=RetryOptions, 
         S3BackupMode=S3BackupMode, **kwargs)
        (super(SplunkDestinationConfiguration, self).__init__)(**processed_kwargs)


class DeliveryStream(troposphere.firehose.DeliveryStream, Mixin):

    def __init__(self, title, template=None, validation=True, DeliveryStreamName=NOTHING, DeliveryStreamType=NOTHING, ElasticsearchDestinationConfiguration=NOTHING, ExtendedS3DestinationConfiguration=NOTHING, KinesisStreamSourceConfiguration=NOTHING, RedshiftDestinationConfiguration=NOTHING, S3DestinationConfiguration=NOTHING, SplunkDestinationConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DeliveryStreamName=DeliveryStreamName, 
         DeliveryStreamType=DeliveryStreamType, 
         ElasticsearchDestinationConfiguration=ElasticsearchDestinationConfiguration, 
         ExtendedS3DestinationConfiguration=ExtendedS3DestinationConfiguration, 
         KinesisStreamSourceConfiguration=KinesisStreamSourceConfiguration, 
         RedshiftDestinationConfiguration=RedshiftDestinationConfiguration, 
         S3DestinationConfiguration=S3DestinationConfiguration, 
         SplunkDestinationConfiguration=SplunkDestinationConfiguration, **kwargs)
        (super(DeliveryStream, self).__init__)(**processed_kwargs)