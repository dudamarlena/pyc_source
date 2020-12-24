# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/codepipeline.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 14571 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.codepipeline
from troposphere.codepipeline import ActionTypeId as _ActionTypeId, Actions as _Actions, ArtifactDetails as _ArtifactDetails, ArtifactStore as _ArtifactStore, ArtifactStoreMap as _ArtifactStoreMap, Blockers as _Blockers, ConfigurationProperties as _ConfigurationProperties, DisableInboundStageTransitions as _DisableInboundStageTransitions, EncryptionKey as _EncryptionKey, InputArtifacts as _InputArtifacts, OutputArtifacts as _OutputArtifacts, Settings as _Settings, Stages as _Stages, Tags as _Tags, WebhookAuthConfiguration as _WebhookAuthConfiguration, WebhookFilterRule as _WebhookFilterRule
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class ActionTypeId(troposphere.codepipeline.ActionTypeId, Mixin):

    def __init__(self, title=None, Category=REQUIRED, Owner=REQUIRED, Provider=REQUIRED, Version=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Category=Category, 
         Owner=Owner, 
         Provider=Provider, 
         Version=Version, **kwargs)
        (super(ActionTypeId, self).__init__)(**processed_kwargs)


class ArtifactDetails(troposphere.codepipeline.ArtifactDetails, Mixin):

    def __init__(self, title=None, MaximumCount=REQUIRED, MinimumCount=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MaximumCount=MaximumCount, 
         MinimumCount=MinimumCount, **kwargs)
        (super(ArtifactDetails, self).__init__)(**processed_kwargs)


class Blockers(troposphere.codepipeline.Blockers, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Type=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Type=Type, **kwargs)
        (super(Blockers, self).__init__)(**processed_kwargs)


class ConfigurationProperties(troposphere.codepipeline.ConfigurationProperties, Mixin):

    def __init__(self, title=None, Key=REQUIRED, Name=REQUIRED, Required=REQUIRED, Secret=REQUIRED, Description=NOTHING, Queryable=NOTHING, Type=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Name=Name, 
         Required=Required, 
         Secret=Secret, 
         Description=Description, 
         Queryable=Queryable, 
         Type=Type, **kwargs)
        (super(ConfigurationProperties, self).__init__)(**processed_kwargs)


class EncryptionKey(troposphere.codepipeline.EncryptionKey, Mixin):

    def __init__(self, title=None, Id=REQUIRED, Type=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Id=Id, 
         Type=Type, **kwargs)
        (super(EncryptionKey, self).__init__)(**processed_kwargs)


class DisableInboundStageTransitions(troposphere.codepipeline.DisableInboundStageTransitions, Mixin):

    def __init__(self, title=None, Reason=REQUIRED, StageName=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Reason=Reason, 
         StageName=StageName, **kwargs)
        (super(DisableInboundStageTransitions, self).__init__)(**processed_kwargs)


class InputArtifacts(troposphere.codepipeline.InputArtifacts, Mixin):

    def __init__(self, title=None, Name=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, **kwargs)
        (super(InputArtifacts, self).__init__)(**processed_kwargs)


class OutputArtifacts(troposphere.codepipeline.OutputArtifacts, Mixin):

    def __init__(self, title=None, Name=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, **kwargs)
        (super(OutputArtifacts, self).__init__)(**processed_kwargs)


class Settings(troposphere.codepipeline.Settings, Mixin):

    def __init__(self, title=None, EntityUrlTemplate=NOTHING, ExecutionUrlTemplate=NOTHING, RevisionUrlTemplate=NOTHING, ThirdPartyConfigurationUrl=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EntityUrlTemplate=EntityUrlTemplate, 
         ExecutionUrlTemplate=ExecutionUrlTemplate, 
         RevisionUrlTemplate=RevisionUrlTemplate, 
         ThirdPartyConfigurationUrl=ThirdPartyConfigurationUrl, **kwargs)
        (super(Settings, self).__init__)(**processed_kwargs)


class ArtifactStore(troposphere.codepipeline.ArtifactStore, Mixin):

    def __init__(self, title=None, Location=REQUIRED, Type=REQUIRED, EncryptionKey=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Location=Location, 
         Type=Type, 
         EncryptionKey=EncryptionKey, **kwargs)
        (super(ArtifactStore, self).__init__)(**processed_kwargs)


