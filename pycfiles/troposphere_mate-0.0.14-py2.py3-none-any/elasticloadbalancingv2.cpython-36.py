# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/elasticloadbalancingv2.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 20915 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.elasticloadbalancingv2
from troposphere.elasticloadbalancingv2 import Action as _Action, AuthenticateCognitoConfig as _AuthenticateCognitoConfig, AuthenticateOidcConfig as _AuthenticateOidcConfig, Certificate as _Certificate, Condition as _Condition, FixedResponseConfig as _FixedResponseConfig, HostHeaderConfig as _HostHeaderConfig, HttpHeaderConfig as _HttpHeaderConfig, HttpRequestMethodConfig as _HttpRequestMethodConfig, LoadBalancerAttributes as _LoadBalancerAttributes, Matcher as _Matcher, PathPatternConfig as _PathPatternConfig, QueryStringConfig as _QueryStringConfig, QueryStringKeyValue as _QueryStringKeyValue, RedirectConfig as _RedirectConfig, SourceIpConfig as _SourceIpConfig, SubnetMapping as _SubnetMapping, Tags as _Tags, TargetDescription as _TargetDescription, TargetGroupAttribute as _TargetGroupAttribute
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class LoadBalancerAttributes(troposphere.elasticloadbalancingv2.LoadBalancerAttributes, Mixin):

    def __init__(self, title=None, Key=NOTHING, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Value=Value, **kwargs)
        (super(LoadBalancerAttributes, self).__init__)(**processed_kwargs)


class Certificate(troposphere.elasticloadbalancingv2.Certificate, Mixin):

    def __init__(self, title=None, CertificateArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CertificateArn=CertificateArn, **kwargs)
        (super(Certificate, self).__init__)(**processed_kwargs)


class AuthenticateCognitoConfig(troposphere.elasticloadbalancingv2.AuthenticateCognitoConfig, Mixin):

    def __init__(self, title=None, UserPoolArn=REQUIRED, UserPoolClientId=REQUIRED, UserPoolDomain=REQUIRED, AuthenticationRequestExtraParams=NOTHING, OnUnauthenticatedRequest=NOTHING, Scope=NOTHING, SessionCookieName=NOTHING, SessionTimeout=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         UserPoolArn=UserPoolArn, 
         UserPoolClientId=UserPoolClientId, 
         UserPoolDomain=UserPoolDomain, 
         AuthenticationRequestExtraParams=AuthenticationRequestExtraParams, 
         OnUnauthenticatedRequest=OnUnauthenticatedRequest, 
         Scope=Scope, 
         SessionCookieName=SessionCookieName, 
         SessionTimeout=SessionTimeout, **kwargs)
        (super(AuthenticateCognitoConfig, self).__init__)(**processed_kwargs)


class AuthenticateOidcConfig(troposphere.elasticloadbalancingv2.AuthenticateOidcConfig, Mixin):

    def __init__(self, title=None, AuthorizationEndpoint=REQUIRED, ClientId=REQUIRED, ClientSecret=REQUIRED, Issuer=REQUIRED, TokenEndpoint=REQUIRED, UserInfoEndpoint=REQUIRED, AuthenticationRequestExtraParams=NOTHING, OnUnauthenticatedRequest=NOTHING, Scope=NOTHING, SessionCookieName=NOTHING, SessionTimeout=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AuthorizationEndpoint=AuthorizationEndpoint, 
         ClientId=ClientId, 
         ClientSecret=ClientSecret, 
         Issuer=Issuer, 
         TokenEndpoint=TokenEndpoint, 
         UserInfoEndpoint=UserInfoEndpoint, 
         AuthenticationRequestExtraParams=AuthenticationRequestExtraParams, 
         OnUnauthenticatedRequest=OnUnauthenticatedRequest, 
         Scope=Scope, 
         SessionCookieName=SessionCookieName, 
         SessionTimeout=SessionTimeout, **kwargs)
        (super(AuthenticateOidcConfig, self).__init__)(**processed_kwargs)


class RedirectConfig(troposphere.elasticloadbalancingv2.RedirectConfig, Mixin):

    def __init__(self, title=None, StatusCode=REQUIRED, Host=NOTHING, Path=NOTHING, Port=NOTHING, Protocol=NOTHING, Query=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         StatusCode=StatusCode, 
         Host=Host, 
         Path=Path, 
         Port=Port, 
         Protocol=Protocol, 
         Query=Query, **kwargs)
        (super(RedirectConfig, self).__init__)(**processed_kwargs)


