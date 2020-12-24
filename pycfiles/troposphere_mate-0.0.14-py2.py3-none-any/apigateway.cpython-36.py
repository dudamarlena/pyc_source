# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/apigateway.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 35034 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.apigateway
from troposphere.apigateway import AccessLogSetting as _AccessLogSetting, ApiStage as _ApiStage, CanarySetting as _CanarySetting, DeploymentCanarySettings as _DeploymentCanarySettings, EndpointConfiguration as _EndpointConfiguration, Integration as _Integration, IntegrationResponse as _IntegrationResponse, Location as _Location, MethodResponse as _MethodResponse, MethodSetting as _MethodSetting, QuotaSettings as _QuotaSettings, S3Location as _S3Location, StageDescription as _StageDescription, StageKey as _StageKey, Tags as _Tags, ThrottleSettings as _ThrottleSettings, double as _double
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class AccessLogSetting(troposphere.apigateway.AccessLogSetting, Mixin):

    def __init__(self, title=None, DestinationArn=NOTHING, Format=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DestinationArn=DestinationArn, 
         Format=Format, **kwargs)
        (super(AccessLogSetting, self).__init__)(**processed_kwargs)


class Account(troposphere.apigateway.Account, Mixin):

    def __init__(self, title, template=None, validation=True, CloudWatchRoleArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CloudWatchRoleArn=CloudWatchRoleArn, **kwargs)
        (super(Account, self).__init__)(**processed_kwargs)


class StageKey(troposphere.apigateway.StageKey, Mixin):

    def __init__(self, title=None, RestApiId=NOTHING, StageName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RestApiId=RestApiId, 
         StageName=StageName, **kwargs)
        (super(StageKey, self).__init__)(**processed_kwargs)


class ApiKey(troposphere.apigateway.ApiKey, Mixin):

    def __init__(self, title, template=None, validation=True, CustomerId=NOTHING, Description=NOTHING, Enabled=NOTHING, GenerateDistinctId=NOTHING, Name=NOTHING, StageKeys=NOTHING, Tags=NOTHING, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CustomerId=CustomerId, 
         Description=Description, 
         Enabled=Enabled, 
         GenerateDistinctId=GenerateDistinctId, 
         Name=Name, 
         StageKeys=StageKeys, 
         Tags=Tags, 
         Value=Value, **kwargs)
        (super(ApiKey, self).__init__)(**processed_kwargs)


class Authorizer(troposphere.apigateway.Authorizer, Mixin):

    def __init__(self, title, template=None, validation=True, AuthorizerUri=REQUIRED, IdentitySource=REQUIRED, Name=REQUIRED, Type=REQUIRED, AuthType=NOTHING, AuthorizerCredentials=NOTHING, AuthorizerResultTtlInSeconds=NOTHING, IdentityValidationExpression=NOTHING, ProviderARNs=NOTHING, RestApiId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AuthorizerUri=AuthorizerUri, 
         IdentitySource=IdentitySource, 
         Name=Name, 
         Type=Type, 
         AuthType=AuthType, 
         AuthorizerCredentials=AuthorizerCredentials, 
         AuthorizerResultTtlInSeconds=AuthorizerResultTtlInSeconds, 
         IdentityValidationExpression=IdentityValidationExpression, 
         ProviderARNs=ProviderARNs, 
         RestApiId=RestApiId, **kwargs)
        (super(Authorizer, self).__init__)(**processed_kwargs)


class BasePathMapping(troposphere.apigateway.BasePathMapping, Mixin):

    def __init__(self, title, template=None, validation=True, DomainName=REQUIRED, RestApiId=REQUIRED, BasePath=NOTHING, Stage=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DomainName=DomainName, 
         RestApiId=RestApiId, 
         BasePath=BasePath, 
         Stage=Stage, **kwargs)
        (super(BasePathMapping, self).__init__)(**processed_kwargs)


class CanarySetting(troposphere.apigateway.CanarySetting, Mixin):

    def __init__(self, title=None, DeploymentId=NOTHING, PercentTraffic=NOTHING, StageVariableOverrides=NOTHING, UseStageCache=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeploymentId=DeploymentId, 
         PercentTraffic=PercentTraffic, 
         StageVariableOverrides=StageVariableOverrides, 
         UseStageCache=UseStageCache, **kwargs)
        (super(CanarySetting, self).__init__)(**processed_kwargs)


