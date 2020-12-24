# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/appmesh.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 27489 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.appmesh
from troposphere.appmesh import AccessLog as _AccessLog, AwsCloudMapInstanceAttribute as _AwsCloudMapInstanceAttribute, AwsCloudMapServiceDiscovery as _AwsCloudMapServiceDiscovery, Backend as _Backend, DnsServiceDiscovery as _DnsServiceDiscovery, Duration as _Duration, EgressFilter as _EgressFilter, FileAccessLog as _FileAccessLog, GrpcRetryPolicy as _GrpcRetryPolicy, GrpcRoute as _GrpcRoute, GrpcRouteAction as _GrpcRouteAction, GrpcRouteMatch as _GrpcRouteMatch, GrpcRouteMetadata as _GrpcRouteMetadata, GrpcRouteMetadataMatchMethod as _GrpcRouteMetadataMatchMethod, HeaderMatchMethod as _HeaderMatchMethod, HealthCheck as _HealthCheck, HttpRetryPolicy as _HttpRetryPolicy, HttpRoute as _HttpRoute, HttpRouteAction as _HttpRouteAction, HttpRouteHeader as _HttpRouteHeader, HttpRouteMatch as _HttpRouteMatch, Listener as _Listener, Logging as _Logging, MatchRange as _MatchRange, MeshSpec as _MeshSpec, PortMapping as _PortMapping, RouteSpec as _RouteSpec, ServiceDiscovery as _ServiceDiscovery, Tags as _Tags, TcpRoute as _TcpRoute, TcpRouteAction as _TcpRouteAction, VirtualNodeServiceProvider as _VirtualNodeServiceProvider, VirtualNodeSpec as _VirtualNodeSpec, VirtualRouterListener as _VirtualRouterListener, VirtualRouterServiceProvider as _VirtualRouterServiceProvider, VirtualRouterSpec as _VirtualRouterSpec, VirtualServiceBackend as _VirtualServiceBackend, VirtualServiceProvider as _VirtualServiceProvider, VirtualServiceSpec as _VirtualServiceSpec, WeightedTarget as _WeightedTarget
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class EgressFilter(troposphere.appmesh.EgressFilter, Mixin):

    def __init__(self, title=None, Type=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, **kwargs)
        (super(EgressFilter, self).__init__)(**processed_kwargs)


class MeshSpec(troposphere.appmesh.MeshSpec, Mixin):

    def __init__(self, title=None, EgressFilter=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EgressFilter=EgressFilter, **kwargs)
        (super(MeshSpec, self).__init__)(**processed_kwargs)


class Mesh(troposphere.appmesh.Mesh, Mixin):

    def __init__(self, title, template=None, validation=True, MeshName=REQUIRED, Spec=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         MeshName=MeshName, 
         Spec=Spec, 
         Tags=Tags, **kwargs)
        (super(Mesh, self).__init__)(**processed_kwargs)


class Duration(troposphere.appmesh.Duration, Mixin):

    def __init__(self, title=None, Unit=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Unit=Unit, 
         Value=Value, **kwargs)
        (super(Duration, self).__init__)(**processed_kwargs)


class GrpcRetryPolicy(troposphere.appmesh.GrpcRetryPolicy, Mixin):

    def __init__(self, title=None, MaxRetries=REQUIRED, PerRetryTimeout=REQUIRED, GrpcRetryEvents=NOTHING, HttpRetryEvents=NOTHING, TcpRetryEvents=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MaxRetries=MaxRetries, 
         PerRetryTimeout=PerRetryTimeout, 
         GrpcRetryEvents=GrpcRetryEvents, 
         HttpRetryEvents=HttpRetryEvents, 
         TcpRetryEvents=TcpRetryEvents, **kwargs)
        (super(GrpcRetryPolicy, self).__init__)(**processed_kwargs)


class WeightedTarget(troposphere.appmesh.WeightedTarget, Mixin):

    def __init__(self, title=None, VirtualNode=REQUIRED, Weight=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         VirtualNode=VirtualNode, 
         Weight=Weight, **kwargs)
        (super(WeightedTarget, self).__init__)(**processed_kwargs)


class GrpcRouteAction(troposphere.appmesh.GrpcRouteAction, Mixin):

    def __init__(self, title=None, WeightedTargets=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         WeightedTargets=WeightedTargets, **kwargs)
        (super(GrpcRouteAction, self).__init__)(**processed_kwargs)


