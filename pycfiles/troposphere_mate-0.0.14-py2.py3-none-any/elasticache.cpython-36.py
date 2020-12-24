# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/elasticache.py
# Compiled at: 2020-02-12 18:15:54
# Size of source mod 2**32: 11655 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.elasticache
from troposphere.elasticache import Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class CacheCluster(troposphere.elasticache.CacheCluster, Mixin):

    def __init__(self, title, template=None, validation=True, CacheNodeType=REQUIRED, Engine=REQUIRED, NumCacheNodes=REQUIRED, AutoMinorVersionUpgrade=NOTHING, AZMode=NOTHING, CacheParameterGroupName=NOTHING, CacheSecurityGroupNames=NOTHING, CacheSubnetGroupName=NOTHING, ClusterName=NOTHING, EngineVersion=NOTHING, NotificationTopicArn=NOTHING, Port=NOTHING, PreferredAvailabilityZone=NOTHING, PreferredAvailabilityZones=NOTHING, PreferredMaintenanceWindow=NOTHING, SnapshotArns=NOTHING, SnapshotName=NOTHING, SnapshotRetentionLimit=NOTHING, SnapshotWindow=NOTHING, Tags=NOTHING, VpcSecurityGroupIds=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CacheNodeType=CacheNodeType, 
         Engine=Engine, 
         NumCacheNodes=NumCacheNodes, 
         AutoMinorVersionUpgrade=AutoMinorVersionUpgrade, 
         AZMode=AZMode, 
         CacheParameterGroupName=CacheParameterGroupName, 
         CacheSecurityGroupNames=CacheSecurityGroupNames, 
         CacheSubnetGroupName=CacheSubnetGroupName, 
         ClusterName=ClusterName, 
         EngineVersion=EngineVersion, 
         NotificationTopicArn=NotificationTopicArn, 
         Port=Port, 
         PreferredAvailabilityZone=PreferredAvailabilityZone, 
         PreferredAvailabilityZones=PreferredAvailabilityZones, 
         PreferredMaintenanceWindow=PreferredMaintenanceWindow, 
         SnapshotArns=SnapshotArns, 
         SnapshotName=SnapshotName, 
         SnapshotRetentionLimit=SnapshotRetentionLimit, 
         SnapshotWindow=SnapshotWindow, 
         Tags=Tags, 
         VpcSecurityGroupIds=VpcSecurityGroupIds, **kwargs)
        (super(CacheCluster, self).__init__)(**processed_kwargs)


class ParameterGroup(troposphere.elasticache.ParameterGroup, Mixin):

    def __init__(self, title, template=None, validation=True, CacheParameterGroupFamily=REQUIRED, Description=REQUIRED, Properties=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CacheParameterGroupFamily=CacheParameterGroupFamily, 
         Description=Description, 
         Properties=Properties, **kwargs)
        (super(ParameterGroup, self).__init__)(**processed_kwargs)


class SecurityGroup(troposphere.elasticache.SecurityGroup, Mixin):

    def __init__(self, title, template=None, validation=True, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, **kwargs)
        (super(SecurityGroup, self).__init__)(**processed_kwargs)


class SecurityGroupIngress(troposphere.elasticache.SecurityGroupIngress, Mixin):

    def __init__(self, title, template=None, validation=True, CacheSecurityGroupName=REQUIRED, EC2SecurityGroupName=REQUIRED, EC2SecurityGroupOwnerId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CacheSecurityGroupName=CacheSecurityGroupName, 
         EC2SecurityGroupName=EC2SecurityGroupName, 
         EC2SecurityGroupOwnerId=EC2SecurityGroupOwnerId, **kwargs)
        (super(SecurityGroupIngress, self).__init__)(**processed_kwargs)


class SubnetGroup(troposphere.elasticache.SubnetGroup, Mixin):

    def __init__(self, title, template=None, validation=True, Description=REQUIRED, SubnetIds=REQUIRED, CacheSubnetGroupName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         SubnetIds=SubnetIds, 
         CacheSubnetGroupName=CacheSubnetGroupName, **kwargs)
        (super(SubnetGroup, self).__init__)(**processed_kwargs)


class ReplicationGroup(troposphere.elasticache.ReplicationGroup, Mixin):

    def __init__(self, title, template, validation, ReplicationGroupDescription, AtRestEncryptionEnabled, AuthToken, AutoMinorVersionUpgrade, AutomaticFailoverEnabled, CacheNodeType, CacheParameterGroupName, CacheSecurityGroupNames, CacheSubnetGroupName, Engine, EngineVersion, KmsKeyId, NodeGroupConfiguration, NotificationTopicArn, NumCacheClusters, NumNodeGroups, Port, PreferredCacheClusterAZs, PreferredMaintenanceWindow, PrimaryClusterId, ReplicasPerNodeGroup, ReplicationGroupId, SecurityGroupIds, SnapshotArns, SnapshotName, SnapshotRetentionLimit, SnapshottingClusterId, SnapshotWindow, Tags, TransitEncryptionEnabled=NoneTrueREQUIREDNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ReplicationGroupDescription=ReplicationGroupDescription, 
         AtRestEncryptionEnabled=AtRestEncryptionEnabled, 
         AuthToken=AuthToken, 
         AutoMinorVersionUpgrade=AutoMinorVersionUpgrade, 
         AutomaticFailoverEnabled=AutomaticFailoverEnabled, 
         CacheNodeType=CacheNodeType, 
         CacheParameterGroupName=CacheParameterGroupName, 
         CacheSecurityGroupNames=CacheSecurityGroupNames, 
         CacheSubnetGroupName=CacheSubnetGroupName, 
         Engine=Engine, 
         EngineVersion=EngineVersion, 
         KmsKeyId=KmsKeyId, 
         NodeGroupConfiguration=NodeGroupConfiguration, 
         NotificationTopicArn=NotificationTopicArn, 
         NumCacheClusters=NumCacheClusters, 
         NumNodeGroups=NumNodeGroups, 
         Port=Port, 
         PreferredCacheClusterAZs=PreferredCacheClusterAZs, 
         PreferredMaintenanceWindow=PreferredMaintenanceWindow, 
         PrimaryClusterId=PrimaryClusterId, 
         ReplicasPerNodeGroup=ReplicasPerNodeGroup, 
         ReplicationGroupId=ReplicationGroupId, 
         SecurityGroupIds=SecurityGroupIds, 
         SnapshotArns=SnapshotArns, 
         SnapshotName=SnapshotName, 
         SnapshotRetentionLimit=SnapshotRetentionLimit, 
         SnapshottingClusterId=SnapshottingClusterId, 
         SnapshotWindow=SnapshotWindow, 
         Tags=Tags, 
         TransitEncryptionEnabled=TransitEncryptionEnabled, **kwargs)
        (super(ReplicationGroup, self).__init__)(**processed_kwargs)


class NodeGroupConfiguration(troposphere.elasticache.NodeGroupConfiguration, Mixin):

    def __init__(self, title=None, NodeGroupId=NOTHING, PrimaryAvailabilityZone=NOTHING, ReplicaAvailabilityZones=NOTHING, ReplicaCount=NOTHING, Slots=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         NodeGroupId=NodeGroupId, 
         PrimaryAvailabilityZone=PrimaryAvailabilityZone, 
         ReplicaAvailabilityZones=ReplicaAvailabilityZones, 
         ReplicaCount=ReplicaCount, 
         Slots=Slots, **kwargs)
        (super(NodeGroupConfiguration, self).__init__)(**processed_kwargs)