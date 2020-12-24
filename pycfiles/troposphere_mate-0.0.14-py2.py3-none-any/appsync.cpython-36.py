# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/appsync.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 21640 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.appsync
from troposphere.appsync import AdditionalAuthenticationProvider as _AdditionalAuthenticationProvider, AuthorizationConfig as _AuthorizationConfig, AwsIamConfig as _AwsIamConfig, CachingConfig as _CachingConfig, CognitoUserPoolConfig as _CognitoUserPoolConfig, DeltaSyncConfig as _DeltaSyncConfig, DynamoDBConfig as _DynamoDBConfig, ElasticsearchConfig as _ElasticsearchConfig, HttpConfig as _HttpConfig, LambdaConfig as _LambdaConfig, LambdaConflictHandlerConfig as _LambdaConflictHandlerConfig, LogConfig as _LogConfig, OpenIDConnectConfig as _OpenIDConnectConfig, PipelineConfig as _PipelineConfig, RdsHttpEndpointConfig as _RdsHttpEndpointConfig, RelationalDatabaseConfig as _RelationalDatabaseConfig, SyncConfig as _SyncConfig, Tags as _Tags, UserPoolConfig as _UserPoolConfig
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class ApiCache(troposphere.appsync.ApiCache, Mixin):

    def __init__(self, title, template=None, validation=True, ApiCachingBehavior=REQUIRED, ApiId=REQUIRED, Ttl=REQUIRED, Type=REQUIRED, AtRestEncryptionEnabled=NOTHING, TransitEncryptionEnabled=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiCachingBehavior=ApiCachingBehavior, 
         ApiId=ApiId, 
         Ttl=Ttl, 
         Type=Type, 
         AtRestEncryptionEnabled=AtRestEncryptionEnabled, 
         TransitEncryptionEnabled=TransitEncryptionEnabled, **kwargs)
        (super(ApiCache, self).__init__)(**processed_kwargs)


class ApiKey(troposphere.appsync.ApiKey, Mixin):

    def __init__(self, title, template=None, validation=True, ApiId=REQUIRED, Description=NOTHING, Expires=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiId=ApiId, 
         Description=Description, 
         Expires=Expires, **kwargs)
        (super(ApiKey, self).__init__)(**processed_kwargs)


class DeltaSyncConfig(troposphere.appsync.DeltaSyncConfig, Mixin):

    def __init__(self, title=None, BaseTableTTL=REQUIRED, DeltaSyncTableName=REQUIRED, DeltaSyncTableTTL=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BaseTableTTL=BaseTableTTL, 
         DeltaSyncTableName=DeltaSyncTableName, 
         DeltaSyncTableTTL=DeltaSyncTableTTL, **kwargs)
        (super(DeltaSyncConfig, self).__init__)(**processed_kwargs)


class DynamoDBConfig(troposphere.appsync.DynamoDBConfig, Mixin):

    def __init__(self, title=None, AwsRegion=REQUIRED, TableName=REQUIRED, DeltaSyncConfig=NOTHING, UseCallerCredentials=NOTHING, Versioned=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AwsRegion=AwsRegion, 
         TableName=TableName, 
         DeltaSyncConfig=DeltaSyncConfig, 
         UseCallerCredentials=UseCallerCredentials, 
         Versioned=Versioned, **kwargs)
        (super(DynamoDBConfig, self).__init__)(**processed_kwargs)


class ElasticsearchConfig(troposphere.appsync.ElasticsearchConfig, Mixin):

    def __init__(self, title=None, AwsRegion=REQUIRED, Endpoint=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AwsRegion=AwsRegion, 
         Endpoint=Endpoint, **kwargs)
        (super(ElasticsearchConfig, self).__init__)(**processed_kwargs)


class AwsIamConfig(troposphere.appsync.AwsIamConfig, Mixin):

    def __init__(self, title=None, SigningRegion=NOTHING, SigningServiceName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SigningRegion=SigningRegion, 
         SigningServiceName=SigningServiceName, **kwargs)
        (super(AwsIamConfig, self).__init__)(**processed_kwargs)


class AuthorizationConfig(troposphere.appsync.AuthorizationConfig, Mixin):

    def __init__(self, title=None, AuthorizationType=REQUIRED, AwsIamConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AuthorizationType=AuthorizationType, 
         AwsIamConfig=AwsIamConfig, **kwargs)
        (super(AuthorizationConfig, self).__init__)(**processed_kwargs)


class HttpConfig(troposphere.appsync.HttpConfig, Mixin):

    def __init__(self, title=None, Endpoint=REQUIRED, AuthorizationConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Endpoint=Endpoint, 
         AuthorizationConfig=AuthorizationConfig, **kwargs)
        (super(HttpConfig, self).__init__)(**processed_kwargs)


