# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/codebuild.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 13339 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.codebuild
from troposphere.codebuild import Artifacts as _Artifacts, CloudWatchLogs as _CloudWatchLogs, Environment as _Environment, GitSubmodulesConfig as _GitSubmodulesConfig, LogsConfig as _LogsConfig, ProjectCache as _ProjectCache, ProjectSourceVersion as _ProjectSourceVersion, ProjectTriggers as _ProjectTriggers, RegistryCredential as _RegistryCredential, S3Logs as _S3Logs, Source as _Source, SourceAuth as _SourceAuth, Tags as _Tags, VpcConfig as _VpcConfig
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class SourceAuth(troposphere.codebuild.SourceAuth, Mixin):

    def __init__(self, title=None, Type=REQUIRED, Resource=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         Resource=Resource, **kwargs)
        (super(SourceAuth, self).__init__)(**processed_kwargs)


class Artifacts(troposphere.codebuild.Artifacts, Mixin):

    def __init__(self, title=None, Type=REQUIRED, ArtifactIdentifier=NOTHING, EncryptionDisabled=NOTHING, Location=NOTHING, Name=NOTHING, NamespaceType=NOTHING, OverrideArtifactName=NOTHING, Packaging=NOTHING, Path=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         ArtifactIdentifier=ArtifactIdentifier, 
         EncryptionDisabled=EncryptionDisabled, 
         Location=Location, 
         Name=Name, 
         NamespaceType=NamespaceType, 
         OverrideArtifactName=OverrideArtifactName, 
         Packaging=Packaging, 
         Path=Path, **kwargs)
        (super(Artifacts, self).__init__)(**processed_kwargs)


class EnvironmentVariable(troposphere.codebuild.EnvironmentVariable, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Value=REQUIRED, Type=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Value=Value, 
         Type=Type, **kwargs)
        (super(EnvironmentVariable, self).__init__)(**processed_kwargs)


class RegistryCredential(troposphere.codebuild.RegistryCredential, Mixin):

    def __init__(self, title=None, Credential=REQUIRED, CredentialProvider=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Credential=Credential, 
         CredentialProvider=CredentialProvider, **kwargs)
        (super(RegistryCredential, self).__init__)(**processed_kwargs)


class Environment(troposphere.codebuild.Environment, Mixin):

    def __init__(self, title=None, ComputeType=REQUIRED, Image=REQUIRED, Type=REQUIRED, Certificate=NOTHING, ImagePullCredentialsType=NOTHING, PrivilegedMode=NOTHING, RegistryCredential=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ComputeType=ComputeType, 
         Image=Image, 
         Type=Type, 
         Certificate=Certificate, 
         ImagePullCredentialsType=ImagePullCredentialsType, 
         PrivilegedMode=PrivilegedMode, 
         RegistryCredential=RegistryCredential, **kwargs)
        (super(Environment, self).__init__)(**processed_kwargs)


class ProjectCache(troposphere.codebuild.ProjectCache, Mixin):

    def __init__(self, title=None, Type=REQUIRED, Location=NOTHING, Modes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         Location=Location, 
         Modes=Modes, **kwargs)
        (super(ProjectCache, self).__init__)(**processed_kwargs)


class GitSubmodulesConfig(troposphere.codebuild.GitSubmodulesConfig, Mixin):

    def __init__(self, title=None, FetchSubmodules=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FetchSubmodules=FetchSubmodules, **kwargs)
        (super(GitSubmodulesConfig, self).__init__)(**processed_kwargs)


class Source(troposphere.codebuild.Source, Mixin):

    def __init__(self, title=None, Type=REQUIRED, Auth=NOTHING, BuildSpec=NOTHING, GitCloneDepth=NOTHING, GitSubmodulesConfig=NOTHING, InsecureSsl=NOTHING, Location=NOTHING, ReportBuildStatus=NOTHING, SourceIdentifier=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         Auth=Auth, 
         BuildSpec=BuildSpec, 
         GitCloneDepth=GitCloneDepth, 
         GitSubmodulesConfig=GitSubmodulesConfig, 
         InsecureSsl=InsecureSsl, 
         Location=Location, 
         ReportBuildStatus=ReportBuildStatus, 
         SourceIdentifier=SourceIdentifier, **kwargs)
        (super(Source, self).__init__)(**processed_kwargs)