class FixedResponseConfig(troposphere.elasticloadbalancingv2.FixedResponseConfig, Mixin):

    def __init__(self, title=None, StatusCode=REQUIRED, ContentType=NOTHING, MessageBody=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         StatusCode=StatusCode, 
         ContentType=ContentType, 
         MessageBody=MessageBody, **kwargs)
        (super(FixedResponseConfig, self).__init__)(**processed_kwargs)


class Action(troposphere.elasticloadbalancingv2.Action, Mixin):

    def __init__(self, title=None, Type=REQUIRED, AuthenticateCognitoConfig=NOTHING, AuthenticateOidcConfig=NOTHING, FixedResponseConfig=NOTHING, Order=NOTHING, RedirectConfig=NOTHING, TargetGroupArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         AuthenticateCognitoConfig=AuthenticateCognitoConfig, 
         AuthenticateOidcConfig=AuthenticateOidcConfig, 
         FixedResponseConfig=FixedResponseConfig, 
         Order=Order, 
         RedirectConfig=RedirectConfig, 
         TargetGroupArn=TargetGroupArn, **kwargs)
        (super(Action, self).__init__)(**processed_kwargs)


class HostHeaderConfig(troposphere.elasticloadbalancingv2.HostHeaderConfig, Mixin):

    def __init__(self, title=None, Values=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Values=Values, **kwargs)
        (super(HostHeaderConfig, self).__init__)(**processed_kwargs)


class HttpHeaderConfig(troposphere.elasticloadbalancingv2.HttpHeaderConfig, Mixin):

    def __init__(self, title=None, HttpHeaderName=NOTHING, Values=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HttpHeaderName=HttpHeaderName, 
         Values=Values, **kwargs)
        (super(HttpHeaderConfig, self).__init__)(**processed_kwargs)


class HttpRequestMethodConfig(troposphere.elasticloadbalancingv2.HttpRequestMethodConfig, Mixin):

    def __init__(self, title=None, Values=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Values=Values, **kwargs)
        (super(HttpRequestMethodConfig, self).__init__)(**processed_kwargs)


class PathPatternConfig(troposphere.elasticloadbalancingv2.PathPatternConfig, Mixin):

    def __init__(self, title=None, Values=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Values=Values, **kwargs)
        (super(PathPatternConfig, self).__init__)(**processed_kwargs)


class QueryStringKeyValue(troposphere.elasticloadbalancingv2.QueryStringKeyValue, Mixin):

    def __init__(self, title=None, Key=NOTHING, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Value=Value, **kwargs)
        (super(QueryStringKeyValue, self).__init__)(**processed_kwargs)


class QueryStringConfig(troposphere.elasticloadbalancingv2.QueryStringConfig, Mixin):

    def __init__(self, title=None, Values=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Values=Values, **kwargs)
        (super(QueryStringConfig, self).__init__)(**processed_kwargs)


class SourceIpConfig(troposphere.elasticloadbalancingv2.SourceIpConfig, Mixin):

    def __init__(self, title=None, Values=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Values=Values, **kwargs)
        (super(SourceIpConfig, self).__init__)(**processed_kwargs)


class Condition(troposphere.elasticloadbalancingv2.Condition, Mixin):

    def __init__(self, title=None, Field=NOTHING, HostHeaderConfig=NOTHING, HttpHeaderConfig=NOTHING, HttpRequestMethodConfig=NOTHING, PathPatternConfig=NOTHING, QueryStringConfig=NOTHING, SourceIpConfig=NOTHING, Values=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Field=Field, 
         HostHeaderConfig=HostHeaderConfig, 
         HttpHeaderConfig=HttpHeaderConfig, 
         HttpRequestMethodConfig=HttpRequestMethodConfig, 
         PathPatternConfig=PathPatternConfig, 
         QueryStringConfig=QueryStringConfig, 
         SourceIpConfig=SourceIpConfig, 
         Values=Values, **kwargs)
        (super(Condition, self).__init__)(**processed_kwargs)


class Matcher(troposphere.elasticloadbalancingv2.Matcher, Mixin):

    def __init__(self, title=None, HttpCode=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HttpCode=HttpCode, **kwargs)
        (super(Matcher, self).__init__)(**processed_kwargs)


class SubnetMapping(troposphere.elasticloadbalancingv2.SubnetMapping, Mixin):

    def __init__(self, title=None, AllocationId=REQUIRED, SubnetId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AllocationId=AllocationId, 
         SubnetId=SubnetId, **kwargs)
        (super(SubnetMapping, self).__init__)(**processed_kwargs)


