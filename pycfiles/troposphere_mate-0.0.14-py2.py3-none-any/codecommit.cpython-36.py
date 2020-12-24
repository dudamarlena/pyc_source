# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/codecommit.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 3278 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.codecommit
from troposphere.codecommit import Code as _Code, S3 as _S3, Tags as _Tags, Trigger as _Trigger
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class S3(troposphere.codecommit.S3, Mixin):

    def __init__(self, title=None, Bucket=REQUIRED, Key=REQUIRED, ObjectVersion=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Bucket=Bucket, 
         Key=Key, 
         ObjectVersion=ObjectVersion, **kwargs)
        (super(S3, self).__init__)(**processed_kwargs)


class Code(troposphere.codecommit.Code, Mixin):

    def __init__(self, title=None, S3=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         S3=S3, **kwargs)
        (super(Code, self).__init__)(**processed_kwargs)


class Trigger(troposphere.codecommit.Trigger, Mixin):

    def __init__(self, title=None, Branches=NOTHING, CustomData=NOTHING, DestinationArn=NOTHING, Events=NOTHING, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Branches=Branches, 
         CustomData=CustomData, 
         DestinationArn=DestinationArn, 
         Events=Events, 
         Name=Name, **kwargs)
        (super(Trigger, self).__init__)(**processed_kwargs)


class Repository(troposphere.codecommit.Repository, Mixin):

    def __init__(self, title, template=None, validation=True, RepositoryName=REQUIRED, Code=NOTHING, RepositoryDescription=NOTHING, Tags=NOTHING, Triggers=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         RepositoryName=RepositoryName, 
         Code=Code, 
         RepositoryDescription=RepositoryDescription, 
         Tags=Tags, 
         Triggers=Triggers, **kwargs)
        (super(Repository, self).__init__)(**processed_kwargs)