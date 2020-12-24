# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/amplify.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 8716 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.amplify
from troposphere.amplify import AutoBranchCreationConfig as _AutoBranchCreationConfig, BasicAuthConfig as _BasicAuthConfig, CustomRule as _CustomRule, EnvironmentVariable as _EnvironmentVariable, SubDomainSetting as _SubDomainSetting, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class BasicAuthConfig(troposphere.amplify.BasicAuthConfig, Mixin):

    def __init__(self, title=None, Password=REQUIRED, Username=REQUIRED, EnableBasicAuth=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Password=Password, 
         Username=Username, 
         EnableBasicAuth=EnableBasicAuth, **kwargs)
        (super(BasicAuthConfig, self).__init__)(**processed_kwargs)


class EnvironmentVariable(troposphere.amplify.EnvironmentVariable, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Value=Value, **kwargs)
        (super(EnvironmentVariable, self).__init__)(**processed_kwargs)


class AutoBranchCreationConfig(troposphere.amplify.AutoBranchCreationConfig, Mixin):

    def __init__(self, title=None, AutoBranchCreationPatterns=NOTHING, BasicAuthConfig=NOTHING, BuildSpec=NOTHING, EnableAutoBranchCreation=NOTHING, EnableAutoBuild=NOTHING, EnablePullRequestPreview=NOTHING, EnvironmentVariables=NOTHING, PullRequestEnvironmentName=NOTHING, Stage=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AutoBranchCreationPatterns=AutoBranchCreationPatterns, 
         BasicAuthConfig=BasicAuthConfig, 
         BuildSpec=BuildSpec, 
         EnableAutoBranchCreation=EnableAutoBranchCreation, 
         EnableAutoBuild=EnableAutoBuild, 
         EnablePullRequestPreview=EnablePullRequestPreview, 
         EnvironmentVariables=EnvironmentVariables, 
         PullRequestEnvironmentName=PullRequestEnvironmentName, 
         Stage=Stage, **kwargs)
        (super(AutoBranchCreationConfig, self).__init__)(**processed_kwargs)


class CustomRule(troposphere.amplify.CustomRule, Mixin):

    def __init__(self, title=None, Source=REQUIRED, Target=REQUIRED, Condition=NOTHING, Status=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Source=Source, 
         Target=Target, 
         Condition=Condition, 
         Status=Status, **kwargs)
        (super(CustomRule, self).__init__)(**processed_kwargs)


class App(troposphere.amplify.App, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, AccessToken=NOTHING, AutoBranchCreationConfig=NOTHING, BasicAuthConfig=NOTHING, BuildSpec=NOTHING, CustomRules=NOTHING, Description=NOTHING, EnvironmentVariables=NOTHING, IAMServiceRole=NOTHING, OauthToken=NOTHING, Repository=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         AccessToken=AccessToken, 
         AutoBranchCreationConfig=AutoBranchCreationConfig, 
         BasicAuthConfig=BasicAuthConfig, 
         BuildSpec=BuildSpec, 
         CustomRules=CustomRules, 
         Description=Description, 
         EnvironmentVariables=EnvironmentVariables, 
         IAMServiceRole=IAMServiceRole, 
         OauthToken=OauthToken, 
         Repository=Repository, 
         Tags=Tags, **kwargs)
        (super(App, self).__init__)(**processed_kwargs)


class Branch(troposphere.amplify.Branch, Mixin):

    def __init__(self, title, template=None, validation=True, AppId=REQUIRED, BranchName=REQUIRED, BasicAuthConfig=NOTHING, BuildSpec=NOTHING, Description=NOTHING, EnableAutoBuild=NOTHING, EnablePullRequestPreview=NOTHING, EnvironmentVariables=NOTHING, PullRequestEnvironmentName=NOTHING, Stage=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AppId=AppId, 
         BranchName=BranchName, 
         BasicAuthConfig=BasicAuthConfig, 
         BuildSpec=BuildSpec, 
         Description=Description, 
         EnableAutoBuild=EnableAutoBuild, 
         EnablePullRequestPreview=EnablePullRequestPreview, 
         EnvironmentVariables=EnvironmentVariables, 
         PullRequestEnvironmentName=PullRequestEnvironmentName, 
         Stage=Stage, 
         Tags=Tags, **kwargs)
        (super(Branch, self).__init__)(**processed_kwargs)


class SubDomainSetting(troposphere.amplify.SubDomainSetting, Mixin):

    def __init__(self, title=None, BranchName=REQUIRED, Prefix=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BranchName=BranchName, 
         Prefix=Prefix, **kwargs)
        (super(SubDomainSetting, self).__init__)(**processed_kwargs)


class Domain(troposphere.amplify.Domain, Mixin):

    def __init__(self, title, template=None, validation=True, AppId=REQUIRED, DomainName=REQUIRED, SubDomainSettings=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AppId=AppId, 
         DomainName=DomainName, 
         SubDomainSettings=SubDomainSettings, **kwargs)
        (super(Domain, self).__init__)(**processed_kwargs)