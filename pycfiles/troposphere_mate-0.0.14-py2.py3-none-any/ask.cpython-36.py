# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/ask.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 3306 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.ask
from troposphere.ask import AuthenticationConfiguration as _AuthenticationConfiguration, Overrides as _Overrides, SkillPackage as _SkillPackage
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Overrides(troposphere.ask.Overrides, Mixin):

    def __init__(self, title=None, Manifest=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Manifest=Manifest, **kwargs)
        (super(Overrides, self).__init__)(**processed_kwargs)


class AuthenticationConfiguration(troposphere.ask.AuthenticationConfiguration, Mixin):

    def __init__(self, title=None, ClientId=REQUIRED, ClientSecret=REQUIRED, RefreshToken=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ClientId=ClientId, 
         ClientSecret=ClientSecret, 
         RefreshToken=RefreshToken, **kwargs)
        (super(AuthenticationConfiguration, self).__init__)(**processed_kwargs)


class SkillPackage(troposphere.ask.SkillPackage, Mixin):

    def __init__(self, title=None, S3Bucket=REQUIRED, S3Key=REQUIRED, Overrides=NOTHING, S3BucketRole=NOTHING, S3ObjectVersion=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         S3Bucket=S3Bucket, 
         S3Key=S3Key, 
         Overrides=Overrides, 
         S3BucketRole=S3BucketRole, 
         S3ObjectVersion=S3ObjectVersion, **kwargs)
        (super(SkillPackage, self).__init__)(**processed_kwargs)


class Skill(troposphere.ask.Skill, Mixin):

    def __init__(self, title, template=None, validation=True, AuthenticationConfiguration=REQUIRED, SkillPackage=REQUIRED, VendorId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AuthenticationConfiguration=AuthenticationConfiguration, 
         SkillPackage=SkillPackage, 
         VendorId=VendorId, **kwargs)
        (super(Skill, self).__init__)(**processed_kwargs)