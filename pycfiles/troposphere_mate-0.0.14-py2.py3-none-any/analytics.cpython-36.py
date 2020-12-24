# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/analytics.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 15744 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.analytics
from troposphere.analytics import CSVMappingParameters as _CSVMappingParameters, DestinationSchema as _DestinationSchema, Input as _Input, InputLambdaProcessor as _InputLambdaProcessor, InputParallelism as _InputParallelism, InputProcessingConfiguration as _InputProcessingConfiguration, InputSchema as _InputSchema, JSONMappingParameters as _JSONMappingParameters, KinesisFirehoseInput as _KinesisFirehoseInput, KinesisFirehoseOutput as _KinesisFirehoseOutput, KinesisStreamsInput as _KinesisStreamsInput, KinesisStreamsOutput as _KinesisStreamsOutput, LambdaOutput as _LambdaOutput, MappingParameters as _MappingParameters, Output as _Output, RecordColumn as _RecordColumn, RecordFormat as _RecordFormat, ReferenceDataSource as _ReferenceDataSource, ReferenceSchema as _ReferenceSchema, S3ReferenceDataSource as _S3ReferenceDataSource
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class InputParallelism(troposphere.analytics.InputParallelism, Mixin):

    def __init__(self, title=None, Count=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Count=Count, **kwargs)
        (super(InputParallelism, self).__init__)(**processed_kwargs)


class RecordColumn(troposphere.analytics.RecordColumn, Mixin):

    def __init__(self, title=None, Name=REQUIRED, SqlType=REQUIRED, Mapping=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         SqlType=SqlType, 
         Mapping=Mapping, **kwargs)
        (super(RecordColumn, self).__init__)(**processed_kwargs)


class CSVMappingParameters(troposphere.analytics.CSVMappingParameters, Mixin):

    def __init__(self, title=None, RecordColumnDelimiter=REQUIRED, RecordRowDelimiter=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RecordColumnDelimiter=RecordColumnDelimiter, 
         RecordRowDelimiter=RecordRowDelimiter, **kwargs)
        (super(CSVMappingParameters, self).__init__)(**processed_kwargs)


class JSONMappingParameters(troposphere.analytics.JSONMappingParameters, Mixin):

    def __init__(self, title=None, RecordRowPath=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RecordRowPath=RecordRowPath, **kwargs)
        (super(JSONMappingParameters, self).__init__)(**processed_kwargs)


class MappingParameters(troposphere.analytics.MappingParameters, Mixin):

    def __init__(self, title=None, CSVMappingParameters=NOTHING, JSONMappingParameters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CSVMappingParameters=CSVMappingParameters, 
         JSONMappingParameters=JSONMappingParameters, **kwargs)
        (super(MappingParameters, self).__init__)(**processed_kwargs)


class RecordFormat(troposphere.analytics.RecordFormat, Mixin):

    def __init__(self, title=None, RecordFormatType=REQUIRED, MappingParameters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RecordFormatType=RecordFormatType, 
         MappingParameters=MappingParameters, **kwargs)
        (super(RecordFormat, self).__init__)(**processed_kwargs)


class InputSchema(troposphere.analytics.InputSchema, Mixin):

    def __init__(self, title=None, RecordColumns=REQUIRED, RecordFormat=REQUIRED, RecordEncoding=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RecordColumns=RecordColumns, 
         RecordFormat=RecordFormat, 
         RecordEncoding=RecordEncoding, **kwargs)
        (super(InputSchema, self).__init__)(**processed_kwargs)


class KinesisFirehoseInput(troposphere.analytics.KinesisFirehoseInput, Mixin):

    def __init__(self, title=None, ResourceARN=REQUIRED, RoleARN=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ResourceARN=ResourceARN, 
         RoleARN=RoleARN, **kwargs)
        (super(KinesisFirehoseInput, self).__init__)(**processed_kwargs)


class KinesisStreamsInput(troposphere.analytics.KinesisStreamsInput, Mixin):

    def __init__(self, title=None, ResourceARN=REQUIRED, RoleARN=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ResourceARN=ResourceARN, 
         RoleARN=RoleARN, **kwargs)
        (super(KinesisStreamsInput, self).__init__)(**processed_kwargs)


class InputLambdaProcessor(troposphere.analytics.InputLambdaProcessor, Mixin):

    def __init__(self, title=None, ResourceARN=REQUIRED, RoleARN=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ResourceARN=ResourceARN, 
         RoleARN=RoleARN, **kwargs)
        (super(InputLambdaProcessor, self).__init__)(**processed_kwargs)


class InputProcessingConfiguration(troposphere.analytics.InputProcessingConfiguration, Mixin):

    def __init__(self, title=None, InputLambdaProcessor=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         InputLambdaProcessor=InputLambdaProcessor, **kwargs)
        (super(InputProcessingConfiguration, self).__init__)(**processed_kwargs)