class LambdaConfig(troposphere.appsync.LambdaConfig, Mixin):

    def __init__(self, title=None, LambdaFunctionArn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LambdaFunctionArn=LambdaFunctionArn, **kwargs)
        (super(LambdaConfig, self).__init__)(**processed_kwargs)


class RdsHttpEndpointConfig(troposphere.appsync.RdsHttpEndpointConfig, Mixin):

    def __init__(self, title=None, AwsRegion=REQUIRED, AwsSecretStoreArn=REQUIRED, DbClusterIdentifier=REQUIRED, DatabaseName=NOTHING, Schema=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AwsRegion=AwsRegion, 
         AwsSecretStoreArn=AwsSecretStoreArn, 
         DbClusterIdentifier=DbClusterIdentifier, 
         DatabaseName=DatabaseName, 
         Schema=Schema, **kwargs)
        (super(RdsHttpEndpointConfig, self).__init__)(**processed_kwargs)


class RelationalDatabaseConfig(troposphere.appsync.RelationalDatabaseConfig, Mixin):

    def __init__(self, title=None, RelationalDatasourceType=REQUIRED, RdsHttpEndpointConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RelationalDatasourceType=RelationalDatasourceType, 
         RdsHttpEndpointConfig=RdsHttpEndpointConfig, **kwargs)
        (super(RelationalDatabaseConfig, self).__init__)(**processed_kwargs)


class DataSource(troposphere.appsync.DataSource, Mixin):

    def __init__(self, title, template=None, validation=True, ApiId=REQUIRED, Name=REQUIRED, Type=REQUIRED, Description=NOTHING, DynamoDBConfig=NOTHING, ElasticsearchConfig=NOTHING, HttpConfig=NOTHING, LambdaConfig=NOTHING, RelationalDatabaseConfig=NOTHING, ServiceRoleArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiId=ApiId, 
         Name=Name, 
         Type=Type, 
         Description=Description, 
         DynamoDBConfig=DynamoDBConfig, 
         ElasticsearchConfig=ElasticsearchConfig, 
         HttpConfig=HttpConfig, 
         LambdaConfig=LambdaConfig, 
         RelationalDatabaseConfig=RelationalDatabaseConfig, 
         ServiceRoleArn=ServiceRoleArn, **kwargs)
        (super(DataSource, self).__init__)(**processed_kwargs)


class FunctionConfiguration(troposphere.appsync.FunctionConfiguration, Mixin):

    def __init__(self, title, template=None, validation=True, ApiId=REQUIRED, DataSourceName=REQUIRED, FunctionVersion=REQUIRED, Name=REQUIRED, Description=NOTHING, RequestMappingTemplate=NOTHING, RequestMappingTemplateS3Location=NOTHING, ResponseMappingTemplate=NOTHING, ResponseMappingTemplateS3Location=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiId=ApiId, 
         DataSourceName=DataSourceName, 
         FunctionVersion=FunctionVersion, 
         Name=Name, 
         Description=Description, 
         RequestMappingTemplate=RequestMappingTemplate, 
         RequestMappingTemplateS3Location=RequestMappingTemplateS3Location, 
         ResponseMappingTemplate=ResponseMappingTemplate, 
         ResponseMappingTemplateS3Location=ResponseMappingTemplateS3Location, **kwargs)
        (super(FunctionConfiguration, self).__init__)(**processed_kwargs)


class CognitoUserPoolConfig(troposphere.appsync.CognitoUserPoolConfig, Mixin):

    def __init__(self, title=None, AppIdClientRegex=NOTHING, AwsRegion=NOTHING, UserPoolId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AppIdClientRegex=AppIdClientRegex, 
         AwsRegion=AwsRegion, 
         UserPoolId=UserPoolId, **kwargs)
        (super(CognitoUserPoolConfig, self).__init__)(**processed_kwargs)


class OpenIDConnectConfig(troposphere.appsync.OpenIDConnectConfig, Mixin):

    def __init__(self, title=None, AuthTTL=NOTHING, ClientId=NOTHING, IatTTL=NOTHING, Issuer=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AuthTTL=AuthTTL, 
         ClientId=ClientId, 
         IatTTL=IatTTL, 
         Issuer=Issuer, **kwargs)
        (super(OpenIDConnectConfig, self).__init__)(**processed_kwargs)


class AdditionalAuthenticationProvider(troposphere.appsync.AdditionalAuthenticationProvider, Mixin):

    def __init__(self, title=None, AuthenticationType=REQUIRED, OpenIDConnectConfig=NOTHING, UserPoolConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AuthenticationType=AuthenticationType, 
         OpenIDConnectConfig=OpenIDConnectConfig, 
         UserPoolConfig=UserPoolConfig, **kwargs)
        (super(AdditionalAuthenticationProvider, self).__init__)(**processed_kwargs)