class MatchRange(troposphere.appmesh.MatchRange, Mixin):

    def __init__(self, title=None, End=REQUIRED, Start=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         End=End, 
         Start=Start, **kwargs)
        (super(MatchRange, self).__init__)(**processed_kwargs)


class GrpcRouteMetadataMatchMethod(troposphere.appmesh.GrpcRouteMetadataMatchMethod, Mixin):

    def __init__(self, title=None, Exact=NOTHING, Prefix=NOTHING, Range=NOTHING, Regex=NOTHING, Suffix=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Exact=Exact, 
         Prefix=Prefix, 
         Range=Range, 
         Regex=Regex, 
         Suffix=Suffix, **kwargs)
        (super(GrpcRouteMetadataMatchMethod, self).__init__)(**processed_kwargs)


class GrpcRouteMetadata(troposphere.appmesh.GrpcRouteMetadata, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Invert=NOTHING, Match=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Invert=Invert, 
         Match=Match, **kwargs)
        (super(GrpcRouteMetadata, self).__init__)(**processed_kwargs)


class GrpcRouteMatch(troposphere.appmesh.GrpcRouteMatch, Mixin):

    def __init__(self, title=None, Metadata=NOTHING, MethodName=NOTHING, ServiceName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Metadata=Metadata, 
         MethodName=MethodName, 
         ServiceName=ServiceName, **kwargs)
        (super(GrpcRouteMatch, self).__init__)(**processed_kwargs)


class GrpcRoute(troposphere.appmesh.GrpcRoute, Mixin):

    def __init__(self, title=None, Action=REQUIRED, Match=REQUIRED, RetryPolicy=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Action=Action, 
         Match=Match, 
         RetryPolicy=RetryPolicy, **kwargs)
        (super(GrpcRoute, self).__init__)(**processed_kwargs)


class HttpRetryPolicy(troposphere.appmesh.HttpRetryPolicy, Mixin):

    def __init__(self, title=None, MaxRetries=REQUIRED, PerRetryTimeout=REQUIRED, HttpRetryEvents=NOTHING, TcpRetryEvents=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MaxRetries=MaxRetries, 
         PerRetryTimeout=PerRetryTimeout, 
         HttpRetryEvents=HttpRetryEvents, 
         TcpRetryEvents=TcpRetryEvents, **kwargs)
        (super(HttpRetryPolicy, self).__init__)(**processed_kwargs)


class HttpRouteAction(troposphere.appmesh.HttpRouteAction, Mixin):

    def __init__(self, title=None, WeightedTargets=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         WeightedTargets=WeightedTargets, **kwargs)
        (super(HttpRouteAction, self).__init__)(**processed_kwargs)


class HeaderMatchMethod(troposphere.appmesh.HeaderMatchMethod, Mixin):

    def __init__(self, title=None, Exact=NOTHING, Prefix=NOTHING, Range=NOTHING, Regex=NOTHING, Suffix=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Exact=Exact, 
         Prefix=Prefix, 
         Range=Range, 
         Regex=Regex, 
         Suffix=Suffix, **kwargs)
        (super(HeaderMatchMethod, self).__init__)(**processed_kwargs)


class HttpRouteHeader(troposphere.appmesh.HttpRouteHeader, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Invert=NOTHING, Match=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Invert=Invert, 
         Match=Match, **kwargs)
        (super(HttpRouteHeader, self).__init__)(**processed_kwargs)


class HttpRouteMatch(troposphere.appmesh.HttpRouteMatch, Mixin):

    def __init__(self, title=None, Prefix=REQUIRED, Headers=NOTHING, Method=NOTHING, Scheme=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Prefix=Prefix, 
         Headers=Headers, 
         Method=Method, 
         Scheme=Scheme, **kwargs)
        (super(HttpRouteMatch, self).__init__)(**processed_kwargs)


class HttpRoute(troposphere.appmesh.HttpRoute, Mixin):

    def __init__(self, title=None, Action=REQUIRED, Match=REQUIRED, RetryPolicy=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Action=Action, 
         Match=Match, 
         RetryPolicy=RetryPolicy, **kwargs)
        (super(HttpRoute, self).__init__)(**processed_kwargs)


class TcpRouteAction(troposphere.appmesh.TcpRouteAction, Mixin):

    def __init__(self, title=None, WeightedTargets=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         WeightedTargets=WeightedTargets, **kwargs)
        (super(TcpRouteAction, self).__init__)(**processed_kwargs)


