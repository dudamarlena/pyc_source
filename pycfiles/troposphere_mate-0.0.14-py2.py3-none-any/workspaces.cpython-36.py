# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/workspaces.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 2885 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.workspaces
from troposphere.workspaces import Tags as _Tags, WorkspaceProperties as _WorkspaceProperties
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class WorkspaceProperties(troposphere.workspaces.WorkspaceProperties, Mixin):

    def __init__(self, title=None, ComputeTypeName=NOTHING, RootVolumeSizeGib=NOTHING, RunningMode=NOTHING, RunningModeAutoStopTimeoutInMinutes=NOTHING, UserVolumeSizeGib=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ComputeTypeName=ComputeTypeName, 
         RootVolumeSizeGib=RootVolumeSizeGib, 
         RunningMode=RunningMode, 
         RunningModeAutoStopTimeoutInMinutes=RunningModeAutoStopTimeoutInMinutes, 
         UserVolumeSizeGib=UserVolumeSizeGib, **kwargs)
        (super(WorkspaceProperties, self).__init__)(**processed_kwargs)


class Workspace(troposphere.workspaces.Workspace, Mixin):

    def __init__(self, title, template=None, validation=True, BundleId=REQUIRED, DirectoryId=REQUIRED, UserName=REQUIRED, RootVolumeEncryptionEnabled=NOTHING, Tags=NOTHING, UserVolumeEncryptionEnabled=NOTHING, VolumeEncryptionKey=NOTHING, WorkspaceProperties=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         BundleId=BundleId, 
         DirectoryId=DirectoryId, 
         UserName=UserName, 
         RootVolumeEncryptionEnabled=RootVolumeEncryptionEnabled, 
         Tags=Tags, 
         UserVolumeEncryptionEnabled=UserVolumeEncryptionEnabled, 
         VolumeEncryptionKey=VolumeEncryptionKey, 
         WorkspaceProperties=WorkspaceProperties, **kwargs)
        (super(Workspace, self).__init__)(**processed_kwargs)