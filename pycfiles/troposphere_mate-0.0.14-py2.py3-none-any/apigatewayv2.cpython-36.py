# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/apigatewayv2.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 20113 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.apigatewayv2
from troposphere.apigatewayv2 import AccessLogSettings as _AccessLogSettings, BodyS3Location as _BodyS3Location, Cors as _Cors, DomainNameConfiguration as _DomainNameConfiguration, JWTConfiguration as _JWTConfiguration, RouteSettings as _RouteSettings
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class BodyS3Location(troposphere.apigatewayv2.BodyS3Location, Mixin):

    def __init__(self, title=None, Bucket=NOTHING, Etag=NOTHING, Key=NOTHING, Version=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Bucket=Bucket, 
         Etag=Etag, 
         Key=Key, 
         Version=Version, **kwargs)
        (super(BodyS3Location, self).__init__)(**processed_kwargs)


class Cors(troposphere.apigatewayv2.Cors, Mixin):

    def __init__(self, title=None, AllowCredentials=NOTHING, AllowHeaders=NOTHING, AllowMethods=NOTHING, AllowOrigins=NOTHING, ExposeHeaders=NOTHING, MaxAge=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AllowCredentials=AllowCredentials, 
         AllowHeaders=AllowHeaders, 
         AllowMethods=AllowMethods, 
         AllowOrigins=AllowOrigins, 
         ExposeHeaders=ExposeHeaders, 
         MaxAge=MaxAge, **kwargs)
        (super(Cors, self).__init__)(**processed_kwargs)


class Api(troposphere.apigatewayv2.Api, Mixin):

    def __init__(self, title, template=None, validation=True, ApiKeySelectionExpression=NOTHING, BasePath=NOTHING, Body=NOTHING, BodyS3Location=NOTHING, CorsConfiguration=NOTHING, CredentialsArn=NOTHING, Description=NOTHING, DisableSchemaValidation=NOTHING, FailOnWarnings=NOTHING, Name=NOTHING, ProtocolType=NOTHING, RouteKey=NOTHING, RouteSelectionExpression=NOTHING, Tags=NOTHING, Target=NOTHING, Version=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiKeySelectionExpression=ApiKeySelectionExpression, 
         BasePath=BasePath, 
         Body=Body, 
         BodyS3Location=BodyS3Location, 
         CorsConfiguration=CorsConfiguration, 
         CredentialsArn=CredentialsArn, 
         Description=Description, 
         DisableSchemaValidation=DisableSchemaValidation, 
         FailOnWarnings=FailOnWarnings, 
         Name=Name, 
         ProtocolType=ProtocolType, 
         RouteKey=RouteKey, 
         RouteSelectionExpression=RouteSelectionExpression, 
         Tags=Tags, 
         Target=Target, 
         Version=Version, **kwargs)
        (super(Api, self).__init__)(**processed_kwargs)


class ApiMapping(troposphere.apigatewayv2.ApiMapping, Mixin):

    def __init__(self, title, template=None, validation=True, ApiId=REQUIRED, DomainName=REQUIRED, Stage=REQUIRED, ApiMappingKey=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiId=ApiId, 
         DomainName=DomainName, 
         Stage=Stage, 
         ApiMappingKey=ApiMappingKey, **kwargs)
        (super(ApiMapping, self).__init__)(**processed_kwargs)


class JWTConfiguration(troposphere.apigatewayv2.JWTConfiguration, Mixin):

    def __init__(self, title=None, Audience=NOTHING, Issuer=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Audience=Audience, 
         Issuer=Issuer, **kwargs)
        (super(JWTConfiguration, self).__init__)(**processed_kwargs)