class ClientCertificate(troposphere.apigateway.ClientCertificate, Mixin):

    def __init__(self, title, template=None, validation=True, Description=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         Tags=Tags, **kwargs)
        (super(ClientCertificate, self).__init__)(**processed_kwargs)


class DeploymentCanarySettings(troposphere.apigateway.DeploymentCanarySettings, Mixin):

    def __init__(self, title=None, PercentTraffic=NOTHING, StageVariableOverrides=NOTHING, UseStageCache=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PercentTraffic=PercentTraffic, 
         StageVariableOverrides=StageVariableOverrides, 
         UseStageCache=UseStageCache, **kwargs)
        (super(DeploymentCanarySettings, self).__init__)(**processed_kwargs)


class MethodSetting(troposphere.apigateway.MethodSetting, Mixin):

    def __init__(self, title=None, HttpMethod=REQUIRED, ResourcePath=REQUIRED, CacheDataEncrypted=NOTHING, CacheTtlInSeconds=NOTHING, CachingEnabled=NOTHING, DataTraceEnabled=NOTHING, LoggingLevel=NOTHING, MetricsEnabled=NOTHING, ThrottlingBurstLimit=NOTHING, ThrottlingRateLimit=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HttpMethod=HttpMethod, 
         ResourcePath=ResourcePath, 
         CacheDataEncrypted=CacheDataEncrypted, 
         CacheTtlInSeconds=CacheTtlInSeconds, 
         CachingEnabled=CachingEnabled, 
         DataTraceEnabled=DataTraceEnabled, 
         LoggingLevel=LoggingLevel, 
         MetricsEnabled=MetricsEnabled, 
         ThrottlingBurstLimit=ThrottlingBurstLimit, 
         ThrottlingRateLimit=ThrottlingRateLimit, **kwargs)
        (super(MethodSetting, self).__init__)(**processed_kwargs)


class StageDescription(troposphere.apigateway.StageDescription, Mixin):

    def __init__(self, title=None, AccessLogSetting=NOTHING, CacheClusterEnabled=NOTHING, CacheClusterSize=NOTHING, CacheDataEncrypted=NOTHING, CacheTtlInSeconds=NOTHING, CachingEnabled=NOTHING, CanarySetting=NOTHING, ClientCertificateId=NOTHING, DataTraceEnabled=NOTHING, Description=NOTHING, LoggingLevel=NOTHING, MethodSettings=NOTHING, MetricsEnabled=NOTHING, StageName=NOTHING, Tags=NOTHING, ThrottlingBurstLimit=NOTHING, ThrottlingRateLimit=NOTHING, Variables=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AccessLogSetting=AccessLogSetting, 
         CacheClusterEnabled=CacheClusterEnabled, 
         CacheClusterSize=CacheClusterSize, 
         CacheDataEncrypted=CacheDataEncrypted, 
         CacheTtlInSeconds=CacheTtlInSeconds, 
         CachingEnabled=CachingEnabled, 
         CanarySetting=CanarySetting, 
         ClientCertificateId=ClientCertificateId, 
         DataTraceEnabled=DataTraceEnabled, 
         Description=Description, 
         LoggingLevel=LoggingLevel, 
         MethodSettings=MethodSettings, 
         MetricsEnabled=MetricsEnabled, 
         StageName=StageName, 
         Tags=Tags, 
         ThrottlingBurstLimit=ThrottlingBurstLimit, 
         ThrottlingRateLimit=ThrottlingRateLimit, 
         Variables=Variables, **kwargs)
        (super(StageDescription, self).__init__)(**processed_kwargs)


class Deployment(troposphere.apigateway.Deployment, Mixin):

    def __init__(self, title, template=None, validation=True, RestApiId=REQUIRED, DeploymentCanarySettings=NOTHING, Description=NOTHING, StageDescription=NOTHING, StageName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         RestApiId=RestApiId, 
         DeploymentCanarySettings=DeploymentCanarySettings, 
         Description=Description, 
         StageDescription=StageDescription, 
         StageName=StageName, **kwargs)
        (super(Deployment, self).__init__)(**processed_kwargs)