class TcpRoute(troposphere.appmesh.TcpRoute, Mixin):

    def __init__(self, title=None, Action=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Action=Action, **kwargs)
        (super(TcpRoute, self).__init__)(**processed_kwargs)


class RouteSpec(troposphere.appmesh.RouteSpec, Mixin):

    def __init__(self, title=None, GrpcRoute=NOTHING, Http2Route=NOTHING, HttpRoute=NOTHING, Priority=NOTHING, TcpRoute=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         GrpcRoute=GrpcRoute, 
         Http2Route=Http2Route, 
         HttpRoute=HttpRoute, 
         Priority=Priority, 
         TcpRoute=TcpRoute, **kwargs)
        (super(RouteSpec, self).__init__)(**processed_kwargs)


class Route(troposphere.appmesh.Route, Mixin):

    def __init__(self, title, template=None, validation=True, MeshName=REQUIRED, RouteName=REQUIRED, Spec=REQUIRED, VirtualRouterName=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         MeshName=MeshName, 
         RouteName=RouteName, 
         Spec=Spec, 
         VirtualRouterName=VirtualRouterName, 
         Tags=Tags, **kwargs)
        (super(Route, self).__init__)(**processed_kwargs)


class VirtualServiceBackend(troposphere.appmesh.VirtualServiceBackend, Mixin):

    def __init__(self, title=None, VirtualServiceName=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         VirtualServiceName=VirtualServiceName, **kwargs)
        (super(VirtualServiceBackend, self).__init__)(**processed_kwargs)


class Backend(troposphere.appmesh.Backend, Mixin):

    def __init__(self, title=None, VirtualService=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         VirtualService=VirtualService, **kwargs)
        (super(Backend, self).__init__)(**processed_kwargs)


class HealthCheck(troposphere.appmesh.HealthCheck, Mixin):

    def __init__(self, title=None, HealthyThreshold=REQUIRED, IntervalMillis=REQUIRED, Protocol=REQUIRED, TimeoutMillis=REQUIRED, UnhealthyThreshold=REQUIRED, Path=NOTHING, Port=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HealthyThreshold=HealthyThreshold, 
         IntervalMillis=IntervalMillis, 
         Protocol=Protocol, 
         TimeoutMillis=TimeoutMillis, 
         UnhealthyThreshold=UnhealthyThreshold, 
         Path=Path, 
         Port=Port, **kwargs)
        (super(HealthCheck, self).__init__)(**processed_kwargs)


class PortMapping(troposphere.appmesh.PortMapping, Mixin):

    def __init__(self, title=None, Port=REQUIRED, Protocol=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Port=Port, 
         Protocol=Protocol, **kwargs)
        (super(PortMapping, self).__init__)(**processed_kwargs)


class Listener(troposphere.appmesh.Listener, Mixin):

    def __init__(self, title=None, PortMapping=REQUIRED, HealthCheck=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PortMapping=PortMapping, 
         HealthCheck=HealthCheck, **kwargs)
        (super(Listener, self).__init__)(**processed_kwargs)


class FileAccessLog(troposphere.appmesh.FileAccessLog, Mixin):

    def __init__(self, title=None, Path=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Path=Path, **kwargs)
        (super(FileAccessLog, self).__init__)(**processed_kwargs)


class AccessLog(troposphere.appmesh.AccessLog, Mixin):

    def __init__(self, title=None, File=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         File=File, **kwargs)
        (super(AccessLog, self).__init__)(**processed_kwargs)


class Logging(troposphere.appmesh.Logging, Mixin):

    def __init__(self, title=None, AccessLog=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AccessLog=AccessLog, **kwargs)
        (super(Logging, self).__init__)(**processed_kwargs)


class AwsCloudMapInstanceAttribute(troposphere.appmesh.AwsCloudMapInstanceAttribute, Mixin):

    def __init__(self, title=None, Key=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Value=Value, **kwargs)
        (super(AwsCloudMapInstanceAttribute, self).__init__)(**processed_kwargs)


class AwsCloudMapServiceDiscovery(troposphere.appmesh.AwsCloudMapServiceDiscovery, Mixin):

    def __init__(self, title=None, NamespaceName=REQUIRED, ServiceName=REQUIRED, Attributes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         NamespaceName=NamespaceName, 
         ServiceName=ServiceName, 
         Attributes=Attributes, **kwargs)
        (super(AwsCloudMapServiceDiscovery, self).__init__)(**processed_kwargs)


