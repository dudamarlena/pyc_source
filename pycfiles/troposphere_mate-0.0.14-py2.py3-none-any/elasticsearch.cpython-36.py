# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/elasticsearch.py
# Compiled at: 2020-02-12 18:15:54
# Size of source mod 2**32: 7829 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.elasticsearch
from troposphere.elasticsearch import CognitoOptions as _CognitoOptions, EBSOptions as _EBSOptions, ElasticsearchClusterConfig as _ElasticsearchClusterConfig, EncryptionAtRestOptions as _EncryptionAtRestOptions, NodeToNodeEncryptionOptions as _NodeToNodeEncryptionOptions, SnapshotOptions as _SnapshotOptions, Tags as _Tags, VPCOptions as _VPCOptions, ZoneAwarenessConfig as _ZoneAwarenessConfig
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class CognitoOptions(troposphere.elasticsearch.CognitoOptions, Mixin):

    def __init__(self, title=None, Enabled=NOTHING, IdentityPoolId=NOTHING, RoleArn=NOTHING, UserPoolId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Enabled=Enabled, 
         IdentityPoolId=IdentityPoolId, 
         RoleArn=RoleArn, 
         UserPoolId=UserPoolId, **kwargs)
        (super(CognitoOptions, self).__init__)(**processed_kwargs)


class EBSOptions(troposphere.elasticsearch.EBSOptions, Mixin):

    def __init__(self, title=None, EBSEnabled=NOTHING, Iops=NOTHING, VolumeSize=NOTHING, VolumeType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EBSEnabled=EBSEnabled, 
         Iops=Iops, 
         VolumeSize=VolumeSize, 
         VolumeType=VolumeType, **kwargs)
        (super(EBSOptions, self).__init__)(**processed_kwargs)


class ZoneAwarenessConfig(troposphere.elasticsearch.ZoneAwarenessConfig, Mixin):

    def __init__(self, title=None, AvailabilityZoneCount=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AvailabilityZoneCount=AvailabilityZoneCount, **kwargs)
        (super(ZoneAwarenessConfig, self).__init__)(**processed_kwargs)


class ElasticsearchClusterConfig(troposphere.elasticsearch.ElasticsearchClusterConfig, Mixin):

    def __init__(self, title=None, DedicatedMasterCount=NOTHING, DedicatedMasterEnabled=NOTHING, DedicatedMasterType=NOTHING, InstanceCount=NOTHING, InstanceType=NOTHING, ZoneAwarenessConfig=NOTHING, ZoneAwarenessEnabled=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DedicatedMasterCount=DedicatedMasterCount, 
         DedicatedMasterEnabled=DedicatedMasterEnabled, 
         DedicatedMasterType=DedicatedMasterType, 
         InstanceCount=InstanceCount, 
         InstanceType=InstanceType, 
         ZoneAwarenessConfig=ZoneAwarenessConfig, 
         ZoneAwarenessEnabled=ZoneAwarenessEnabled, **kwargs)
        (super(ElasticsearchClusterConfig, self).__init__)(**processed_kwargs)


class EncryptionAtRestOptions(troposphere.elasticsearch.EncryptionAtRestOptions, Mixin):

    def __init__(self, title=None, Enabled=NOTHING, KmsKeyId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Enabled=Enabled, 
         KmsKeyId=KmsKeyId, **kwargs)
        (super(EncryptionAtRestOptions, self).__init__)(**processed_kwargs)


class NodeToNodeEncryptionOptions(troposphere.elasticsearch.NodeToNodeEncryptionOptions, Mixin):

    def __init__(self, title=None, Enabled=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Enabled=Enabled, **kwargs)
        (super(NodeToNodeEncryptionOptions, self).__init__)(**processed_kwargs)


class SnapshotOptions(troposphere.elasticsearch.SnapshotOptions, Mixin):

    def __init__(self, title=None, AutomatedSnapshotStartHour=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AutomatedSnapshotStartHour=AutomatedSnapshotStartHour, **kwargs)
        (super(SnapshotOptions, self).__init__)(**processed_kwargs)


class VPCOptions(troposphere.elasticsearch.VPCOptions, Mixin):

    def __init__(self, title=None, SecurityGroupIds=NOTHING, SubnetIds=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SecurityGroupIds=SecurityGroupIds, 
         SubnetIds=SubnetIds, **kwargs)
        (super(VPCOptions, self).__init__)(**processed_kwargs)


class Domain(troposphere.elasticsearch.Domain, Mixin):

    def __init__(self, title, template=None, validation=True, AccessPolicies=NOTHING, AdvancedOptions=NOTHING, CognitoOptions=NOTHING, DomainName=NOTHING, EBSOptions=NOTHING, ElasticsearchClusterConfig=NOTHING, ElasticsearchVersion=NOTHING, EncryptionAtRestOptions=NOTHING, LogPublishingOptions=NOTHING, NodeToNodeEncryptionOptions=NOTHING, SnapshotOptions=NOTHING, Tags=NOTHING, VPCOptions=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AccessPolicies=AccessPolicies, 
         AdvancedOptions=AdvancedOptions, 
         CognitoOptions=CognitoOptions, 
         DomainName=DomainName, 
         EBSOptions=EBSOptions, 
         ElasticsearchClusterConfig=ElasticsearchClusterConfig, 
         ElasticsearchVersion=ElasticsearchVersion, 
         EncryptionAtRestOptions=EncryptionAtRestOptions, 
         LogPublishingOptions=LogPublishingOptions, 
         NodeToNodeEncryptionOptions=NodeToNodeEncryptionOptions, 
         SnapshotOptions=SnapshotOptions, 
         Tags=Tags, 
         VPCOptions=VPCOptions, **kwargs)
        (super(Domain, self).__init__)(**processed_kwargs)