class Input(troposphere.analytics.Input, Mixin):

    def __init__(self, title=None, NamePrefix=REQUIRED, InputSchema=REQUIRED, InputParallelism=NOTHING, KinesisFirehoseInput=NOTHING, KinesisStreamsInput=NOTHING, InputProcessingConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         NamePrefix=NamePrefix, 
         InputSchema=InputSchema, 
         InputParallelism=InputParallelism, 
         KinesisFirehoseInput=KinesisFirehoseInput, 
         KinesisStreamsInput=KinesisStreamsInput, 
         InputProcessingConfiguration=InputProcessingConfiguration, **kwargs)
        (super(Input, self).__init__)(**processed_kwargs)


class Application(troposphere.analytics.Application, Mixin):

    def __init__(self, title, template=None, validation=True, Inputs=REQUIRED, ApplicationName=NOTHING, ApplicationDescription=NOTHING, ApplicationCode=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Inputs=Inputs, 
         ApplicationName=ApplicationName, 
         ApplicationDescription=ApplicationDescription, 
         ApplicationCode=ApplicationCode, **kwargs)
        (super(Application, self).__init__)(**processed_kwargs)


class DestinationSchema(troposphere.analytics.DestinationSchema, Mixin):

    def __init__(self, title=None, RecordFormatType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RecordFormatType=RecordFormatType, **kwargs)
        (super(DestinationSchema, self).__init__)(**processed_kwargs)


class KinesisFirehoseOutput(troposphere.analytics.KinesisFirehoseOutput, Mixin):

    def __init__(self, title=None, ResourceARN=REQUIRED, RoleARN=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ResourceARN=ResourceARN, 
         RoleARN=RoleARN, **kwargs)
        (super(KinesisFirehoseOutput, self).__init__)(**processed_kwargs)


class KinesisStreamsOutput(troposphere.analytics.KinesisStreamsOutput, Mixin):

    def __init__(self, title=None, ResourceARN=REQUIRED, RoleARN=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ResourceARN=ResourceARN, 
         RoleARN=RoleARN, **kwargs)
        (super(KinesisStreamsOutput, self).__init__)(**processed_kwargs)


class LambdaOutput(troposphere.analytics.LambdaOutput, Mixin):

    def __init__(self, title=None, ResourceARN=REQUIRED, RoleARN=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ResourceARN=ResourceARN, 
         RoleARN=RoleARN, **kwargs)
        (super(LambdaOutput, self).__init__)(**processed_kwargs)


class Output(troposphere.analytics.Output, Mixin):

    def __init__(self, title=None, DestinationSchema=REQUIRED, Name=REQUIRED, KinesisFirehoseOutput=NOTHING, KinesisStreamsOutput=NOTHING, LambdaOutput=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DestinationSchema=DestinationSchema, 
         Name=Name, 
         KinesisFirehoseOutput=KinesisFirehoseOutput, 
         KinesisStreamsOutput=KinesisStreamsOutput, 
         LambdaOutput=LambdaOutput, **kwargs)
        (super(Output, self).__init__)(**processed_kwargs)


class ApplicationOutput(troposphere.analytics.ApplicationOutput, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationName=REQUIRED, Output=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationName=ApplicationName, 
         Output=Output, **kwargs)
        (super(ApplicationOutput, self).__init__)(**processed_kwargs)


class ReferenceSchema(troposphere.analytics.ReferenceSchema, Mixin):

    def __init__(self, title=None, RecordColumns=REQUIRED, RecordFormat=REQUIRED, RecordEncoding=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RecordColumns=RecordColumns, 
         RecordFormat=RecordFormat, 
         RecordEncoding=RecordEncoding, **kwargs)
        (super(ReferenceSchema, self).__init__)(**processed_kwargs)


class S3ReferenceDataSource(troposphere.analytics.S3ReferenceDataSource, Mixin):

    def __init__(self, title=None, BucketARN=NOTHING, FileKey=NOTHING, ReferenceRoleARN=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BucketARN=BucketARN, 
         FileKey=FileKey, 
         ReferenceRoleARN=ReferenceRoleARN, **kwargs)
        (super(S3ReferenceDataSource, self).__init__)(**processed_kwargs)


class ReferenceDataSource(troposphere.analytics.ReferenceDataSource, Mixin):

    def __init__(self, title=None, ReferenceSchema=REQUIRED, S3ReferenceDataSource=NOTHING, TableName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ReferenceSchema=ReferenceSchema, 
         S3ReferenceDataSource=S3ReferenceDataSource, 
         TableName=TableName, **kwargs)
        (super(ReferenceDataSource, self).__init__)(**processed_kwargs)


class ApplicationReferenceDataSource(troposphere.analytics.ApplicationReferenceDataSource, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationName=REQUIRED, ReferenceDataSource=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationName=ApplicationName, 
         ReferenceDataSource=ReferenceDataSource, **kwargs)
        (super(ApplicationReferenceDataSource, self).__init__)(**processed_kwargs)