class Location(troposphere.apigateway.Location, Mixin):

    def __init__(self, title=None, Method=NOTHING, Name=NOTHING, Path=NOTHING, StatusCode=NOTHING, Type=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Method=Method, 
         Name=Name, 
         Path=Path, 
         StatusCode=StatusCode, 
         Type=Type, **kwargs)
        (super(Location, self).__init__)(**processed_kwargs)


class DocumentationPart(troposphere.apigateway.DocumentationPart, Mixin):

    def __init__(self, title, template=None, validation=True, Location=REQUIRED, Properties=REQUIRED, RestApiId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Location=Location, 
         Properties=Properties, 
         RestApiId=RestApiId, **kwargs)
        (super(DocumentationPart, self).__init__)(**processed_kwargs)


class DocumentationVersion(troposphere.apigateway.DocumentationVersion, Mixin):

    def __init__(self, title, template=None, validation=True, DocumentationVersion=REQUIRED, RestApiId=REQUIRED, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DocumentationVersion=DocumentationVersion, 
         RestApiId=RestApiId, 
         Description=Description, **kwargs)
        (super(DocumentationVersion, self).__init__)(**processed_kwargs)


class EndpointConfiguration(troposphere.apigateway.EndpointConfiguration, Mixin):

    def __init__(self, title=None, Types=NOTHING, VpcEndpointIds=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Types=Types, 
         VpcEndpointIds=VpcEndpointIds, **kwargs)
        (super(EndpointConfiguration, self).__init__)(**processed_kwargs)


class DomainName(troposphere.apigateway.DomainName, Mixin):

    def __init__(self, title, template=None, validation=True, DomainName=REQUIRED, CertificateArn=NOTHING, EndpointConfiguration=NOTHING, RegionalCertificateArn=NOTHING, SecurityPolicy=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DomainName=DomainName, 
         CertificateArn=CertificateArn, 
         EndpointConfiguration=EndpointConfiguration, 
         RegionalCertificateArn=RegionalCertificateArn, 
         SecurityPolicy=SecurityPolicy, 
         Tags=Tags, **kwargs)
        (super(DomainName, self).__init__)(**processed_kwargs)


class IntegrationResponse(troposphere.apigateway.IntegrationResponse, Mixin):

    def __init__(self, title=None, ContentHandling=NOTHING, ResponseParameters=NOTHING, ResponseTemplates=NOTHING, SelectionPattern=NOTHING, StatusCode=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ContentHandling=ContentHandling, 
         ResponseParameters=ResponseParameters, 
         ResponseTemplates=ResponseTemplates, 
         SelectionPattern=SelectionPattern, 
         StatusCode=StatusCode, **kwargs)
        (super(IntegrationResponse, self).__init__)(**processed_kwargs)


class Integration(troposphere.apigateway.Integration, Mixin):

    def __init__(self, title=None, Type=REQUIRED, CacheKeyParameters=NOTHING, CacheNamespace=NOTHING, ConnectionId=NOTHING, ConnectionType=NOTHING, ContentHandling=NOTHING, Credentials=NOTHING, IntegrationHttpMethod=NOTHING, IntegrationResponses=NOTHING, PassthroughBehavior=NOTHING, RequestParameters=NOTHING, RequestTemplates=NOTHING, TimeoutInMillis=NOTHING, Uri=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         CacheKeyParameters=CacheKeyParameters, 
         CacheNamespace=CacheNamespace, 
         ConnectionId=ConnectionId, 
         ConnectionType=ConnectionType, 
         ContentHandling=ContentHandling, 
         Credentials=Credentials, 
         IntegrationHttpMethod=IntegrationHttpMethod, 
         IntegrationResponses=IntegrationResponses, 
         PassthroughBehavior=PassthroughBehavior, 
         RequestParameters=RequestParameters, 
         RequestTemplates=RequestTemplates, 
         TimeoutInMillis=TimeoutInMillis, 
         Uri=Uri, **kwargs)
        (super(Integration, self).__init__)(**processed_kwargs)


