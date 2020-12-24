# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/serverless.py
# Compiled at: 2020-02-12 18:15:54
# Size of source mod 2**32: 24139 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.serverless
from troposphere.serverless import AccessLogSetting as _AccessLogSetting, Auth as _Auth, Authorizers as _Authorizers, CanarySetting as _CanarySetting, CognitoAuth as _CognitoAuth, CognitoAuthIdentity as _CognitoAuthIdentity, Cors as _Cors, DeadLetterQueue as _DeadLetterQueue, DeploymentPreference as _DeploymentPreference, Environment as _Environment, Filter as _Filter, Hooks as _Hooks, LambdaRequestAuth as _LambdaRequestAuth, LambdaRequestAuthIdentity as _LambdaRequestAuthIdentity, LambdaTokenAuth as _LambdaTokenAuth, LambdaTokenAuthIdentity as _LambdaTokenAuthIdentity, MethodSetting as _MethodSetting, PrimaryKey as _PrimaryKey, ProvisionedThroughput as _ProvisionedThroughput, S3Location as _S3Location, SSESpecification as _SSESpecification, VPCConfig as _VPCConfig
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class DeadLetterQueue(troposphere.serverless.DeadLetterQueue, Mixin):

    def __init__(self, title=None, Type=NOTHING, TargetArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         TargetArn=TargetArn, **kwargs)
        (super(DeadLetterQueue, self).__init__)(**processed_kwargs)


class S3Location(troposphere.serverless.S3Location, Mixin):

    def __init__(self, title=None, Bucket=REQUIRED, Key=REQUIRED, Version=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Bucket=Bucket, 
         Key=Key, 
         Version=Version, **kwargs)
        (super(S3Location, self).__init__)(**processed_kwargs)


class Hooks(troposphere.serverless.Hooks, Mixin):

    def __init__(self, title=None, PreTraffic=NOTHING, PostTraffic=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PreTraffic=PreTraffic, 
         PostTraffic=PostTraffic, **kwargs)
        (super(Hooks, self).__init__)(**processed_kwargs)


class DeploymentPreference(troposphere.serverless.DeploymentPreference, Mixin):

    def __init__(self, title=None, Type=REQUIRED, Alarms=NOTHING, Hooks=NOTHING, Enabled=NOTHING, Role=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         Alarms=Alarms, 
         Hooks=Hooks, 
         Enabled=Enabled, 
         Role=Role, **kwargs)
        (super(DeploymentPreference, self).__init__)(**processed_kwargs)


class Function(troposphere.serverless.Function, Mixin):

    def __init__(self, title, template=None, validation=True, Handler=REQUIRED, Runtime=REQUIRED, CodeUri=NOTHING, InlineCode=NOTHING, FunctionName=NOTHING, Description=NOTHING, MemorySize=NOTHING, Timeout=NOTHING, Role=NOTHING, Policies=NOTHING, Environment=NOTHING, VpcConfig=NOTHING, Events=NOTHING, Tags=NOTHING, Tracing=NOTHING, KmsKeyArn=NOTHING, DeadLetterQueue=NOTHING, DeploymentPreference=NOTHING, Layers=NOTHING, AutoPublishAlias=NOTHING, ReservedConcurrentExecutions=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Handler=Handler, 
         Runtime=Runtime, 
         CodeUri=CodeUri, 
         InlineCode=InlineCode, 
         FunctionName=FunctionName, 
         Description=Description, 
         MemorySize=MemorySize, 
         Timeout=Timeout, 
         Role=Role, 
         Policies=Policies, 
         Environment=Environment, 
         VpcConfig=VpcConfig, 
         Events=Events, 
         Tags=Tags, 
         Tracing=Tracing, 
         KmsKeyArn=KmsKeyArn, 
         DeadLetterQueue=DeadLetterQueue, 
         DeploymentPreference=DeploymentPreference, 
         Layers=Layers, 
         AutoPublishAlias=AutoPublishAlias, 
         ReservedConcurrentExecutions=ReservedConcurrentExecutions, **kwargs)
        (super(Function, self).__init__)(**processed_kwargs)


class CognitoAuthIdentity(troposphere.serverless.CognitoAuthIdentity, Mixin):

    def __init__(self, title=None, Header=NOTHING, ValidationExpression=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Header=Header, 
         ValidationExpression=ValidationExpression, **kwargs)
        (super(CognitoAuthIdentity, self).__init__)(**processed_kwargs)


class LambdaTokenAuthIdentity(troposphere.serverless.LambdaTokenAuthIdentity, Mixin):

    def __init__(self, title=None, Header=NOTHING, ValidationExpression=NOTHING, ReauthorizeEvery=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Header=Header, 
         ValidationExpression=ValidationExpression, 
         ReauthorizeEvery=ReauthorizeEvery, **kwargs)
        (super(LambdaTokenAuthIdentity, self).__init__)(**processed_kwargs)