class DnsServiceDiscovery(troposphere.appmesh.DnsServiceDiscovery, Mixin):

    def __init__(self, title=None, Hostname=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Hostname=Hostname, **kwargs)
        (super(DnsServiceDiscovery, self).__init__)(**processed_kwargs)


class ServiceDiscovery(troposphere.appmesh.ServiceDiscovery, Mixin):

    def __init__(self, title=None, AWSCloudMap=NOTHING, DNS=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AWSCloudMap=AWSCloudMap, 
         DNS=DNS, **kwargs)
        (super(ServiceDiscovery, self).__init__)(**processed_kwargs)


class VirtualNodeSpec(troposphere.appmesh.VirtualNodeSpec, Mixin):

    def __init__(self, title=None, Backends=NOTHING, Listeners=NOTHING, Logging=NOTHING, ServiceDiscovery=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Backends=Backends, 
         Listeners=Listeners, 
         Logging=Logging, 
         ServiceDiscovery=ServiceDiscovery, **kwargs)
        (super(VirtualNodeSpec, self).__init__)(**processed_kwargs)


class VirtualNode(troposphere.appmesh.VirtualNode, Mixin):

    def __init__(self, title, template=None, validation=True, MeshName=REQUIRED, Spec=REQUIRED, VirtualNodeName=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         MeshName=MeshName, 
         Spec=Spec, 
         VirtualNodeName=VirtualNodeName, 
         Tags=Tags, **kwargs)
        (super(VirtualNode, self).__init__)(**processed_kwargs)


class VirtualRouterListener(troposphere.appmesh.VirtualRouterListener, Mixin):

    def __init__(self, title=None, PortMapping=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PortMapping=PortMapping, **kwargs)
        (super(VirtualRouterListener, self).__init__)(**processed_kwargs)


class VirtualRouterSpec(troposphere.appmesh.VirtualRouterSpec, Mixin):

    def __init__(self, title=None, Listeners=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Listeners=Listeners, **kwargs)
        (super(VirtualRouterSpec, self).__init__)(**processed_kwargs)


class VirtualRouter(troposphere.appmesh.VirtualRouter, Mixin):

    def __init__(self, title, template=None, validation=True, MeshName=REQUIRED, Spec=REQUIRED, VirtualRouterName=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         MeshName=MeshName, 
         Spec=Spec, 
         VirtualRouterName=VirtualRouterName, 
         Tags=Tags, **kwargs)
        (super(VirtualRouter, self).__init__)(**processed_kwargs)


class VirtualNodeServiceProvider(troposphere.appmesh.VirtualNodeServiceProvider, Mixin):

    def __init__(self, title=None, VirtualNodeName=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         VirtualNodeName=VirtualNodeName, **kwargs)
        (super(VirtualNodeServiceProvider, self).__init__)(**processed_kwargs)


class VirtualRouterServiceProvider(troposphere.appmesh.VirtualRouterServiceProvider, Mixin):

    def __init__(self, title=None, VirtualRouterName=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         VirtualRouterName=VirtualRouterName, **kwargs)
        (super(VirtualRouterServiceProvider, self).__init__)(**processed_kwargs)


class VirtualServiceProvider(troposphere.appmesh.VirtualServiceProvider, Mixin):

    def __init__(self, title=None, VirtualNode=NOTHING, VirtualRouter=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         VirtualNode=VirtualNode, 
         VirtualRouter=VirtualRouter, **kwargs)
        (super(VirtualServiceProvider, self).__init__)(**processed_kwargs)


class VirtualServiceSpec(troposphere.appmesh.VirtualServiceSpec, Mixin):

    def __init__(self, title=None, Provider=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Provider=Provider, **kwargs)
        (super(VirtualServiceSpec, self).__init__)(**processed_kwargs)


class VirtualService(troposphere.appmesh.VirtualService, Mixin):

    def __init__(self, title, template=None, validation=True, MeshName=REQUIRED, Spec=REQUIRED, VirtualServiceName=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         MeshName=MeshName, 
         Spec=Spec, 
         VirtualServiceName=VirtualServiceName, 
         Tags=Tags, **kwargs)
        (super(VirtualService, self).__init__)(**processed_kwargs)