class LogConfig(troposphere.appsync.LogConfig, Mixin):

    def __init__(self, title=None, CloudWatchLogsRoleArn=NOTHING, ExcludeVerboseContent=NOTHING, FieldLogLevel=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CloudWatchLogsRoleArn=CloudWatchLogsRoleArn, 
         ExcludeVerboseContent=ExcludeVerboseContent, 
         FieldLogLevel=FieldLogLevel, **kwargs)
        (super(LogConfig, self).__init__)(**processed_kwargs)


class UserPoolConfig(troposphere.appsync.UserPoolConfig, Mixin):

    def __init__(self, title=None, AppIdClientRegex=NOTHING, AwsRegion=NOTHING, DefaultAction=NOTHING, UserPoolId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AppIdClientRegex=AppIdClientRegex, 
         AwsRegion=AwsRegion, 
         DefaultAction=DefaultAction, 
         UserPoolId=UserPoolId, **kwargs)
        (super(UserPoolConfig, self).__init__)(**processed_kwargs)


class GraphQLApi(troposphere.appsync.GraphQLApi, Mixin):

    def __init__(self, title, template=None, validation=True, AuthenticationType=REQUIRED, Name=REQUIRED, AdditionalAuthenticationProviders=NOTHING, LogConfig=NOTHING, OpenIDConnectConfig=NOTHING, Tags=NOTHING, UserPoolConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AuthenticationType=AuthenticationType, 
         Name=Name, 
         AdditionalAuthenticationProviders=AdditionalAuthenticationProviders, 
         LogConfig=LogConfig, 
         OpenIDConnectConfig=OpenIDConnectConfig, 
         Tags=Tags, 
         UserPoolConfig=UserPoolConfig, **kwargs)
        (super(GraphQLApi, self).__init__)(**processed_kwargs)


class GraphQLSchema(troposphere.appsync.GraphQLSchema, Mixin):

    def __init__(self, title, template=None, validation=True, ApiId=REQUIRED, Definition=NOTHING, DefinitionS3Location=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiId=ApiId, 
         Definition=Definition, 
         DefinitionS3Location=DefinitionS3Location, **kwargs)
        (super(GraphQLSchema, self).__init__)(**processed_kwargs)


class CachingConfig(troposphere.appsync.CachingConfig, Mixin):

    def __init__(self, title=None, CachingKeys=NOTHING, Ttl=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CachingKeys=CachingKeys, 
         Ttl=Ttl, **kwargs)
        (super(CachingConfig, self).__init__)(**processed_kwargs)


class PipelineConfig(troposphere.appsync.PipelineConfig, Mixin):

    def __init__(self, title=None, Functions=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Functions=Functions, **kwargs)
        (super(PipelineConfig, self).__init__)(**processed_kwargs)


class LambdaConflictHandlerConfig(troposphere.appsync.LambdaConflictHandlerConfig, Mixin):

    def __init__(self, title=None, LambdaConflictHandlerArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LambdaConflictHandlerArn=LambdaConflictHandlerArn, **kwargs)
        (super(LambdaConflictHandlerConfig, self).__init__)(**processed_kwargs)


class SyncConfig(troposphere.appsync.SyncConfig, Mixin):

    def __init__(self, title=None, ConflictDetection=REQUIRED, ConflictHandler=NOTHING, LambdaConflictHandlerConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ConflictDetection=ConflictDetection, 
         ConflictHandler=ConflictHandler, 
         LambdaConflictHandlerConfig=LambdaConflictHandlerConfig, **kwargs)
        (super(SyncConfig, self).__init__)(**processed_kwargs)


class Resolver(troposphere.appsync.Resolver, Mixin):

    def __init__(self, title, template=None, validation=True, ApiId=REQUIRED, FieldName=REQUIRED, TypeName=REQUIRED, CachingConfig=NOTHING, DataSourceName=NOTHING, Kind=NOTHING, PipelineConfig=NOTHING, RequestMappingTemplate=NOTHING, RequestMappingTemplateS3Location=NOTHING, ResponseMappingTemplate=NOTHING, ResponseMappingTemplateS3Location=NOTHING, SyncConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiId=ApiId, 
         FieldName=FieldName, 
         TypeName=TypeName, 
         CachingConfig=CachingConfig, 
         DataSourceName=DataSourceName, 
         Kind=Kind, 
         PipelineConfig=PipelineConfig, 
         RequestMappingTemplate=RequestMappingTemplate, 
         RequestMappingTemplateS3Location=RequestMappingTemplateS3Location, 
         ResponseMappingTemplate=ResponseMappingTemplate, 
         ResponseMappingTemplateS3Location=ResponseMappingTemplateS3Location, 
         SyncConfig=SyncConfig, **kwargs)
        (super(Resolver, self).__init__)(**processed_kwargs)