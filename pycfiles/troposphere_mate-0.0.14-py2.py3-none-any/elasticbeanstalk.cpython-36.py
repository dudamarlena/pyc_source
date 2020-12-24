# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/elasticbeanstalk.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 10323 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.elasticbeanstalk
from troposphere.elasticbeanstalk import ApplicationResourceLifecycleConfig as _ApplicationResourceLifecycleConfig, ApplicationVersionLifecycleConfig as _ApplicationVersionLifecycleConfig, MaxAgeRule as _MaxAgeRule, MaxCountRule as _MaxCountRule, OptionSettings as _OptionSettings, SourceBundle as _SourceBundle, SourceConfiguration as _SourceConfiguration, Tags as _Tags, Tier as _Tier
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class MaxAgeRule(troposphere.elasticbeanstalk.MaxAgeRule, Mixin):

    def __init__(self, title=None, DeleteSourceFromS3=NOTHING, Enabled=NOTHING, MaxAgeInDays=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeleteSourceFromS3=DeleteSourceFromS3, 
         Enabled=Enabled, 
         MaxAgeInDays=MaxAgeInDays, **kwargs)
        (super(MaxAgeRule, self).__init__)(**processed_kwargs)


class MaxCountRule(troposphere.elasticbeanstalk.MaxCountRule, Mixin):

    def __init__(self, title=None, DeleteSourceFromS3=NOTHING, Enabled=NOTHING, MaxCount=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeleteSourceFromS3=DeleteSourceFromS3, 
         Enabled=Enabled, 
         MaxCount=MaxCount, **kwargs)
        (super(MaxCountRule, self).__init__)(**processed_kwargs)


class ApplicationVersionLifecycleConfig(troposphere.elasticbeanstalk.ApplicationVersionLifecycleConfig, Mixin):

    def __init__(self, title=None, MaxAgeRule=NOTHING, MaxCountRule=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MaxAgeRule=MaxAgeRule, 
         MaxCountRule=MaxCountRule, **kwargs)
        (super(ApplicationVersionLifecycleConfig, self).__init__)(**processed_kwargs)


class SourceBundle(troposphere.elasticbeanstalk.SourceBundle, Mixin):

    def __init__(self, title=None, S3Bucket=REQUIRED, S3Key=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         S3Bucket=S3Bucket, 
         S3Key=S3Key, **kwargs)
        (super(SourceBundle, self).__init__)(**processed_kwargs)


class SourceConfiguration(troposphere.elasticbeanstalk.SourceConfiguration, Mixin):

    def __init__(self, title=None, ApplicationName=REQUIRED, TemplateName=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ApplicationName=ApplicationName, 
         TemplateName=TemplateName, **kwargs)
        (super(SourceConfiguration, self).__init__)(**processed_kwargs)


class ApplicationResourceLifecycleConfig(troposphere.elasticbeanstalk.ApplicationResourceLifecycleConfig, Mixin):

    def __init__(self, title=None, ServiceRole=NOTHING, VersionLifecycleConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ServiceRole=ServiceRole, 
         VersionLifecycleConfig=VersionLifecycleConfig, **kwargs)
        (super(ApplicationResourceLifecycleConfig, self).__init__)(**processed_kwargs)


class OptionSettings(troposphere.elasticbeanstalk.OptionSettings, Mixin):

    def __init__(self, title=None, Namespace=REQUIRED, OptionName=REQUIRED, Value=REQUIRED, ResourceName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Namespace=Namespace, 
         OptionName=OptionName, 
         Value=Value, 
         ResourceName=ResourceName, **kwargs)
        (super(OptionSettings, self).__init__)(**processed_kwargs)


class Application(troposphere.elasticbeanstalk.Application, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationName=NOTHING, Description=NOTHING, ResourceLifecycleConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationName=ApplicationName, 
         Description=Description, 
         ResourceLifecycleConfig=ResourceLifecycleConfig, **kwargs)
        (super(Application, self).__init__)(**processed_kwargs)


class ApplicationVersion(troposphere.elasticbeanstalk.ApplicationVersion, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationName=REQUIRED, Description=NOTHING, SourceBundle=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationName=ApplicationName, 
         Description=Description, 
         SourceBundle=SourceBundle, **kwargs)
        (super(ApplicationVersion, self).__init__)(**processed_kwargs)


class ConfigurationTemplate(troposphere.elasticbeanstalk.ConfigurationTemplate, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationName=REQUIRED, Description=NOTHING, EnvironmentId=NOTHING, OptionSettings=NOTHING, PlatformArn=NOTHING, SolutionStackName=NOTHING, SourceConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationName=ApplicationName, 
         Description=Description, 
         EnvironmentId=EnvironmentId, 
         OptionSettings=OptionSettings, 
         PlatformArn=PlatformArn, 
         SolutionStackName=SolutionStackName, 
         SourceConfiguration=SourceConfiguration, **kwargs)
        (super(ConfigurationTemplate, self).__init__)(**processed_kwargs)


class Tier(troposphere.elasticbeanstalk.Tier, Mixin):

    def __init__(self, title=None, Name=NOTHING, Type=NOTHING, Version=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Type=Type, 
         Version=Version, **kwargs)
        (super(Tier, self).__init__)(**processed_kwargs)


class Environment(troposphere.elasticbeanstalk.Environment, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationName=REQUIRED, CNAMEPrefix=NOTHING, Description=NOTHING, EnvironmentName=NOTHING, OptionSettings=NOTHING, PlatformArn=NOTHING, SolutionStackName=NOTHING, Tags=NOTHING, TemplateName=NOTHING, Tier=NOTHING, VersionLabel=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationName=ApplicationName, 
         CNAMEPrefix=CNAMEPrefix, 
         Description=Description, 
         EnvironmentName=EnvironmentName, 
         OptionSettings=OptionSettings, 
         PlatformArn=PlatformArn, 
         SolutionStackName=SolutionStackName, 
         Tags=Tags, 
         TemplateName=TemplateName, 
         Tier=Tier, 
         VersionLabel=VersionLabel, **kwargs)
        (super(Environment, self).__init__)(**processed_kwargs)