class LambdaRequestAuthIdentity(troposphere.serverless.LambdaRequestAuthIdentity, Mixin):

    def __init__(self, title=None, Headers=NOTHING, QueryStrings=NOTHING, StageVariables=NOTHING, Context=NOTHING, ReauthorizeEvery=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Headers=Headers, 
         QueryStrings=QueryStrings, 
         StageVariables=StageVariables, 
         Context=Context, 
         ReauthorizeEvery=ReauthorizeEvery, **kwargs)
        (super(LambdaRequestAuthIdentity, self).__init__)(**processed_kwargs)


class CognitoAuth(troposphere.serverless.CognitoAuth, Mixin):

    def __init__(self, title=None, UserPoolArn=NOTHING, Identity=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         UserPoolArn=UserPoolArn, 
         Identity=Identity, **kwargs)
        (super(CognitoAuth, self).__init__)(**processed_kwargs)


class LambdaTokenAuth(troposphere.serverless.LambdaTokenAuth, Mixin):

    def __init__(self, title=None, FunctionPayloadType=NOTHING, FunctionArn=NOTHING, FunctionInvokeRole=NOTHING, Identity=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FunctionPayloadType=FunctionPayloadType, 
         FunctionArn=FunctionArn, 
         FunctionInvokeRole=FunctionInvokeRole, 
         Identity=Identity, **kwargs)
        (super(LambdaTokenAuth, self).__init__)(**processed_kwargs)


class LambdaRequestAuth(troposphere.serverless.LambdaRequestAuth, Mixin):

    def __init__(self, title=None, FunctionPayloadType=NOTHING, FunctionArn=NOTHING, FunctionInvokeRole=NOTHING, Identity=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FunctionPayloadType=FunctionPayloadType, 
         FunctionArn=FunctionArn, 
         FunctionInvokeRole=FunctionInvokeRole, 
         Identity=Identity, **kwargs)
        (super(LambdaRequestAuth, self).__init__)(**processed_kwargs)


class Authorizers(troposphere.serverless.Authorizers, Mixin):

    def __init__(self, title=None, DefaultAuthorizer=NOTHING, CognitoAuth=NOTHING, LambdaTokenAuth=NOTHING, LambdaRequestAuth=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DefaultAuthorizer=DefaultAuthorizer, 
         CognitoAuth=CognitoAuth, 
         LambdaTokenAuth=LambdaTokenAuth, 
         LambdaRequestAuth=LambdaRequestAuth, **kwargs)
        (super(Authorizers, self).__init__)(**processed_kwargs)


class Auth(troposphere.serverless.Auth, Mixin):

    def __init__(self, title=None, DefaultAuthorizer=NOTHING, Authorizers=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DefaultAuthorizer=DefaultAuthorizer, 
         Authorizers=Authorizers, **kwargs)
        (super(Auth, self).__init__)(**processed_kwargs)


class Cors(troposphere.serverless.Cors, Mixin):

    def __init__(self, title=None, AllowOrigin=REQUIRED, AllowCredentials=NOTHING, AllowHeaders=NOTHING, AllowMethods=NOTHING, MaxAge=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AllowOrigin=AllowOrigin, 
         AllowCredentials=AllowCredentials, 
         AllowHeaders=AllowHeaders, 
         AllowMethods=AllowMethods, 
         MaxAge=MaxAge, **kwargs)
        (super(Cors, self).__init__)(**processed_kwargs)


class Api(troposphere.serverless.Api, Mixin):

    def __init__(self, title, template=None, validation=True, StageName=REQUIRED, AccessLogSetting=NOTHING, Auth=NOTHING, BinaryMediaTypes=NOTHING, CacheClusterEnabled=NOTHING, CacheClusterSize=NOTHING, CanarySetting=NOTHING, Cors=NOTHING, DefinitionBody=NOTHING, DefinitionUri=NOTHING, EndpointConfiguration=NOTHING, MethodSettings=NOTHING, Name=NOTHING, TracingEnabled=NOTHING, Variables=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         StageName=StageName, 
         AccessLogSetting=AccessLogSetting, 
         Auth=Auth, 
         BinaryMediaTypes=BinaryMediaTypes, 
         CacheClusterEnabled=CacheClusterEnabled, 
         CacheClusterSize=CacheClusterSize, 
         CanarySetting=CanarySetting, 
         Cors=Cors, 
         DefinitionBody=DefinitionBody, 
         DefinitionUri=DefinitionUri, 
         EndpointConfiguration=EndpointConfiguration, 
         MethodSettings=MethodSettings, 
         Name=Name, 
         TracingEnabled=TracingEnabled, 
         Variables=Variables, **kwargs)
        (super(Api, self).__init__)(**processed_kwargs)


