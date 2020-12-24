# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/servicediscovery.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 6994 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.servicediscovery
from troposphere.servicediscovery import DnsConfig as _DnsConfig, DnsRecord as _DnsRecord, HealthCheckConfig as _HealthCheckConfig, HealthCheckCustomConfig as _HealthCheckCustomConfig
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Instance(troposphere.servicediscovery.Instance, Mixin):

    def __init__(self, title, template=None, validation=True, InstanceAttributes=REQUIRED, ServiceId=REQUIRED, InstanceId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         InstanceAttributes=InstanceAttributes, 
         ServiceId=ServiceId, 
         InstanceId=InstanceId, **kwargs)
        (super(Instance, self).__init__)(**processed_kwargs)


class PrivateDnsNamespace(troposphere.servicediscovery.PrivateDnsNamespace, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, Vpc=REQUIRED, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         Vpc=Vpc, 
         Description=Description, **kwargs)
        (super(PrivateDnsNamespace, self).__init__)(**processed_kwargs)


class PublicDnsNamespace(troposphere.servicediscovery.PublicDnsNamespace, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         Description=Description, **kwargs)
        (super(PublicDnsNamespace, self).__init__)(**processed_kwargs)


class HealthCheckConfig(troposphere.servicediscovery.HealthCheckConfig, Mixin):

    def __init__(self, title=None, Type=REQUIRED, FailureThreshold=NOTHING, ResourcePath=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         FailureThreshold=FailureThreshold, 
         ResourcePath=ResourcePath, **kwargs)
        (super(HealthCheckConfig, self).__init__)(**processed_kwargs)


class HealthCheckCustomConfig(troposphere.servicediscovery.HealthCheckCustomConfig, Mixin):

    def __init__(self, title=None, FailureThreshold=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FailureThreshold=FailureThreshold, **kwargs)
        (super(HealthCheckCustomConfig, self).__init__)(**processed_kwargs)


class DnsRecord(troposphere.servicediscovery.DnsRecord, Mixin):

    def __init__(self, title=None, TTL=REQUIRED, Type=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TTL=TTL, 
         Type=Type, **kwargs)
        (super(DnsRecord, self).__init__)(**processed_kwargs)


class DnsConfig(troposphere.servicediscovery.DnsConfig, Mixin):

    def __init__(self, title=None, DnsRecords=REQUIRED, NamespaceId=REQUIRED, RoutingPolicy=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DnsRecords=DnsRecords, 
         NamespaceId=NamespaceId, 
         RoutingPolicy=RoutingPolicy, **kwargs)
        (super(DnsConfig, self).__init__)(**processed_kwargs)


class Service(troposphere.servicediscovery.Service, Mixin):

    def __init__(self, title, template=None, validation=True, Description=NOTHING, DnsConfig=NOTHING, HealthCheckConfig=NOTHING, HealthCheckCustomConfig=NOTHING, Name=NOTHING, NamespaceId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         DnsConfig=DnsConfig, 
         HealthCheckConfig=HealthCheckConfig, 
         HealthCheckCustomConfig=HealthCheckCustomConfig, 
         Name=Name, 
         NamespaceId=NamespaceId, **kwargs)
        (super(Service, self).__init__)(**processed_kwargs)


class HttpNamespace(troposphere.servicediscovery.HttpNamespace, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         Description=Description, **kwargs)
        (super(HttpNamespace, self).__init__)(**processed_kwargs)