class Authorizer(troposphere.apigatewayv2.Authorizer, Mixin):

    def __init__(self, title, template=None, validation=True, ApiId=REQUIRED, AuthorizerType=REQUIRED, IdentitySource=REQUIRED, Name=REQUIRED, AuthorizerCredentialsArn=NOTHING, AuthorizerResultTtlInSeconds=NOTHING, AuthorizerUri=NOTHING, IdentityValidationExpression=NOTHING, JwtConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiId=ApiId, 
         AuthorizerType=AuthorizerType, 
         IdentitySource=IdentitySource, 
         Name=Name, 
         AuthorizerCredentialsArn=AuthorizerCredentialsArn, 
         AuthorizerResultTtlInSeconds=AuthorizerResultTtlInSeconds, 
         AuthorizerUri=AuthorizerUri, 
         IdentityValidationExpression=IdentityValidationExpression, 
         JwtConfiguration=JwtConfiguration, **kwargs)
        (super(Authorizer, self).__init__)(**processed_kwargs)


class Deployment(troposphere.apigatewayv2.Deployment, Mixin):

    def __init__(self, title, template=None, validation=True, ApiId=REQUIRED, Description=NOTHING, StageName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiId=ApiId, 
         Description=Description, 
         StageName=StageName, **kwargs)
        (super(Deployment, self).__init__)(**processed_kwargs)


class DomainNameConfiguration(troposphere.apigatewayv2.DomainNameConfiguration, Mixin):

    def __init__(self, title=None, CertificateArn=NOTHING, CertificateName=NOTHING, EndpointType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CertificateArn=CertificateArn, 
         CertificateName=CertificateName, 
         EndpointType=EndpointType, **kwargs)
        (super(DomainNameConfiguration, self).__init__)(**processed_kwargs)


class DomainName(troposphere.apigatewayv2.DomainName, Mixin):

    def __init__(self, title, template=None, validation=True, DomainName=REQUIRED, DomainNameConfigurations=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DomainName=DomainName, 
         DomainNameConfigurations=DomainNameConfigurations, 
         Tags=Tags, **kwargs)
        (super(DomainName, self).__init__)(**processed_kwargs)


class Integration(troposphere.apigatewayv2.Integration, Mixin):

    def __init__(self, title, template=None, validation=True, ApiId=REQUIRED, IntegrationType=REQUIRED, ConnectionType=NOTHING, ContentHandlingStrategy=NOTHING, CredentialsArn=NOTHING, Description=NOTHING, IntegrationMethod=NOTHING, IntegrationUri=NOTHING, PassthroughBehavior=NOTHING, PayloadFormatVersion=NOTHING, RequestParameters=NOTHING, RequestTemplates=NOTHING, TemplateSelectionExpression=NOTHING, TimeoutInMillis=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiId=ApiId, 
         IntegrationType=IntegrationType, 
         ConnectionType=ConnectionType, 
         ContentHandlingStrategy=ContentHandlingStrategy, 
         CredentialsArn=CredentialsArn, 
         Description=Description, 
         IntegrationMethod=IntegrationMethod, 
         IntegrationUri=IntegrationUri, 
         PassthroughBehavior=PassthroughBehavior, 
         PayloadFormatVersion=PayloadFormatVersion, 
         RequestParameters=RequestParameters, 
         RequestTemplates=RequestTemplates, 
         TemplateSelectionExpression=TemplateSelectionExpression, 
         TimeoutInMillis=TimeoutInMillis, **kwargs)
        (super(Integration, self).__init__)(**processed_kwargs)


class IntegrationResponse(troposphere.apigatewayv2.IntegrationResponse, Mixin):

    def __init__(self, title, template=None, validation=True, ApiId=REQUIRED, IntegrationId=REQUIRED, IntegrationResponseKey=REQUIRED, ContentHandlingStrategy=NOTHING, ResponseParameters=NOTHING, ResponseTemplates=NOTHING, TemplateSelectionExpression=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiId=ApiId, 
         IntegrationId=IntegrationId, 
         IntegrationResponseKey=IntegrationResponseKey, 
         ContentHandlingStrategy=ContentHandlingStrategy, 
         ResponseParameters=ResponseParameters, 
         ResponseTemplates=ResponseTemplates, 
         TemplateSelectionExpression=TemplateSelectionExpression, **kwargs)
        (super(IntegrationResponse, self).__init__)(**processed_kwargs)