class PrimaryKey(troposphere.serverless.PrimaryKey, Mixin):

    def __init__(self, title=None, Name=NOTHING, Type=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Type=Type, **kwargs)
        (super(PrimaryKey, self).__init__)(**processed_kwargs)


class SimpleTable(troposphere.serverless.SimpleTable, Mixin):

    def __init__(self, title, template=None, validation=True, PrimaryKey=NOTHING, ProvisionedThroughput=NOTHING, SSESpecification=NOTHING, Tags=NOTHING, TableName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PrimaryKey=PrimaryKey, 
         ProvisionedThroughput=ProvisionedThroughput, 
         SSESpecification=SSESpecification, 
         Tags=Tags, 
         TableName=TableName, **kwargs)
        (super(SimpleTable, self).__init__)(**processed_kwargs)


class LayerVersion(troposphere.serverless.LayerVersion, Mixin):

    def __init__(self, title, template=None, validation=True, ContentUri=REQUIRED, CompatibleRuntimes=NOTHING, Description=NOTHING, LayerName=NOTHING, LicenseInfo=NOTHING, RetentionPolicy=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ContentUri=ContentUri, 
         CompatibleRuntimes=CompatibleRuntimes, 
         Description=Description, 
         LayerName=LayerName, 
         LicenseInfo=LicenseInfo, 
         RetentionPolicy=RetentionPolicy, **kwargs)
        (super(LayerVersion, self).__init__)(**processed_kwargs)


class S3Event(troposphere.serverless.S3Event, Mixin):

    def __init__(self, title, template=None, validation=True, Bucket=REQUIRED, Events=REQUIRED, Filter=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Bucket=Bucket, 
         Events=Events, 
         Filter=Filter, **kwargs)
        (super(S3Event, self).__init__)(**processed_kwargs)


class SNSEvent(troposphere.serverless.SNSEvent, Mixin):

    def __init__(self, title, template=None, validation=True, Topic=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Topic=Topic, **kwargs)
        (super(SNSEvent, self).__init__)(**processed_kwargs)


class KinesisEvent(troposphere.serverless.KinesisEvent, Mixin):

    def __init__(self, title, template=None, validation=True, Stream=REQUIRED, StartingPosition=REQUIRED, BatchSize=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Stream=Stream, 
         StartingPosition=StartingPosition, 
         BatchSize=BatchSize, **kwargs)
        (super(KinesisEvent, self).__init__)(**processed_kwargs)


class DynamoDBEvent(troposphere.serverless.DynamoDBEvent, Mixin):

    def __init__(self, title, template=None, validation=True, Stream=REQUIRED, StartingPosition=REQUIRED, BatchSize=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Stream=Stream, 
         StartingPosition=StartingPosition, 
         BatchSize=BatchSize, **kwargs)
        (super(DynamoDBEvent, self).__init__)(**processed_kwargs)


class ApiEvent(troposphere.serverless.ApiEvent, Mixin):

    def __init__(self, title, template=None, validation=True, Path=REQUIRED, Method=REQUIRED, RestApiId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Path=Path, 
         Method=Method, 
         RestApiId=RestApiId, **kwargs)
        (super(ApiEvent, self).__init__)(**processed_kwargs)


class ScheduleEvent(troposphere.serverless.ScheduleEvent, Mixin):

    def __init__(self, title, template=None, validation=True, Schedule=REQUIRED, Input=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Schedule=Schedule, 
         Input=Input, **kwargs)
        (super(ScheduleEvent, self).__init__)(**processed_kwargs)


class CloudWatchEvent(troposphere.serverless.CloudWatchEvent, Mixin):

    def __init__(self, title, template=None, validation=True, Pattern=REQUIRED, Input=NOTHING, InputPath=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Pattern=Pattern, 
         Input=Input, 
         InputPath=InputPath, **kwargs)
        (super(CloudWatchEvent, self).__init__)(**processed_kwargs)


class IoTRuleEvent(troposphere.serverless.IoTRuleEvent, Mixin):

    def __init__(self, title, template=None, validation=True, Sql=REQUIRED, AwsIotSqlVersion=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Sql=Sql, 
         AwsIotSqlVersion=AwsIotSqlVersion, **kwargs)
        (super(IoTRuleEvent, self).__init__)(**processed_kwargs)


class AlexaSkillEvent(troposphere.serverless.AlexaSkillEvent, Mixin):

    def __init__(self, title, template=None, validation=True, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, **kwargs)
        (super(AlexaSkillEvent, self).__init__)(**processed_kwargs)


class SQSEvent(troposphere.serverless.SQSEvent, Mixin):

    def __init__(self, title, template=None, validation=True, Queue=REQUIRED, BatchSize=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Queue=Queue, 
         BatchSize=BatchSize, **kwargs)
        (super(SQSEvent, self).__init__)(**processed_kwargs)