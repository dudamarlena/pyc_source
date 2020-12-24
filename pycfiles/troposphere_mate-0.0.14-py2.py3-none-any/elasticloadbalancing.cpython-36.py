# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/elasticloadbalancing.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 8257 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.elasticloadbalancing
from troposphere.elasticloadbalancing import AccessLoggingPolicy as _AccessLoggingPolicy, ConnectionDrainingPolicy as _ConnectionDrainingPolicy, ConnectionSettings as _ConnectionSettings, HealthCheck as _HealthCheck, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class AppCookieStickinessPolicy(troposphere.elasticloadbalancing.AppCookieStickinessPolicy, Mixin):

    def __init__(self, title=None, CookieName=REQUIRED, PolicyName=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CookieName=CookieName, 
         PolicyName=PolicyName, **kwargs)
        (super(AppCookieStickinessPolicy, self).__init__)(**processed_kwargs)


class HealthCheck(troposphere.elasticloadbalancing.HealthCheck, Mixin):

    def __init__(self, title=None, HealthyThreshold=REQUIRED, Interval=REQUIRED, Target=REQUIRED, Timeout=REQUIRED, UnhealthyThreshold=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HealthyThreshold=HealthyThreshold, 
         Interval=Interval, 
         Target=Target, 
         Timeout=Timeout, 
         UnhealthyThreshold=UnhealthyThreshold, **kwargs)
        (super(HealthCheck, self).__init__)(**processed_kwargs)


class LBCookieStickinessPolicy(troposphere.elasticloadbalancing.LBCookieStickinessPolicy, Mixin):

    def __init__(self, title=None, CookieExpirationPeriod=NOTHING, PolicyName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CookieExpirationPeriod=CookieExpirationPeriod, 
         PolicyName=PolicyName, **kwargs)
        (super(LBCookieStickinessPolicy, self).__init__)(**processed_kwargs)


class Listener(troposphere.elasticloadbalancing.Listener, Mixin):

    def __init__(self, title=None, InstancePort=REQUIRED, LoadBalancerPort=REQUIRED, Protocol=REQUIRED, InstanceProtocol=NOTHING, PolicyNames=NOTHING, SSLCertificateId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         InstancePort=InstancePort, 
         LoadBalancerPort=LoadBalancerPort, 
         Protocol=Protocol, 
         InstanceProtocol=InstanceProtocol, 
         PolicyNames=PolicyNames, 
         SSLCertificateId=SSLCertificateId, **kwargs)
        (super(Listener, self).__init__)(**processed_kwargs)


class Policy(troposphere.elasticloadbalancing.Policy, Mixin):

    def __init__(self, title=None, PolicyName=REQUIRED, PolicyType=REQUIRED, Attributes=NOTHING, InstancePorts=NOTHING, LoadBalancerPorts=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PolicyName=PolicyName, 
         PolicyType=PolicyType, 
         Attributes=Attributes, 
         InstancePorts=InstancePorts, 
         LoadBalancerPorts=LoadBalancerPorts, **kwargs)
        (super(Policy, self).__init__)(**processed_kwargs)


class ConnectionDrainingPolicy(troposphere.elasticloadbalancing.ConnectionDrainingPolicy, Mixin):

    def __init__(self, title=None, Enabled=REQUIRED, Timeout=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Enabled=Enabled, 
         Timeout=Timeout, **kwargs)
        (super(ConnectionDrainingPolicy, self).__init__)(**processed_kwargs)


class ConnectionSettings(troposphere.elasticloadbalancing.ConnectionSettings, Mixin):

    def __init__(self, title=None, IdleTimeout=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         IdleTimeout=IdleTimeout, **kwargs)
        (super(ConnectionSettings, self).__init__)(**processed_kwargs)


class AccessLoggingPolicy(troposphere.elasticloadbalancing.AccessLoggingPolicy, Mixin):

    def __init__(self, title=None, Enabled=REQUIRED, EmitInterval=NOTHING, S3BucketName=NOTHING, S3BucketPrefix=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Enabled=Enabled, 
         EmitInterval=EmitInterval, 
         S3BucketName=S3BucketName, 
         S3BucketPrefix=S3BucketPrefix, **kwargs)
        (super(AccessLoggingPolicy, self).__init__)(**processed_kwargs)


class LoadBalancer(troposphere.elasticloadbalancing.LoadBalancer, Mixin):

    def __init__(self, title, template=None, validation=True, Listeners=REQUIRED, AccessLoggingPolicy=NOTHING, AppCookieStickinessPolicy=NOTHING, AvailabilityZones=NOTHING, ConnectionDrainingPolicy=NOTHING, ConnectionSettings=NOTHING, CrossZone=NOTHING, HealthCheck=NOTHING, Instances=NOTHING, LBCookieStickinessPolicy=NOTHING, LoadBalancerName=NOTHING, Policies=NOTHING, Scheme=NOTHING, SecurityGroups=NOTHING, Subnets=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Listeners=Listeners, 
         AccessLoggingPolicy=AccessLoggingPolicy, 
         AppCookieStickinessPolicy=AppCookieStickinessPolicy, 
         AvailabilityZones=AvailabilityZones, 
         ConnectionDrainingPolicy=ConnectionDrainingPolicy, 
         ConnectionSettings=ConnectionSettings, 
         CrossZone=CrossZone, 
         HealthCheck=HealthCheck, 
         Instances=Instances, 
         LBCookieStickinessPolicy=LBCookieStickinessPolicy, 
         LoadBalancerName=LoadBalancerName, 
         Policies=Policies, 
         Scheme=Scheme, 
         SecurityGroups=SecurityGroups, 
         Subnets=Subnets, 
         Tags=Tags, **kwargs)
        (super(LoadBalancer, self).__init__)(**processed_kwargs)