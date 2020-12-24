# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/neptune.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 7467 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.neptune
from troposphere.neptune import Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class DBClusterParameterGroup(troposphere.neptune.DBClusterParameterGroup, Mixin):

    def __init__(self, title, template=None, validation=True, Description=REQUIRED, Family=REQUIRED, Parameters=REQUIRED, Name=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         Family=Family, 
         Parameters=Parameters, 
         Name=Name, 
         Tags=Tags, **kwargs)
        (super(DBClusterParameterGroup, self).__init__)(**processed_kwargs)


class DBCluster(troposphere.neptune.DBCluster, Mixin):

    def __init__(self, title, template=None, validation=True, AvailabilityZones=NOTHING, BackupRetentionPeriod=NOTHING, DBClusterIdentifier=NOTHING, DBClusterParameterGroupName=NOTHING, DBSubnetGroupName=NOTHING, EnableCloudwatchLogsExports=NOTHING, IamAuthEnabled=NOTHING, KmsKeyId=NOTHING, Port=NOTHING, PreferredBackupWindow=NOTHING, PreferredMaintenanceWindow=NOTHING, SnapshotIdentifier=NOTHING, StorageEncrypted=NOTHING, Tags=NOTHING, VpcSecurityGroupIds=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AvailabilityZones=AvailabilityZones, 
         BackupRetentionPeriod=BackupRetentionPeriod, 
         DBClusterIdentifier=DBClusterIdentifier, 
         DBClusterParameterGroupName=DBClusterParameterGroupName, 
         DBSubnetGroupName=DBSubnetGroupName, 
         EnableCloudwatchLogsExports=EnableCloudwatchLogsExports, 
         IamAuthEnabled=IamAuthEnabled, 
         KmsKeyId=KmsKeyId, 
         Port=Port, 
         PreferredBackupWindow=PreferredBackupWindow, 
         PreferredMaintenanceWindow=PreferredMaintenanceWindow, 
         SnapshotIdentifier=SnapshotIdentifier, 
         StorageEncrypted=StorageEncrypted, 
         Tags=Tags, 
         VpcSecurityGroupIds=VpcSecurityGroupIds, **kwargs)
        (super(DBCluster, self).__init__)(**processed_kwargs)


class DBInstance(troposphere.neptune.DBInstance, Mixin):

    def __init__(self, title, template=None, validation=True, DBInstanceClass=REQUIRED, AllowMajorVersionUpgrade=NOTHING, AutoMinorVersionUpgrade=NOTHING, AvailabilityZone=NOTHING, DBClusterIdentifier=NOTHING, DBInstanceIdentifier=NOTHING, DBParameterGroupName=NOTHING, DBSnapshotIdentifier=NOTHING, DBSubnetGroupName=NOTHING, PreferredMaintenanceWindow=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DBInstanceClass=DBInstanceClass, 
         AllowMajorVersionUpgrade=AllowMajorVersionUpgrade, 
         AutoMinorVersionUpgrade=AutoMinorVersionUpgrade, 
         AvailabilityZone=AvailabilityZone, 
         DBClusterIdentifier=DBClusterIdentifier, 
         DBInstanceIdentifier=DBInstanceIdentifier, 
         DBParameterGroupName=DBParameterGroupName, 
         DBSnapshotIdentifier=DBSnapshotIdentifier, 
         DBSubnetGroupName=DBSubnetGroupName, 
         PreferredMaintenanceWindow=PreferredMaintenanceWindow, 
         Tags=Tags, **kwargs)
        (super(DBInstance, self).__init__)(**processed_kwargs)


class DBParameterGroup(troposphere.neptune.DBParameterGroup, Mixin):

    def __init__(self, title, template=None, validation=True, Description=REQUIRED, Family=REQUIRED, Parameters=REQUIRED, Name=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         Family=Family, 
         Parameters=Parameters, 
         Name=Name, 
         Tags=Tags, **kwargs)
        (super(DBParameterGroup, self).__init__)(**processed_kwargs)


class DBSubnetGroup(troposphere.neptune.DBSubnetGroup, Mixin):

    def __init__(self, title, template=None, validation=True, DBSubnetGroupDescription=REQUIRED, SubnetIds=REQUIRED, DBSubnetGroupName=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DBSubnetGroupDescription=DBSubnetGroupDescription, 
         SubnetIds=SubnetIds, 
         DBSubnetGroupName=DBSubnetGroupName, 
         Tags=Tags, **kwargs)
        (super(DBSubnetGroup, self).__init__)(**processed_kwargs)