# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/rds.py
# Compiled at: 2020-02-12 18:15:54
# Size of source mod 2**32: 22742 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.rds
from troposphere.rds import DBClusterRole as _DBClusterRole, DBInstanceRole as _DBInstanceRole, OptionConfiguration as _OptionConfiguration, OptionSetting as _OptionSetting, ProcessorFeature as _ProcessorFeature, ScalingConfiguration as _ScalingConfiguration, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class DBInstanceRole(troposphere.rds.DBInstanceRole, Mixin):

    def __init__(self, title=None, FeatureName=REQUIRED, RoleArn=REQUIRED, Status=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FeatureName=FeatureName, 
         RoleArn=RoleArn, 
         Status=Status, **kwargs)
        (super(DBInstanceRole, self).__init__)(**processed_kwargs)


class ProcessorFeature(troposphere.rds.ProcessorFeature, Mixin):

    def __init__(self, title=None, Name=NOTHING, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Value=Value, **kwargs)
        (super(ProcessorFeature, self).__init__)(**processed_kwargs)


class DBInstance(troposphere.rds.DBInstance, Mixin):

    def __init__(self, title, template, validation, DBInstanceClass, AllocatedStorage, AllowMajorVersionUpgrade, AssociatedRoles, AutoMinorVersionUpgrade, AvailabilityZone, BackupRetentionPeriod, CharacterSetName, CopyTagsToSnapshot, DBClusterIdentifier, DBInstanceIdentifier, DBName, DBParameterGroupName, DBSecurityGroups, DBSnapshotIdentifier, DBSubnetGroupName, DeleteAutomatedBackups, DeletionProtection, Domain, DomainIAMRoleName, EnableCloudwatchLogsExports, EnableIAMDatabaseAuthentication, EnablePerformanceInsights, Engine, EngineVersion, Iops, KmsKeyId, LicenseModel, MasterUsername, MasterUserPassword=NoneTrueREQUIREDNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHING, MonitoringInterval=NOTHING, MonitoringRoleArn=NOTHING, MultiAZ=NOTHING, OptionGroupName=NOTHING, PerformanceInsightsKMSKeyId=NOTHING, PerformanceInsightsRetentionPeriod=NOTHING, Port=NOTHING, PreferredBackupWindow=NOTHING, PreferredMaintenanceWindow=NOTHING, ProcessorFeatures=NOTHING, PromotionTier=NOTHING, PubliclyAccessible=NOTHING, SourceDBInstanceIdentifier=NOTHING, SourceRegion=NOTHING, StorageEncrypted=NOTHING, StorageType=NOTHING, Tags=NOTHING, UseDefaultProcessorFeatures=NOTHING, Timezone=NOTHING, VPCSecurityGroups=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DBInstanceClass=DBInstanceClass, 
         AllocatedStorage=AllocatedStorage, 
         AllowMajorVersionUpgrade=AllowMajorVersionUpgrade, 
         AssociatedRoles=AssociatedRoles, 
         AutoMinorVersionUpgrade=AutoMinorVersionUpgrade, 
         AvailabilityZone=AvailabilityZone, 
         BackupRetentionPeriod=BackupRetentionPeriod, 
         CharacterSetName=CharacterSetName, 
         CopyTagsToSnapshot=CopyTagsToSnapshot, 
         DBClusterIdentifier=DBClusterIdentifier, 
         DBInstanceIdentifier=DBInstanceIdentifier, 
         DBName=DBName, 
         DBParameterGroupName=DBParameterGroupName, 
         DBSecurityGroups=DBSecurityGroups, 
         DBSnapshotIdentifier=DBSnapshotIdentifier, 
         DBSubnetGroupName=DBSubnetGroupName, 
         DeleteAutomatedBackups=DeleteAutomatedBackups, 
         DeletionProtection=DeletionProtection, 
         Domain=Domain, 
         DomainIAMRoleName=DomainIAMRoleName, 
         EnableCloudwatchLogsExports=EnableCloudwatchLogsExports, 
         EnableIAMDatabaseAuthentication=EnableIAMDatabaseAuthentication, 
         EnablePerformanceInsights=EnablePerformanceInsights, 
         Engine=Engine, 
         EngineVersion=EngineVersion, 
         Iops=Iops, 
         KmsKeyId=KmsKeyId, 
         LicenseModel=LicenseModel, 
         MasterUsername=MasterUsername, 
         MasterUserPassword=MasterUserPassword, 
         MonitoringInterval=MonitoringInterval, 
         MonitoringRoleArn=MonitoringRoleArn, 
         MultiAZ=MultiAZ, 
         OptionGroupName=OptionGroupName, 
         PerformanceInsightsKMSKeyId=PerformanceInsightsKMSKeyId, 
         PerformanceInsightsRetentionPeriod=PerformanceInsightsRetentionPeriod, 
         Port=Port, 
         PreferredBackupWindow=PreferredBackupWindow, 
         PreferredMaintenanceWindow=PreferredMaintenanceWindow, 
         ProcessorFeatures=ProcessorFeatures, 
         PromotionTier=PromotionTier, 
         PubliclyAccessible=PubliclyAccessible, 
         SourceDBInstanceIdentifier=SourceDBInstanceIdentifier, 
         SourceRegion=SourceRegion, 
         StorageEncrypted=StorageEncrypted, 
         StorageType=StorageType, 
         Tags=Tags, 
         UseDefaultProcessorFeatures=UseDefaultProcessorFeatures, 
         Timezone=Timezone, 
         VPCSecurityGroups=VPCSecurityGroups, **kwargs)
        (super(DBInstance, self).__init__)(**processed_kwargs)


