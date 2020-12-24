# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/eks.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 6029 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.eks
from troposphere.eks import LogSetup as _LogSetup, Logging as _Logging, RemoteAccess as _RemoteAccess, ResourcesVpcConfig as _ResourcesVpcConfig, ScalingConfig as _ScalingConfig, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class LogSetup(troposphere.eks.LogSetup, Mixin):

    def __init__(self, title=None, Enable=NOTHING, Types=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Enable=Enable, 
         Types=Types, **kwargs)
        (super(LogSetup, self).__init__)(**processed_kwargs)


class Logging(troposphere.eks.Logging, Mixin):

    def __init__(self, title=None, ClusterLogging=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ClusterLogging=ClusterLogging, **kwargs)
        (super(Logging, self).__init__)(**processed_kwargs)


class ResourcesVpcConfig(troposphere.eks.ResourcesVpcConfig, Mixin):

    def __init__(self, title=None, SubnetIds=REQUIRED, SecurityGroupIds=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SubnetIds=SubnetIds, 
         SecurityGroupIds=SecurityGroupIds, **kwargs)
        (super(ResourcesVpcConfig, self).__init__)(**processed_kwargs)


class Cluster(troposphere.eks.Cluster, Mixin):

    def __init__(self, title, template=None, validation=True, ResourcesVpcConfig=REQUIRED, RoleArn=REQUIRED, Name=NOTHING, Logging=NOTHING, Version=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ResourcesVpcConfig=ResourcesVpcConfig, 
         RoleArn=RoleArn, 
         Name=Name, 
         Logging=Logging, 
         Version=Version, **kwargs)
        (super(Cluster, self).__init__)(**processed_kwargs)


class RemoteAccess(troposphere.eks.RemoteAccess, Mixin):

    def __init__(self, title=None, Ec2SshKey=REQUIRED, SourceSecurityGroups=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Ec2SshKey=Ec2SshKey, 
         SourceSecurityGroups=SourceSecurityGroups, **kwargs)
        (super(RemoteAccess, self).__init__)(**processed_kwargs)


class ScalingConfig(troposphere.eks.ScalingConfig, Mixin):

    def __init__(self, title=None, DesiredSize=NOTHING, MaxSize=NOTHING, MinSize=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DesiredSize=DesiredSize, 
         MaxSize=MaxSize, 
         MinSize=MinSize, **kwargs)
        (super(ScalingConfig, self).__init__)(**processed_kwargs)


class Nodegroup(troposphere.eks.Nodegroup, Mixin):

    def __init__(self, title, template=None, validation=True, ClusterName=REQUIRED, NodeRole=REQUIRED, AmiType=NOTHING, DiskSize=NOTHING, ForceUpdateEnabled=NOTHING, InstanceTypes=NOTHING, Labels=NOTHING, NodegroupName=NOTHING, ReleaseVersion=NOTHING, RemoteAccess=NOTHING, ScalingConfig=NOTHING, Subnets=NOTHING, Tags=NOTHING, Version=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ClusterName=ClusterName, 
         NodeRole=NodeRole, 
         AmiType=AmiType, 
         DiskSize=DiskSize, 
         ForceUpdateEnabled=ForceUpdateEnabled, 
         InstanceTypes=InstanceTypes, 
         Labels=Labels, 
         NodegroupName=NodegroupName, 
         ReleaseVersion=ReleaseVersion, 
         RemoteAccess=RemoteAccess, 
         ScalingConfig=ScalingConfig, 
         Subnets=Subnets, 
         Tags=Tags, 
         Version=Version, **kwargs)
        (super(Nodegroup, self).__init__)(**processed_kwargs)