class MethodResponse(troposphere.apigateway.MethodResponse, Mixin):

    def __init__(self, title=None, StatusCode=REQUIRED, ResponseModels=NOTHING, ResponseParameters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         StatusCode=StatusCode, 
         ResponseModels=ResponseModels, 
         ResponseParameters=ResponseParameters, **kwargs)
        (super(MethodResponse, self).__init__)(**processed_kwargs)


class Method(troposphere.apigateway.Method, Mixin):

    def __init__(self, title, template=None, validation=True, AuthorizationType=REQUIRED, HttpMethod=REQUIRED, ResourceId=REQUIRED, RestApiId=REQUIRED, ApiKeyRequired=NOTHING, AuthorizationScopes=NOTHING, AuthorizerId=NOTHING, Integration=NOTHING, MethodResponses=NOTHING, OperationName=NOTHING, RequestModels=NOTHING, RequestParameters=NOTHING, RequestValidatorId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AuthorizationType=AuthorizationType, 
         HttpMethod=HttpMethod, 
         ResourceId=ResourceId, 
         RestApiId=RestApiId, 
         ApiKeyRequired=ApiKeyRequired, 
         AuthorizationScopes=AuthorizationScopes, 
         AuthorizerId=AuthorizerId, 
         Integration=Integration, 
         MethodResponses=MethodResponses, 
         OperationName=OperationName, 
         RequestModels=RequestModels, 
         RequestParameters=RequestParameters, 
         RequestValidatorId=RequestValidatorId, **kwargs)
        (super(Method, self).__init__)(**processed_kwargs)


class Model(troposphere.apigateway.Model, Mixin):

    def __init__(self, title, template=None, validation=True, RestApiId=REQUIRED, ContentType=NOTHING, Description=NOTHING, Name=NOTHING, Schema=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         RestApiId=RestApiId, 
         ContentType=ContentType, 
         Description=Description, 
         Name=Name, 
         Schema=Schema, **kwargs)
        (super(Model, self).__init__)(**processed_kwargs)


class RequestValidator(troposphere.apigateway.RequestValidator, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, RestApiId=REQUIRED, ValidateRequestBody=NOTHING, ValidateRequestParameters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         RestApiId=RestApiId, 
         ValidateRequestBody=ValidateRequestBody, 
         ValidateRequestParameters=ValidateRequestParameters, **kwargs)
        (super(RequestValidator, self).__init__)(**processed_kwargs)


class Resource(troposphere.apigateway.Resource, Mixin):

    def __init__(self, title, template=None, validation=True, ParentId=REQUIRED, PathPart=REQUIRED, RestApiId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ParentId=ParentId, 
         PathPart=PathPart, 
         RestApiId=RestApiId, **kwargs)
        (super(Resource, self).__init__)(**processed_kwargs)


class S3Location(troposphere.apigateway.S3Location, Mixin):

    def __init__(self, title=None, Bucket=NOTHING, ETag=NOTHING, Key=NOTHING, Version=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Bucket=Bucket, 
         ETag=ETag, 
         Key=Key, 
         Version=Version, **kwargs)
        (super(S3Location, self).__init__)(**processed_kwargs)


class RestApi(troposphere.apigateway.RestApi, Mixin):

    def __init__(self, title, template=None, validation=True, ApiKeySourceType=NOTHING, BinaryMediaTypes=NOTHING, Body=NOTHING, BodyS3Location=NOTHING, CloneFrom=NOTHING, Description=NOTHING, EndpointConfiguration=NOTHING, FailOnWarnings=NOTHING, MinimumCompressionSize=NOTHING, Name=NOTHING, Parameters=NOTHING, Policy=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiKeySourceType=ApiKeySourceType, 
         BinaryMediaTypes=BinaryMediaTypes, 
         Body=Body, 
         BodyS3Location=BodyS3Location, 
         CloneFrom=CloneFrom, 
         Description=Description, 
         EndpointConfiguration=EndpointConfiguration, 
         FailOnWarnings=FailOnWarnings, 
         MinimumCompressionSize=MinimumCompressionSize, 
         Name=Name, 
         Parameters=Parameters, 
         Policy=Policy, 
         Tags=Tags, **kwargs)
        (super(RestApi, self).__init__)(**processed_kwargs)


