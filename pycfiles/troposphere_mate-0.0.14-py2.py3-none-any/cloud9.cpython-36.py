# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/cloud9.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 2278 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.cloud9
from troposphere.cloud9 import Repository as _Repository
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Repository(troposphere.cloud9.Repository, Mixin):

    def __init__(self, title=None, PathComponent=REQUIRED, RepositoryUrl=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PathComponent=PathComponent, 
         RepositoryUrl=RepositoryUrl, **kwargs)
        (super(Repository, self).__init__)(**processed_kwargs)


class EnvironmentEC2(troposphere.cloud9.EnvironmentEC2, Mixin):

    def __init__(self, title, template=None, validation=True, InstanceType=REQUIRED, AutomaticStopTimeMinutes=NOTHING, Description=NOTHING, Name=NOTHING, OwnerArn=NOTHING, Repositories=NOTHING, SubnetId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         InstanceType=InstanceType, 
         AutomaticStopTimeMinutes=AutomaticStopTimeMinutes, 
         Description=Description, 
         Name=Name, 
         OwnerArn=OwnerArn, 
         Repositories=Repositories, 
         SubnetId=SubnetId, **kwargs)
        (super(EnvironmentEC2, self).__init__)(**processed_kwargs)