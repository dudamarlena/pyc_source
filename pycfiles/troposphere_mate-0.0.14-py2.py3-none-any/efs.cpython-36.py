# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/efs.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 3123 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.efs
from troposphere.efs import LifecyclePolicy as _LifecyclePolicy, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class LifecyclePolicy(troposphere.efs.LifecyclePolicy, Mixin):

    def __init__(self, title=None, TransitionToIA=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TransitionToIA=TransitionToIA, **kwargs)
        (super(LifecyclePolicy, self).__init__)(**processed_kwargs)


class FileSystem(troposphere.efs.FileSystem, Mixin):

    def __init__(self, title, template=None, validation=True, Encrypted=NOTHING, FileSystemTags=NOTHING, KmsKeyId=NOTHING, LifecyclePolicies=NOTHING, PerformanceMode=NOTHING, ProvisionedThroughputInMibps=NOTHING, ThroughputMode=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Encrypted=Encrypted, 
         FileSystemTags=FileSystemTags, 
         KmsKeyId=KmsKeyId, 
         LifecyclePolicies=LifecyclePolicies, 
         PerformanceMode=PerformanceMode, 
         ProvisionedThroughputInMibps=ProvisionedThroughputInMibps, 
         ThroughputMode=ThroughputMode, **kwargs)
        (super(FileSystem, self).__init__)(**processed_kwargs)


class MountTarget(troposphere.efs.MountTarget, Mixin):

    def __init__(self, title, template=None, validation=True, FileSystemId=REQUIRED, SecurityGroups=REQUIRED, SubnetId=REQUIRED, IpAddress=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         FileSystemId=FileSystemId, 
         SecurityGroups=SecurityGroups, 
         SubnetId=SubnetId, 
         IpAddress=IpAddress, **kwargs)
        (super(MountTarget, self).__init__)(**processed_kwargs)