class Stage(troposphere.apigateway.Stage, Mixin):

    def __init__(self, title, template=None, validation=True, DeploymentId=REQUIRED, RestApiId=REQUIRED, StageName=REQUIRED, AccessLogSetting=NOTHING, CacheClusterEnabled=NOTHING, CacheClusterSize=NOTHING, CanarySetting=NOTHING, ClientCertificateId=NOTHING, Description=NOTHING, DocumentationVersion=NOTHING, MethodSettings=NOTHING, Tags=NOTHING, TracingEnabled=NOTHING, Variables=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DeploymentId=DeploymentId, 
         RestApiId=RestApiId, 
         StageName=StageName, 
         AccessLogSetting=AccessLogSetting, 
         CacheClusterEnabled=CacheClusterEnabled, 
         CacheClusterSize=CacheClusterSize, 
         CanarySetting=CanarySetting, 
         ClientCertificateId=ClientCertificateId, 
         Description=Description, 
         DocumentationVersion=DocumentationVersion, 
         MethodSettings=MethodSettings, 
         Tags=Tags, 
         TracingEnabled=TracingEnabled, 
         Variables=Variables, **kwargs)
        (super(Stage, self).__init__)(**processed_kwargs)


class QuotaSettings(troposphere.apigateway.QuotaSettings, Mixin):

    def __init__(self, title=None, Limit=NOTHING, Offset=NOTHING, Period=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Limit=Limit, 
         Offset=Offset, 
         Period=Period, **kwargs)
        (super(QuotaSettings, self).__init__)(**processed_kwargs)


class ThrottleSettings(troposphere.apigateway.ThrottleSettings, Mixin):

    def __init__(self, title=None, BurstLimit=NOTHING, RateLimit=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BurstLimit=BurstLimit, 
         RateLimit=RateLimit, **kwargs)
        (super(ThrottleSettings, self).__init__)(**processed_kwargs)


class ApiStage(troposphere.apigateway.ApiStage, Mixin):

    def __init__(self, title=None, ApiId=NOTHING, Stage=NOTHING, Throttle=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ApiId=ApiId, 
         Stage=Stage, 
         Throttle=Throttle, **kwargs)
        (super(ApiStage, self).__init__)(**processed_kwargs)


class UsagePlan(troposphere.apigateway.UsagePlan, Mixin):

    def __init__(self, title, template=None, validation=True, ApiStages=NOTHING, Description=NOTHING, Quota=NOTHING, Tags=NOTHING, Throttle=NOTHING, UsagePlanName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiStages=ApiStages, 
         Description=Description, 
         Quota=Quota, 
         Tags=Tags, 
         Throttle=Throttle, 
         UsagePlanName=UsagePlanName, **kwargs)
        (super(UsagePlan, self).__init__)(**processed_kwargs)


class UsagePlanKey(troposphere.apigateway.UsagePlanKey, Mixin):

    def __init__(self, title, template=None, validation=True, KeyId=REQUIRED, KeyType=REQUIRED, UsagePlanId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         KeyId=KeyId, 
         KeyType=KeyType, 
         UsagePlanId=UsagePlanId, **kwargs)
        (super(UsagePlanKey, self).__init__)(**processed_kwargs)


class GatewayResponse(troposphere.apigateway.GatewayResponse, Mixin):

    def __init__(self, title, template=None, validation=True, ResponseType=REQUIRED, RestApiId=REQUIRED, ResponseParameters=NOTHING, ResponseTemplates=NOTHING, StatusCode=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ResponseType=ResponseType, 
         RestApiId=RestApiId, 
         ResponseParameters=ResponseParameters, 
         ResponseTemplates=ResponseTemplates, 
         StatusCode=StatusCode, **kwargs)
        (super(GatewayResponse, self).__init__)(**processed_kwargs)


class VpcLink(troposphere.apigateway.VpcLink, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, TargetArns=REQUIRED, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         TargetArns=TargetArns, 
         Description=Description, **kwargs)
        (super(VpcLink, self).__init__)(**processed_kwargs)