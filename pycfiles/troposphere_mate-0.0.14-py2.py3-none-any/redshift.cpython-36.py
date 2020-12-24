# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/redshift.py
# Compiled at: 2020-02-12 18:15:54
# Size of source mod 2**32: 9013 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.redshift
from troposphere.redshift import AmazonRedshiftParameter as _AmazonRedshiftParameter, LoggingProperties as _LoggingProperties, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class LoggingProperties(troposphere.redshift.LoggingProperties, Mixin):

    def __init__(self, title=None, BucketName=REQUIRED, S3KeyPrefix=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BucketName=BucketName, 
         S3KeyPrefix=S3KeyPrefix, **kwargs)
        (super(LoggingProperties, self).__init__)(**processed_kwargs)


class Cluster(troposphere.redshift.Cluster, Mixin):

    def __init__(self, title, template=None, validation=True, ClusterType=REQUIRED, DBName=REQUIRED, MasterUsername=REQUIRED, MasterUserPassword=REQUIRED, NodeType=REQUIRED, AllowVersionUpgrade=NOTHING, AutomatedSnapshotRetentionPeriod=NOTHING, AvailabilityZone=NOTHING, ClusterIdentifier=NOTHING, ClusterParameterGroupName=NOTHING, ClusterSecurityGroups=NOTHING, ClusterSubnetGroupName=NOTHING, ClusterVersion=NOTHING, ElasticIp=NOTHING, Encrypted=NOTHING, HsmClientCertificateIdentifier=NOTHING, HsmConfigurationIdentifier=NOTHING, IamRoles=NOTHING, KmsKeyId=NOTHING, LoggingProperties=NOTHING, NumberOfNodes=NOTHING, OwnerAccount=NOTHING, Port=NOTHING, PreferredMaintenanceWindow=NOTHING, PubliclyAccessible=NOTHING, SnapshotClusterIdentifier=NOTHING, SnapshotIdentifier=NOTHING, Tags=NOTHING, VpcSecurityGroupIds=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ClusterType=ClusterType, 
         DBName=DBName, 
         MasterUsername=MasterUsername, 
         MasterUserPassword=MasterUserPassword, 
         NodeType=NodeType, 
         AllowVersionUpgrade=AllowVersionUpgrade, 
         AutomatedSnapshotRetentionPeriod=AutomatedSnapshotRetentionPeriod, 
         AvailabilityZone=AvailabilityZone, 
         ClusterIdentifier=ClusterIdentifier, 
         ClusterParameterGroupName=ClusterParameterGroupName, 
         ClusterSecurityGroups=ClusterSecurityGroups, 
         ClusterSubnetGroupName=ClusterSubnetGroupName, 
         ClusterVersion=ClusterVersion, 
         ElasticIp=ElasticIp, 
         Encrypted=Encrypted, 
         HsmClientCertificateIdentifier=HsmClientCertificateIdentifier, 
         HsmConfigurationIdentifier=HsmConfigurationIdentifier, 
         IamRoles=IamRoles, 
         KmsKeyId=KmsKeyId, 
         LoggingProperties=LoggingProperties, 
         NumberOfNodes=NumberOfNodes, 
         OwnerAccount=OwnerAccount, 
         Port=Port, 
         PreferredMaintenanceWindow=PreferredMaintenanceWindow, 
         PubliclyAccessible=PubliclyAccessible, 
         SnapshotClusterIdentifier=SnapshotClusterIdentifier, 
         SnapshotIdentifier=SnapshotIdentifier, 
         Tags=Tags, 
         VpcSecurityGroupIds=VpcSecurityGroupIds, **kwargs)
        (super(Cluster, self).__init__)(**processed_kwargs)


class AmazonRedshiftParameter(troposphere.redshift.AmazonRedshiftParameter, Mixin):

    def __init__(self, title=None, ParameterName=REQUIRED, ParameterValue=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ParameterName=ParameterName, 
         ParameterValue=ParameterValue, **kwargs)
        (super(AmazonRedshiftParameter, self).__init__)(**processed_kwargs)


class ClusterParameterGroup(troposphere.redshift.ClusterParameterGroup, Mixin):

    def __init__(self, title, template=None, validation=True, Description=REQUIRED, ParameterGroupFamily=REQUIRED, Parameters=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         ParameterGroupFamily=ParameterGroupFamily, 
         Parameters=Parameters, 
         Tags=Tags, **kwargs)
        (super(ClusterParameterGroup, self).__init__)(**processed_kwargs)


class ClusterSecurityGroup(troposphere.redshift.ClusterSecurityGroup, Mixin):

    def __init__(self, title, template=None, validation=True, Description=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         Tags=Tags, **kwargs)
        (super(ClusterSecurityGroup, self).__init__)(**processed_kwargs)


class ClusterSecurityGroupIngress(troposphere.redshift.ClusterSecurityGroupIngress, Mixin):

    def __init__(self, title, template=None, validation=True, ClusterSecurityGroupName=REQUIRED, CIDRIP=NOTHING, EC2SecurityGroupName=NOTHING, EC2SecurityGroupOwnerId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ClusterSecurityGroupName=ClusterSecurityGroupName, 
         CIDRIP=CIDRIP, 
         EC2SecurityGroupName=EC2SecurityGroupName, 
         EC2SecurityGroupOwnerId=EC2SecurityGroupOwnerId, **kwargs)
        (super(ClusterSecurityGroupIngress, self).__init__)(**processed_kwargs)


class ClusterSubnetGroup(troposphere.redshift.ClusterSubnetGroup, Mixin):

    def __init__(self, title, template=None, validation=True, Description=REQUIRED, SubnetIds=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         SubnetIds=SubnetIds, 
         Tags=Tags, **kwargs)
        (super(ClusterSubnetGroup, self).__init__)(**processed_kwargs)