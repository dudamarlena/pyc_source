# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/secretsmanager.py
# Compiled at: 2020-02-12 18:15:54
# Size of source mod 2**32: 5929 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.secretsmanager
from troposphere.secretsmanager import GenerateSecretString as _GenerateSecretString, RotationRules as _RotationRules, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class ResourcePolicy(troposphere.secretsmanager.ResourcePolicy, Mixin):

    def __init__(self, title, template=None, validation=True, SecretId=REQUIRED, ResourcePolicy=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         SecretId=SecretId, 
         ResourcePolicy=ResourcePolicy, **kwargs)
        (super(ResourcePolicy, self).__init__)(**processed_kwargs)


class RotationRules(troposphere.secretsmanager.RotationRules, Mixin):

    def __init__(self, title=None, AutomaticallyAfterDays=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AutomaticallyAfterDays=AutomaticallyAfterDays, **kwargs)
        (super(RotationRules, self).__init__)(**processed_kwargs)


class RotationSchedule(troposphere.secretsmanager.RotationSchedule, Mixin):

    def __init__(self, title, template=None, validation=True, SecretId=REQUIRED, RotationLambdaARN=REQUIRED, RotationRules=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         SecretId=SecretId, 
         RotationLambdaARN=RotationLambdaARN, 
         RotationRules=RotationRules, **kwargs)
        (super(RotationSchedule, self).__init__)(**processed_kwargs)


class SecretTargetAttachment(troposphere.secretsmanager.SecretTargetAttachment, Mixin):

    def __init__(self, title, template=None, validation=True, SecretId=REQUIRED, TargetId=REQUIRED, TargetType=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         SecretId=SecretId, 
         TargetId=TargetId, 
         TargetType=TargetType, **kwargs)
        (super(SecretTargetAttachment, self).__init__)(**processed_kwargs)


class GenerateSecretString(troposphere.secretsmanager.GenerateSecretString, Mixin):

    def __init__(self, title=None, ExcludeUppercase=NOTHING, RequireEachIncludedType=NOTHING, IncludeSpace=NOTHING, ExcludeCharacters=NOTHING, GenerateStringKey=NOTHING, PasswordLength=NOTHING, ExcludePunctuation=NOTHING, ExcludeLowercase=NOTHING, SecretStringTemplate=NOTHING, ExcludeNumbers=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ExcludeUppercase=ExcludeUppercase, 
         RequireEachIncludedType=RequireEachIncludedType, 
         IncludeSpace=IncludeSpace, 
         ExcludeCharacters=ExcludeCharacters, 
         GenerateStringKey=GenerateStringKey, 
         PasswordLength=PasswordLength, 
         ExcludePunctuation=ExcludePunctuation, 
         ExcludeLowercase=ExcludeLowercase, 
         SecretStringTemplate=SecretStringTemplate, 
         ExcludeNumbers=ExcludeNumbers, **kwargs)
        (super(GenerateSecretString, self).__init__)(**processed_kwargs)


class Secret(troposphere.secretsmanager.Secret, Mixin):

    def __init__(self, title, template=None, validation=True, Description=NOTHING, KmsKeyId=NOTHING, SecretString=NOTHING, GenerateSecretString=NOTHING, Name=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         KmsKeyId=KmsKeyId, 
         SecretString=SecretString, 
         GenerateSecretString=GenerateSecretString, 
         Name=Name, 
         Tags=Tags, **kwargs)
        (super(Secret, self).__init__)(**processed_kwargs)