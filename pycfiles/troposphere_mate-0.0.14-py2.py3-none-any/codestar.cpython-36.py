# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/codestar.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 2707 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.codestar
from troposphere.codestar import Code as _Code, S3 as _S3
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class S3(troposphere.codestar.S3, Mixin):

    def __init__(self, title=None, Bucket=REQUIRED, Key=REQUIRED, ObjectVersion=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Bucket=Bucket, 
         Key=Key, 
         ObjectVersion=ObjectVersion, **kwargs)
        (super(S3, self).__init__)(**processed_kwargs)


class Code(troposphere.codestar.Code, Mixin):

    def __init__(self, title=None, S3=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         S3=S3, **kwargs)
        (super(Code, self).__init__)(**processed_kwargs)


class GitHubRepository(troposphere.codestar.GitHubRepository, Mixin):

    def __init__(self, title, template=None, validation=True, RepositoryAccessToken=REQUIRED, RepositoryName=REQUIRED, RepositoryOwner=REQUIRED, Code=NOTHING, EnableIssues=NOTHING, IsPrivate=NOTHING, RepositoryDescription=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         RepositoryAccessToken=RepositoryAccessToken, 
         RepositoryName=RepositoryName, 
         RepositoryOwner=RepositoryOwner, 
         Code=Code, 
         EnableIssues=EnableIssues, 
         IsPrivate=IsPrivate, 
         RepositoryDescription=RepositoryDescription, **kwargs)
        (super(GitHubRepository, self).__init__)(**processed_kwargs)