class DBParameterGroup(troposphere.rds.DBParameterGroup, Mixin):

    def __init__(self, title, template=None, validation=True, Description=NOTHING, Family=NOTHING, Parameters=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         Family=Family, 
         Parameters=Parameters, 
         Tags=Tags, **kwargs)
        (super(DBParameterGroup, self).__init__)(**processed_kwargs)


class DBSubnetGroup(troposphere.rds.DBSubnetGroup, Mixin):

    def __init__(self, title, template=None, validation=True, DBSubnetGroupDescription=REQUIRED, SubnetIds=REQUIRED, DBSubnetGroupName=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DBSubnetGroupDescription=DBSubnetGroupDescription, 
         SubnetIds=SubnetIds, 
         DBSubnetGroupName=DBSubnetGroupName, 
         Tags=Tags, **kwargs)
        (super(DBSubnetGroup, self).__init__)(**processed_kwargs)


class RDSSecurityGroup(troposphere.rds.RDSSecurityGroup, Mixin):

    def __init__(self, title=None, CIDRIP=NOTHING, EC2SecurityGroupId=NOTHING, EC2SecurityGroupName=NOTHING, EC2SecurityGroupOwnerId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CIDRIP=CIDRIP, 
         EC2SecurityGroupId=EC2SecurityGroupId, 
         EC2SecurityGroupName=EC2SecurityGroupName, 
         EC2SecurityGroupOwnerId=EC2SecurityGroupOwnerId, **kwargs)
        (super(RDSSecurityGroup, self).__init__)(**processed_kwargs)


class DBSecurityGroup(troposphere.rds.DBSecurityGroup, Mixin):

    def __init__(self, title, template=None, validation=True, DBSecurityGroupIngress=REQUIRED, GroupDescription=REQUIRED, EC2VpcId=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DBSecurityGroupIngress=DBSecurityGroupIngress, 
         GroupDescription=GroupDescription, 
         EC2VpcId=EC2VpcId, 
         Tags=Tags, **kwargs)
        (super(DBSecurityGroup, self).__init__)(**processed_kwargs)


class DBSecurityGroupIngress(troposphere.rds.DBSecurityGroupIngress, Mixin):

    def __init__(self, title, template=None, validation=True, DBSecurityGroupName=REQUIRED, CIDRIP=NOTHING, EC2SecurityGroupId=NOTHING, EC2SecurityGroupName=NOTHING, EC2SecurityGroupOwnerId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DBSecurityGroupName=DBSecurityGroupName, 
         CIDRIP=CIDRIP, 
         EC2SecurityGroupId=EC2SecurityGroupId, 
         EC2SecurityGroupName=EC2SecurityGroupName, 
         EC2SecurityGroupOwnerId=EC2SecurityGroupOwnerId, **kwargs)
        (super(DBSecurityGroupIngress, self).__init__)(**processed_kwargs)


class EventSubscription(troposphere.rds.EventSubscription, Mixin):

    def __init__(self, title, template=None, validation=True, SnsTopicArn=REQUIRED, Enabled=NOTHING, EventCategories=NOTHING, SourceIds=NOTHING, SourceType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         SnsTopicArn=SnsTopicArn, 
         Enabled=Enabled, 
         EventCategories=EventCategories, 
         SourceIds=SourceIds, 
         SourceType=SourceType, **kwargs)
        (super(EventSubscription, self).__init__)(**processed_kwargs)


class OptionSetting(troposphere.rds.OptionSetting, Mixin):

    def __init__(self, title=None, Name=NOTHING, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Value=Value, **kwargs)
        (super(OptionSetting, self).__init__)(**processed_kwargs)


class OptionConfiguration(troposphere.rds.OptionConfiguration, Mixin):

    def __init__(self, title=None, OptionName=REQUIRED, DBSecurityGroupMemberships=NOTHING, OptionSettings=NOTHING, OptionVersion=NOTHING, Port=NOTHING, VpcSecurityGroupMemberships=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         OptionName=OptionName, 
         DBSecurityGroupMemberships=DBSecurityGroupMemberships, 
         OptionSettings=OptionSettings, 
         OptionVersion=OptionVersion, 
         Port=Port, 
         VpcSecurityGroupMemberships=VpcSecurityGroupMemberships, **kwargs)
        (super(OptionConfiguration, self).__init__)(**processed_kwargs)