class Model(troposphere.apigatewayv2.Model, Mixin):

    def __init__(self, title, template=None, validation=True, ApiId=REQUIRED, Name=REQUIRED, Schema=REQUIRED, ContentType=NOTHING, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiId=ApiId, 
         Name=Name, 
         Schema=Schema, 
         ContentType=ContentType, 
         Description=Description, **kwargs)
        (super(Model, self).__init__)(**processed_kwargs)


class Route(troposphere.apigatewayv2.Route, Mixin):

    def __init__(self, title, template=None, validation=True, ApiId=REQUIRED, RouteKey=REQUIRED, ApiKeyRequired=NOTHING, AuthorizationScopes=NOTHING, AuthorizationType=NOTHING, AuthorizerId=NOTHING, ModelSelectionExpression=NOTHING, OperationName=NOTHING, RequestModels=NOTHING, RequestParameters=NOTHING, RouteResponseSelectionExpression=NOTHING, Target=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiId=ApiId, 
         RouteKey=RouteKey, 
         ApiKeyRequired=ApiKeyRequired, 
         AuthorizationScopes=AuthorizationScopes, 
         AuthorizationType=AuthorizationType, 
         AuthorizerId=AuthorizerId, 
         ModelSelectionExpression=ModelSelectionExpression, 
         OperationName=OperationName, 
         RequestModels=RequestModels, 
         RequestParameters=RequestParameters, 
         RouteResponseSelectionExpression=RouteResponseSelectionExpression, 
         Target=Target, **kwargs)
        (super(Route, self).__init__)(**processed_kwargs)


class RouteResponse(troposphere.apigatewayv2.RouteResponse, Mixin):

    def __init__(self, title, template=None, validation=True, ApiId=REQUIRED, RouteId=REQUIRED, RouteResponseKey=REQUIRED, ModelSelectionExpression=NOTHING, ResponseModels=NOTHING, ResponseParameters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiId=ApiId, 
         RouteId=RouteId, 
         RouteResponseKey=RouteResponseKey, 
         ModelSelectionExpression=ModelSelectionExpression, 
         ResponseModels=ResponseModels, 
         ResponseParameters=ResponseParameters, **kwargs)
        (super(RouteResponse, self).__init__)(**processed_kwargs)


class AccessLogSettings(troposphere.apigatewayv2.AccessLogSettings, Mixin):

    def __init__(self, title=None, DestinationArn=NOTHING, Format=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DestinationArn=DestinationArn, 
         Format=Format, **kwargs)
        (super(AccessLogSettings, self).__init__)(**processed_kwargs)


class RouteSettings(troposphere.apigatewayv2.RouteSettings, Mixin):

    def __init__(self, title=None, DataTraceEnabled=NOTHING, DetailedMetricsEnabled=NOTHING, LoggingLevel=NOTHING, ThrottlingBurstLimit=NOTHING, ThrottlingRateLimit=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DataTraceEnabled=DataTraceEnabled, 
         DetailedMetricsEnabled=DetailedMetricsEnabled, 
         LoggingLevel=LoggingLevel, 
         ThrottlingBurstLimit=ThrottlingBurstLimit, 
         ThrottlingRateLimit=ThrottlingRateLimit, **kwargs)
        (super(RouteSettings, self).__init__)(**processed_kwargs)


class Stage(troposphere.apigatewayv2.Stage, Mixin):

    def __init__(self, title, template=None, validation=True, ApiId=REQUIRED, StageName=REQUIRED, AccessLogSettings=NOTHING, AutoDeploy=NOTHING, ClientCertificateId=NOTHING, DefaultRouteSettings=NOTHING, DeploymentId=NOTHING, Description=NOTHING, RouteSettings=NOTHING, StageVariables=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiId=ApiId, 
         StageName=StageName, 
         AccessLogSettings=AccessLogSettings, 
         AutoDeploy=AutoDeploy, 
         ClientCertificateId=ClientCertificateId, 
         DefaultRouteSettings=DefaultRouteSettings, 
         DeploymentId=DeploymentId, 
         Description=Description, 
         RouteSettings=RouteSettings, 
         StageVariables=StageVariables, 
         Tags=Tags, **kwargs)
        (super(Stage, self).__init__)(**processed_kwargs)