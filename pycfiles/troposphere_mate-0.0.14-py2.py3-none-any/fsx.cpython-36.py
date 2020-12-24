# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/fsx.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 5410 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.fsx
from troposphere.fsx import LustreConfiguration as _LustreConfiguration, SelfManagedActiveDirectoryConfiguration as _SelfManagedActiveDirectoryConfiguration, Tags as _Tags, WindowsConfiguration as _WindowsConfiguration
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class LustreConfiguration(troposphere.fsx.LustreConfiguration, Mixin):

    def __init__(self, title=None, ExportPath=NOTHING, ImportedFileChunkSize=NOTHING, ImportPath=NOTHING, WeeklyMaintenanceStartTime=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ExportPath=ExportPath, 
         ImportedFileChunkSize=ImportedFileChunkSize, 
         ImportPath=ImportPath, 
         WeeklyMaintenanceStartTime=WeeklyMaintenanceStartTime, **kwargs)
        (super(LustreConfiguration, self).__init__)(**processed_kwargs)


class SelfManagedActiveDirectoryConfiguration(troposphere.fsx.SelfManagedActiveDirectoryConfiguration, Mixin):

    def __init__(self, title=None, DnsIps=NOTHING, DomainName=NOTHING, FileSystemAdministratorsGroup=NOTHING, OrganizationalUnitDistinguishedName=NOTHING, Password=NOTHING, UserName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DnsIps=DnsIps, 
         DomainName=DomainName, 
         FileSystemAdministratorsGroup=FileSystemAdministratorsGroup, 
         OrganizationalUnitDistinguishedName=OrganizationalUnitDistinguishedName, 
         Password=Password, 
         UserName=UserName, **kwargs)
        (super(SelfManagedActiveDirectoryConfiguration, self).__init__)(**processed_kwargs)


class WindowsConfiguration(troposphere.fsx.WindowsConfiguration, Mixin):

    def __init__(self, title=None, ActiveDirectoryId=NOTHING, AutomaticBackupRetentionDays=NOTHING, CopyTagsToBackups=NOTHING, DailyAutomaticBackupStartTime=NOTHING, SelfManagedActiveDirectoryConfiguration=NOTHING, ThroughputCapacity=NOTHING, WeeklyMaintenanceStartTime=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ActiveDirectoryId=ActiveDirectoryId, 
         AutomaticBackupRetentionDays=AutomaticBackupRetentionDays, 
         CopyTagsToBackups=CopyTagsToBackups, 
         DailyAutomaticBackupStartTime=DailyAutomaticBackupStartTime, 
         SelfManagedActiveDirectoryConfiguration=SelfManagedActiveDirectoryConfiguration, 
         ThroughputCapacity=ThroughputCapacity, 
         WeeklyMaintenanceStartTime=WeeklyMaintenanceStartTime, **kwargs)
        (super(WindowsConfiguration, self).__init__)(**processed_kwargs)


class FileSystem(troposphere.fsx.FileSystem, Mixin):

    def __init__(self, title, template=None, validation=True, BackupId=NOTHING, FileSystemType=NOTHING, KmsKeyId=NOTHING, LustreConfiguration=NOTHING, SecurityGroupIds=NOTHING, StorageCapacity=NOTHING, SubnetIds=NOTHING, Tags=NOTHING, WindowsConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         BackupId=BackupId, 
         FileSystemType=FileSystemType, 
         KmsKeyId=KmsKeyId, 
         LustreConfiguration=LustreConfiguration, 
         SecurityGroupIds=SecurityGroupIds, 
         StorageCapacity=StorageCapacity, 
         SubnetIds=SubnetIds, 
         Tags=Tags, 
         WindowsConfiguration=WindowsConfiguration, **kwargs)
        (super(FileSystem, self).__init__)(**processed_kwargs)