class TargetGroupAttribute(troposphere.elasticloadbalancingv2.TargetGroupAttribute, Mixin):

    def __init__(self, title=None, Key=NOTHING, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Value=Value, **kwargs)
        (super(TargetGroupAttribute, self).__init__)(**processed_kwargs)


class TargetDescription(troposphere.elasticloadbalancingv2.TargetDescription, Mixin):

    def __init__(self, title=None, Id=REQUIRED, AvailabilityZone=NOTHING, Port=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Id=Id, 
         AvailabilityZone=AvailabilityZone, 
         Port=Port, **kwargs)
        (super(TargetDescription, self).__init__)(**processed_kwargs)


class Listener(troposphere.elasticloadbalancingv2.Listener, Mixin):

    def __init__(self, title, template=None, validation=True, DefaultActions=REQUIRED, LoadBalancerArn=REQUIRED, Port=REQUIRED, Protocol=REQUIRED, Certificates=NOTHING, SslPolicy=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DefaultActions=DefaultActions, 
         LoadBalancerArn=LoadBalancerArn, 
         Port=Port, 
         Protocol=Protocol, 
         Certificates=Certificates, 
         SslPolicy=SslPolicy, **kwargs)
        (super(Listener, self).__init__)(**processed_kwargs)


class ListenerCertificate(troposphere.elasticloadbalancingv2.ListenerCertificate, Mixin):

    def __init__(self, title, template=None, validation=True, Certificates=REQUIRED, ListenerArn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Certificates=Certificates, 
         ListenerArn=ListenerArn, **kwargs)
        (super(ListenerCertificate, self).__init__)(**processed_kwargs)


class ListenerRule(troposphere.elasticloadbalancingv2.ListenerRule, Mixin):

    def __init__(self, title, template=None, validation=True, Actions=REQUIRED, Conditions=REQUIRED, ListenerArn=REQUIRED, Priority=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Actions=Actions, 
         Conditions=Conditions, 
         ListenerArn=ListenerArn, 
         Priority=Priority, **kwargs)
        (super(ListenerRule, self).__init__)(**processed_kwargs)


class TargetGroup(troposphere.elasticloadbalancingv2.TargetGroup, Mixin):

    def __init__(self, title, template=None, validation=True, HealthCheckEnabled=NOTHING, HealthCheckIntervalSeconds=NOTHING, HealthCheckPath=NOTHING, HealthCheckPort=NOTHING, HealthCheckProtocol=NOTHING, HealthCheckTimeoutSeconds=NOTHING, HealthyThresholdCount=NOTHING, Matcher=NOTHING, Name=NOTHING, Port=NOTHING, Protocol=NOTHING, Tags=NOTHING, TargetGroupAttributes=NOTHING, Targets=NOTHING, TargetType=NOTHING, UnhealthyThresholdCount=NOTHING, VpcId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         HealthCheckEnabled=HealthCheckEnabled, 
         HealthCheckIntervalSeconds=HealthCheckIntervalSeconds, 
         HealthCheckPath=HealthCheckPath, 
         HealthCheckPort=HealthCheckPort, 
         HealthCheckProtocol=HealthCheckProtocol, 
         HealthCheckTimeoutSeconds=HealthCheckTimeoutSeconds, 
         HealthyThresholdCount=HealthyThresholdCount, 
         Matcher=Matcher, 
         Name=Name, 
         Port=Port, 
         Protocol=Protocol, 
         Tags=Tags, 
         TargetGroupAttributes=TargetGroupAttributes, 
         Targets=Targets, 
         TargetType=TargetType, 
         UnhealthyThresholdCount=UnhealthyThresholdCount, 
         VpcId=VpcId, **kwargs)
        (super(TargetGroup, self).__init__)(**processed_kwargs)


class LoadBalancer(troposphere.elasticloadbalancingv2.LoadBalancer, Mixin):

    def __init__(self, title, template=None, validation=True, LoadBalancerAttributes=NOTHING, Name=NOTHING, Scheme=NOTHING, IpAddressType=NOTHING, SecurityGroups=NOTHING, SubnetMappings=NOTHING, Subnets=NOTHING, Tags=NOTHING, Type=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         LoadBalancerAttributes=LoadBalancerAttributes, 
         Name=Name, 
         Scheme=Scheme, 
         IpAddressType=IpAddressType, 
         SecurityGroups=SecurityGroups, 
         SubnetMappings=SubnetMappings, 
         Subnets=Subnets, 
         Tags=Tags, 
         Type=Type, **kwargs)
        (super(LoadBalancer, self).__init__)(**processed_kwargs)