# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/route53.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 12508 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.route53
from troposphere.route53 import AlarmIdentifier as _AlarmIdentifier, HealthCheckConfiguration as _HealthCheckConfiguration, HostedZoneConfiguration as _HostedZoneConfiguration, HostedZoneVPCs as _HostedZoneVPCs, IpAddressRequest as _IpAddressRequest, QueryLoggingConfig as _QueryLoggingConfig, Tags as _Tags, TargetAddress as _TargetAddress
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class AliasTarget(troposphere.route53.AliasTarget, Mixin):

    def __init__(self, title=None, HostedZoneId=REQUIRED, DNSName=REQUIRED, EvaluateTargetHealth=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HostedZoneId=HostedZoneId, 
         DNSName=DNSName, 
         EvaluateTargetHealth=EvaluateTargetHealth, **kwargs)
        (super(AliasTarget, self).__init__)(**processed_kwargs)


class GeoLocation(troposphere.route53.GeoLocation, Mixin):

    def __init__(self, title=None, ContinentCode=NOTHING, CountryCode=NOTHING, SubdivisionCode=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ContinentCode=ContinentCode, 
         CountryCode=CountryCode, 
         SubdivisionCode=SubdivisionCode, **kwargs)
        (super(GeoLocation, self).__init__)(**processed_kwargs)


class RecordSetGroup(troposphere.route53.RecordSetGroup, Mixin):

    def __init__(self, title, template=None, validation=True, HostedZoneId=NOTHING, HostedZoneName=NOTHING, RecordSets=NOTHING, Comment=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         HostedZoneId=HostedZoneId, 
         HostedZoneName=HostedZoneName, 
         RecordSets=RecordSets, 
         Comment=Comment, **kwargs)
        (super(RecordSetGroup, self).__init__)(**processed_kwargs)


class AlarmIdentifier(troposphere.route53.AlarmIdentifier, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Region=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Region=Region, **kwargs)
        (super(AlarmIdentifier, self).__init__)(**processed_kwargs)


class HealthCheckConfiguration(troposphere.route53.HealthCheckConfiguration, Mixin):

    def __init__(self, title=None, Type=REQUIRED, AlarmIdentifier=NOTHING, ChildHealthChecks=NOTHING, EnableSNI=NOTHING, FailureThreshold=NOTHING, FullyQualifiedDomainName=NOTHING, HealthThreshold=NOTHING, InsufficientDataHealthStatus=NOTHING, Inverted=NOTHING, IPAddress=NOTHING, MeasureLatency=NOTHING, Port=NOTHING, Regions=NOTHING, RequestInterval=NOTHING, ResourcePath=NOTHING, SearchString=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         AlarmIdentifier=AlarmIdentifier, 
         ChildHealthChecks=ChildHealthChecks, 
         EnableSNI=EnableSNI, 
         FailureThreshold=FailureThreshold, 
         FullyQualifiedDomainName=FullyQualifiedDomainName, 
         HealthThreshold=HealthThreshold, 
         InsufficientDataHealthStatus=InsufficientDataHealthStatus, 
         Inverted=Inverted, 
         IPAddress=IPAddress, 
         MeasureLatency=MeasureLatency, 
         Port=Port, 
         Regions=Regions, 
         RequestInterval=RequestInterval, 
         ResourcePath=ResourcePath, 
         SearchString=SearchString, **kwargs)
        (super(HealthCheckConfiguration, self).__init__)(**processed_kwargs)


class HealthCheck(troposphere.route53.HealthCheck, Mixin):

    def __init__(self, title, template=None, validation=True, HealthCheckConfig=REQUIRED, HealthCheckTags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         HealthCheckConfig=HealthCheckConfig, 
         HealthCheckTags=HealthCheckTags, **kwargs)
        (super(HealthCheck, self).__init__)(**processed_kwargs)


class HostedZoneConfiguration(troposphere.route53.HostedZoneConfiguration, Mixin):

    def __init__(self, title=None, Comment=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Comment=Comment, **kwargs)
        (super(HostedZoneConfiguration, self).__init__)(**processed_kwargs)


class HostedZoneVPCs(troposphere.route53.HostedZoneVPCs, Mixin):

    def __init__(self, title=None, VPCId=REQUIRED, VPCRegion=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         VPCId=VPCId, 
         VPCRegion=VPCRegion, **kwargs)
        (super(HostedZoneVPCs, self).__init__)(**processed_kwargs)


class QueryLoggingConfig(troposphere.route53.QueryLoggingConfig, Mixin):

    def __init__(self, title=None, CloudWatchLogsLogGroupArn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CloudWatchLogsLogGroupArn=CloudWatchLogsLogGroupArn, **kwargs)
        (super(QueryLoggingConfig, self).__init__)(**processed_kwargs)


class HostedZone(troposphere.route53.HostedZone, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, HostedZoneConfig=NOTHING, HostedZoneTags=NOTHING, QueryLoggingConfig=NOTHING, VPCs=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         HostedZoneConfig=HostedZoneConfig, 
         HostedZoneTags=HostedZoneTags, 
         QueryLoggingConfig=QueryLoggingConfig, 
         VPCs=VPCs, **kwargs)
        (super(HostedZone, self).__init__)(**processed_kwargs)


class IpAddressRequest(troposphere.route53.IpAddressRequest, Mixin):

    def __init__(self, title=None, SubnetId=REQUIRED, Ip=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SubnetId=SubnetId, 
         Ip=Ip, **kwargs)
        (super(IpAddressRequest, self).__init__)(**processed_kwargs)


class ResolverEndpoint(troposphere.route53.ResolverEndpoint, Mixin):

    def __init__(self, title, template=None, validation=True, Direction=REQUIRED, IpAddresses=REQUIRED, SecurityGroupIds=REQUIRED, Name=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Direction=Direction, 
         IpAddresses=IpAddresses, 
         SecurityGroupIds=SecurityGroupIds, 
         Name=Name, 
         Tags=Tags, **kwargs)
        (super(ResolverEndpoint, self).__init__)(**processed_kwargs)


class TargetAddress(troposphere.route53.TargetAddress, Mixin):

    def __init__(self, title=None, Ip=REQUIRED, Port=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Ip=Ip, 
         Port=Port, **kwargs)
        (super(TargetAddress, self).__init__)(**processed_kwargs)


class ResolverRule(troposphere.route53.ResolverRule, Mixin):

    def __init__(self, title, template=None, validation=True, DomainName=REQUIRED, RuleType=REQUIRED, Name=NOTHING, ResolverEndpointId=NOTHING, Tags=NOTHING, TargetIps=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DomainName=DomainName, 
         RuleType=RuleType, 
         Name=Name, 
         ResolverEndpointId=ResolverEndpointId, 
         Tags=Tags, 
         TargetIps=TargetIps, **kwargs)
        (super(ResolverRule, self).__init__)(**processed_kwargs)


class ResolverRuleAssociation(troposphere.route53.ResolverRuleAssociation, Mixin):

    def __init__(self, title, template=None, validation=True, ResolverRuleId=REQUIRED, VPCId=REQUIRED, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ResolverRuleId=ResolverRuleId, 
         VPCId=VPCId, 
         Name=Name, **kwargs)
        (super(ResolverRuleAssociation, self).__init__)(**processed_kwargs)