class ArtifactStoreMap(troposphere.codepipeline.ArtifactStoreMap, Mixin):

    def __init__(self, title=None, ArtifactStore=REQUIRED, Region=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ArtifactStore=ArtifactStore, 
         Region=Region, **kwargs)
        (super(ArtifactStoreMap, self).__init__)(**processed_kwargs)


class Actions(troposphere.codepipeline.Actions, Mixin):

    def __init__(self, title=None, ActionTypeId=REQUIRED, Name=REQUIRED, Configuration=NOTHING, InputArtifacts=NOTHING, Namespace=NOTHING, OutputArtifacts=NOTHING, Region=NOTHING, RoleArn=NOTHING, RunOrder=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ActionTypeId=ActionTypeId, 
         Name=Name, 
         Configuration=Configuration, 
         InputArtifacts=InputArtifacts, 
         Namespace=Namespace, 
         OutputArtifacts=OutputArtifacts, 
         Region=Region, 
         RoleArn=RoleArn, 
         RunOrder=RunOrder, **kwargs)
        (super(Actions, self).__init__)(**processed_kwargs)


class Stages(troposphere.codepipeline.Stages, Mixin):

    def __init__(self, title=None, Actions=REQUIRED, Name=REQUIRED, Blockers=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Actions=Actions, 
         Name=Name, 
         Blockers=Blockers, **kwargs)
        (super(Stages, self).__init__)(**processed_kwargs)


class CustomActionType(troposphere.codepipeline.CustomActionType, Mixin):

    def __init__(self, title, template=None, validation=True, Category=REQUIRED, InputArtifactDetails=REQUIRED, OutputArtifactDetails=REQUIRED, Provider=REQUIRED, ConfigurationProperties=NOTHING, Settings=NOTHING, Tags=NOTHING, Version=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Category=Category, 
         InputArtifactDetails=InputArtifactDetails, 
         OutputArtifactDetails=OutputArtifactDetails, 
         Provider=Provider, 
         ConfigurationProperties=ConfigurationProperties, 
         Settings=Settings, 
         Tags=Tags, 
         Version=Version, **kwargs)
        (super(CustomActionType, self).__init__)(**processed_kwargs)


class Pipeline(troposphere.codepipeline.Pipeline, Mixin):

    def __init__(self, title, template=None, validation=True, RoleArn=REQUIRED, Stages=REQUIRED, ArtifactStore=NOTHING, ArtifactStores=NOTHING, DisableInboundStageTransitions=NOTHING, Name=NOTHING, RestartExecutionOnUpdate=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         RoleArn=RoleArn, 
         Stages=Stages, 
         ArtifactStore=ArtifactStore, 
         ArtifactStores=ArtifactStores, 
         DisableInboundStageTransitions=DisableInboundStageTransitions, 
         Name=Name, 
         RestartExecutionOnUpdate=RestartExecutionOnUpdate, 
         Tags=Tags, **kwargs)
        (super(Pipeline, self).__init__)(**processed_kwargs)


class WebhookAuthConfiguration(troposphere.codepipeline.WebhookAuthConfiguration, Mixin):

    def __init__(self, title=None, AllowedIPRange=NOTHING, SecretToken=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AllowedIPRange=AllowedIPRange, 
         SecretToken=SecretToken, **kwargs)
        (super(WebhookAuthConfiguration, self).__init__)(**processed_kwargs)


class WebhookFilterRule(troposphere.codepipeline.WebhookFilterRule, Mixin):

    def __init__(self, title=None, JsonPath=REQUIRED, MatchEquals=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         JsonPath=JsonPath, 
         MatchEquals=MatchEquals, **kwargs)
        (super(WebhookFilterRule, self).__init__)(**processed_kwargs)


class Webhook(troposphere.codepipeline.Webhook, Mixin):

    def __init__(self, title, template=None, validation=True, Authentication=REQUIRED, AuthenticationConfiguration=REQUIRED, Filters=REQUIRED, TargetAction=REQUIRED, TargetPipeline=REQUIRED, TargetPipelineVersion=REQUIRED, Name=NOTHING, RegisterWithThirdParty=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Authentication=Authentication, 
         AuthenticationConfiguration=AuthenticationConfiguration, 
         Filters=Filters, 
         TargetAction=TargetAction, 
         TargetPipeline=TargetPipeline, 
         TargetPipelineVersion=TargetPipelineVersion, 
         Name=Name, 
         RegisterWithThirdParty=RegisterWithThirdParty, **kwargs)
        (super(Webhook, self).__init__)(**processed_kwargs)