class OptionGroup(troposphere.rds.OptionGroup, Mixin):

    def __init__(self, title, template=None, validation=True, EngineName=REQUIRED, MajorEngineVersion=REQUIRED, OptionGroupDescription=REQUIRED, OptionConfigurations=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         EngineName=EngineName, 
         MajorEngineVersion=MajorEngineVersion, 
         OptionGroupDescription=OptionGroupDescription, 
         OptionConfigurations=OptionConfigurations, 
         Tags=Tags, **kwargs)
        (super(OptionGroup, self).__init__)(**processed_kwargs)


class DBClusterParameterGroup(troposphere.rds.DBClusterParameterGroup, Mixin):

    def __init__(self, title, template=None, validation=True, Description=REQUIRED, Family=REQUIRED, Parameters=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         Family=Family, 
         Parameters=Parameters, 
         Tags=Tags, **kwargs)
        (super(DBClusterParameterGroup, self).__init__)(**processed_kwargs)


class DBClusterRole(troposphere.rds.DBClusterRole, Mixin):

    def __init__(self, title=None, RoleArn=REQUIRED, FeatureName=NOTHING, Status=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RoleArn=RoleArn, 
         FeatureName=FeatureName, 
         Status=Status, **kwargs)
        (super(DBClusterRole, self).__init__)(**processed_kwargs)


class ScalingConfiguration(troposphere.rds.ScalingConfiguration, Mixin):

    def __init__(self, title=None, AutoPause=NOTHING, MaxCapacity=NOTHING, MinCapacity=NOTHING, SecondsUntilAutoPause=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AutoPause=AutoPause, 
         MaxCapacity=MaxCapacity, 
         MinCapacity=MinCapacity, 
         SecondsUntilAutoPause=SecondsUntilAutoPause, **kwargs)
        (super(ScalingConfiguration, self).__init__)(**processed_kwargs)


class DBCluster(troposphere.rds.DBCluster, Mixin):

    def __init__(self, title, template, validation, Engine, AssociatedRoles, AvailabilityZones, BacktrackWindow, BackupRetentionPeriod, DatabaseName, DBClusterIdentifier, DBClusterParameterGroupName, DBSubnetGroupName, DeletionProtection, EnableCloudwatchLogsExports, EnableHttpEndpoint, EnableIAMDatabaseAuthentication, EngineMode, EngineVersion, KmsKeyId, MasterUsername, MasterUserPassword, Port, PreferredBackupWindow, PreferredMaintenanceWindow, ReplicationSourceIdentifier, RestoreType, ScalingConfiguration, SnapshotIdentifier, SourceDBClusterIdentifier, SourceRegion, StorageEncrypted, Tags, UseLatestRestorableTime=NoneTrueREQUIREDNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHING, VpcSecurityGroupIds=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Engine=Engine, 
         AssociatedRoles=AssociatedRoles, 
         AvailabilityZones=AvailabilityZones, 
         BacktrackWindow=BacktrackWindow, 
         BackupRetentionPeriod=BackupRetentionPeriod, 
         DatabaseName=DatabaseName, 
         DBClusterIdentifier=DBClusterIdentifier, 
         DBClusterParameterGroupName=DBClusterParameterGroupName, 
         DBSubnetGroupName=DBSubnetGroupName, 
         DeletionProtection=DeletionProtection, 
         EnableCloudwatchLogsExports=EnableCloudwatchLogsExports, 
         EnableHttpEndpoint=EnableHttpEndpoint, 
         EnableIAMDatabaseAuthentication=EnableIAMDatabaseAuthentication, 
         EngineMode=EngineMode, 
         EngineVersion=EngineVersion, 
         KmsKeyId=KmsKeyId, 
         MasterUsername=MasterUsername, 
         MasterUserPassword=MasterUserPassword, 
         Port=Port, 
         PreferredBackupWindow=PreferredBackupWindow, 
         PreferredMaintenanceWindow=PreferredMaintenanceWindow, 
         ReplicationSourceIdentifier=ReplicationSourceIdentifier, 
         RestoreType=RestoreType, 
         ScalingConfiguration=ScalingConfiguration, 
         SnapshotIdentifier=SnapshotIdentifier, 
         SourceDBClusterIdentifier=SourceDBClusterIdentifier, 
         SourceRegion=SourceRegion, 
         StorageEncrypted=StorageEncrypted, 
         Tags=Tags, 
         UseLatestRestorableTime=UseLatestRestorableTime, 
         VpcSecurityGroupIds=VpcSecurityGroupIds, **kwargs)
        (super(DBCluster, self).__init__)(**processed_kwargs)