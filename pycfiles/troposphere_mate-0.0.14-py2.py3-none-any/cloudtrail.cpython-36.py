# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/cloudtrail.py
# Compiled at: 2020-02-12 18:15:54
# Size of source mod 2**32: 3668 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.cloudtrail
from troposphere.cloudtrail import DataResource as _DataResource, EventSelector as _EventSelector, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class DataResource(troposphere.cloudtrail.DataResource, Mixin):

    def __init__(self, title=None, Type=REQUIRED, Values=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         Values=Values, **kwargs)
        (super(DataResource, self).__init__)(**processed_kwargs)


class EventSelector(troposphere.cloudtrail.EventSelector, Mixin):

    def __init__(self, title=None, DataResources=NOTHING, IncludeManagementEvents=NOTHING, ReadWriteType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DataResources=DataResources, 
         IncludeManagementEvents=IncludeManagementEvents, 
         ReadWriteType=ReadWriteType, **kwargs)
        (super(EventSelector, self).__init__)(**processed_kwargs)


class Trail(troposphere.cloudtrail.Trail, Mixin):

    def __init__(self, title, template=None, validation=True, IsLogging=REQUIRED, S3BucketName=REQUIRED, CloudWatchLogsLogGroupArn=NOTHING, CloudWatchLogsRoleArn=NOTHING, EnableLogFileValidation=NOTHING, EventSelectors=NOTHING, IncludeGlobalServiceEvents=NOTHING, IsMultiRegionTrail=NOTHING, KMSKeyId=NOTHING, S3KeyPrefix=NOTHING, SnsTopicName=NOTHING, Tags=NOTHING, TrailName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         IsLogging=IsLogging, 
         S3BucketName=S3BucketName, 
         CloudWatchLogsLogGroupArn=CloudWatchLogsLogGroupArn, 
         CloudWatchLogsRoleArn=CloudWatchLogsRoleArn, 
         EnableLogFileValidation=EnableLogFileValidation, 
         EventSelectors=EventSelectors, 
         IncludeGlobalServiceEvents=IncludeGlobalServiceEvents, 
         IsMultiRegionTrail=IsMultiRegionTrail, 
         KMSKeyId=KMSKeyId, 
         S3KeyPrefix=S3KeyPrefix, 
         SnsTopicName=SnsTopicName, 
         Tags=Tags, 
         TrailName=TrailName, **kwargs)
        (super(Trail, self).__init__)(**processed_kwargs)