class VpcConfig(troposphere.codebuild.VpcConfig, Mixin):

    def __init__(self, title=None, SecurityGroupIds=REQUIRED, Subnets=REQUIRED, VpcId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SecurityGroupIds=SecurityGroupIds, 
         Subnets=Subnets, 
         VpcId=VpcId, **kwargs)
        (super(VpcConfig, self).__init__)(**processed_kwargs)


class WebhookFilter(troposphere.codebuild.WebhookFilter, Mixin):

    def __init__(self, title=None, Pattern=REQUIRED, Type=REQUIRED, ExcludeMatchedPattern=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Pattern=Pattern, 
         Type=Type, 
         ExcludeMatchedPattern=ExcludeMatchedPattern, **kwargs)
        (super(WebhookFilter, self).__init__)(**processed_kwargs)


class ProjectTriggers(troposphere.codebuild.ProjectTriggers, Mixin):

    def __init__(self, title=None, Webhook=NOTHING, FilterGroups=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Webhook=Webhook, 
         FilterGroups=FilterGroups, **kwargs)
        (super(ProjectTriggers, self).__init__)(**processed_kwargs)


class CloudWatchLogs(troposphere.codebuild.CloudWatchLogs, Mixin):

    def __init__(self, title=None, Status=REQUIRED, GroupName=NOTHING, StreamName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Status=Status, 
         GroupName=GroupName, 
         StreamName=StreamName, **kwargs)
        (super(CloudWatchLogs, self).__init__)(**processed_kwargs)


class S3Logs(troposphere.codebuild.S3Logs, Mixin):

    def __init__(self, title=None, Status=REQUIRED, EncryptionDisabled=NOTHING, Location=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Status=Status, 
         EncryptionDisabled=EncryptionDisabled, 
         Location=Location, **kwargs)
        (super(S3Logs, self).__init__)(**processed_kwargs)


class LogsConfig(troposphere.codebuild.LogsConfig, Mixin):

    def __init__(self, title=None, CloudWatchLogs=NOTHING, S3Logs=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CloudWatchLogs=CloudWatchLogs, 
         S3Logs=S3Logs, **kwargs)
        (super(LogsConfig, self).__init__)(**processed_kwargs)


class ProjectSourceVersion(troposphere.codebuild.ProjectSourceVersion, Mixin):

    def __init__(self, title=None, SourceIdentifier=REQUIRED, SourceVersion=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SourceIdentifier=SourceIdentifier, 
         SourceVersion=SourceVersion, **kwargs)
        (super(ProjectSourceVersion, self).__init__)(**processed_kwargs)


class Project(troposphere.codebuild.Project, Mixin):

    def __init__(self, title, template=None, validation=True, Artifacts=REQUIRED, Environment=REQUIRED, ServiceRole=REQUIRED, Source=REQUIRED, BadgeEnabled=NOTHING, Cache=NOTHING, Description=NOTHING, EncryptionKey=NOTHING, LogsConfig=NOTHING, Name=NOTHING, SecondaryArtifacts=NOTHING, SecondarySourceVersions=NOTHING, SecondarySources=NOTHING, SourceVersion=NOTHING, Tags=NOTHING, TimeoutInMinutes=NOTHING, Triggers=NOTHING, VpcConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Artifacts=Artifacts, 
         Environment=Environment, 
         ServiceRole=ServiceRole, 
         Source=Source, 
         BadgeEnabled=BadgeEnabled, 
         Cache=Cache, 
         Description=Description, 
         EncryptionKey=EncryptionKey, 
         LogsConfig=LogsConfig, 
         Name=Name, 
         SecondaryArtifacts=SecondaryArtifacts, 
         SecondarySourceVersions=SecondarySourceVersions, 
         SecondarySources=SecondarySources, 
         SourceVersion=SourceVersion, 
         Tags=Tags, 
         TimeoutInMinutes=TimeoutInMinutes, 
         Triggers=Triggers, 
         VpcConfig=VpcConfig, **kwargs)
        (super(Project, self).__init__)(**processed_kwargs)