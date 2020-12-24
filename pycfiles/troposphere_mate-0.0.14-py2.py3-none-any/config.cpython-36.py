# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/config.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 16909 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.config
from troposphere.config import AccountAggregationSources as _AccountAggregationSources, ConfigSnapshotDeliveryProperties as _ConfigSnapshotDeliveryProperties, ExecutionControls as _ExecutionControls, OrganizationAggregationSource as _OrganizationAggregationSource, OrganizationCustomRuleMetadata as _OrganizationCustomRuleMetadata, OrganizationManagedRuleMetadata as _OrganizationManagedRuleMetadata, RecordingGroup as _RecordingGroup, Scope as _Scope, Source as _Source, SourceDetails as _SourceDetails, SsmControls as _SsmControls
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Scope(troposphere.config.Scope, Mixin):

    def __init__(self, title=None, ComplianceResourceId=NOTHING, ComplianceResourceTypes=NOTHING, TagKey=NOTHING, TagValue=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ComplianceResourceId=ComplianceResourceId, 
         ComplianceResourceTypes=ComplianceResourceTypes, 
         TagKey=TagKey, 
         TagValue=TagValue, **kwargs)
        (super(Scope, self).__init__)(**processed_kwargs)


class SourceDetails(troposphere.config.SourceDetails, Mixin):

    def __init__(self, title=None, EventSource=REQUIRED, MessageType=REQUIRED, MaximumExecutionFrequency=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EventSource=EventSource, 
         MessageType=MessageType, 
         MaximumExecutionFrequency=MaximumExecutionFrequency, **kwargs)
        (super(SourceDetails, self).__init__)(**processed_kwargs)


class Source(troposphere.config.Source, Mixin):

    def __init__(self, title=None, Owner=REQUIRED, SourceIdentifier=REQUIRED, SourceDetails=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Owner=Owner, 
         SourceIdentifier=SourceIdentifier, 
         SourceDetails=SourceDetails, **kwargs)
        (super(Source, self).__init__)(**processed_kwargs)


class ConfigRule(troposphere.config.ConfigRule, Mixin):

    def __init__(self, title, template=None, validation=True, Source=REQUIRED, ConfigRuleName=NOTHING, Description=NOTHING, InputParameters=NOTHING, MaximumExecutionFrequency=NOTHING, Scope=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Source=Source, 
         ConfigRuleName=ConfigRuleName, 
         Description=Description, 
         InputParameters=InputParameters, 
         MaximumExecutionFrequency=MaximumExecutionFrequency, 
         Scope=Scope, **kwargs)
        (super(ConfigRule, self).__init__)(**processed_kwargs)


class AggregationAuthorization(troposphere.config.AggregationAuthorization, Mixin):

    def __init__(self, title, template=None, validation=True, AuthorizedAccountId=REQUIRED, AuthorizedAwsRegion=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AuthorizedAccountId=AuthorizedAccountId, 
         AuthorizedAwsRegion=AuthorizedAwsRegion, **kwargs)
        (super(AggregationAuthorization, self).__init__)(**processed_kwargs)


class OrganizationAggregationSource(troposphere.config.OrganizationAggregationSource, Mixin):

    def __init__(self, title=None, RoleArn=REQUIRED, AllAwsRegions=NOTHING, AwsRegions=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RoleArn=RoleArn, 
         AllAwsRegions=AllAwsRegions, 
         AwsRegions=AwsRegions, **kwargs)
        (super(OrganizationAggregationSource, self).__init__)(**processed_kwargs)


class AccountAggregationSources(troposphere.config.AccountAggregationSources, Mixin):

    def __init__(self, title=None, AccountIds=REQUIRED, AllAwsRegions=NOTHING, AwsRegions=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AccountIds=AccountIds, 
         AllAwsRegions=AllAwsRegions, 
         AwsRegions=AwsRegions, **kwargs)
        (super(AccountAggregationSources, self).__init__)(**processed_kwargs)


class ConfigurationAggregator(troposphere.config.ConfigurationAggregator, Mixin):

    def __init__(self, title, template=None, validation=True, ConfigurationAggregatorName=REQUIRED, AccountAggregationSources=NOTHING, OrganizationAggregationSource=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ConfigurationAggregatorName=ConfigurationAggregatorName, 
         AccountAggregationSources=AccountAggregationSources, 
         OrganizationAggregationSource=OrganizationAggregationSource, **kwargs)
        (super(ConfigurationAggregator, self).__init__)(**processed_kwargs)


class RecordingGroup(troposphere.config.RecordingGroup, Mixin):

    def __init__(self, title=None, AllSupported=NOTHING, IncludeGlobalResourceTypes=NOTHING, ResourceTypes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AllSupported=AllSupported, 
         IncludeGlobalResourceTypes=IncludeGlobalResourceTypes, 
         ResourceTypes=ResourceTypes, **kwargs)
        (super(RecordingGroup, self).__init__)(**processed_kwargs)


class ConfigurationRecorder(troposphere.config.ConfigurationRecorder, Mixin):

    def __init__(self, title, template=None, validation=True, RoleARN=REQUIRED, Name=NOTHING, RecordingGroup=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         RoleARN=RoleARN, 
         Name=Name, 
         RecordingGroup=RecordingGroup, **kwargs)
        (super(ConfigurationRecorder, self).__init__)(**processed_kwargs)


class ConfigSnapshotDeliveryProperties(troposphere.config.ConfigSnapshotDeliveryProperties, Mixin):

    def __init__(self, title=None, DeliveryFrequency=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeliveryFrequency=DeliveryFrequency, **kwargs)
        (super(ConfigSnapshotDeliveryProperties, self).__init__)(**processed_kwargs)


class DeliveryChannel(troposphere.config.DeliveryChannel, Mixin):

    def __init__(self, title, template=None, validation=True, S3BucketName=REQUIRED, ConfigSnapshotDeliveryProperties=NOTHING, Name=NOTHING, S3KeyPrefix=NOTHING, SnsTopicARN=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         S3BucketName=S3BucketName, 
         ConfigSnapshotDeliveryProperties=ConfigSnapshotDeliveryProperties, 
         Name=Name, 
         S3KeyPrefix=S3KeyPrefix, 
         SnsTopicARN=SnsTopicARN, **kwargs)
        (super(DeliveryChannel, self).__init__)(**processed_kwargs)


class OrganizationCustomRuleMetadata(troposphere.config.OrganizationCustomRuleMetadata, Mixin):

    def __init__(self, title=None, LambdaFunctionArn=REQUIRED, OrganizationConfigRuleTriggerTypes=REQUIRED, Description=NOTHING, InputParameters=NOTHING, MaximumExecutionFrequency=NOTHING, ResourceIdScope=NOTHING, ResourceTypesScope=NOTHING, TagKeyScope=NOTHING, TagValueScope=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LambdaFunctionArn=LambdaFunctionArn, 
         OrganizationConfigRuleTriggerTypes=OrganizationConfigRuleTriggerTypes, 
         Description=Description, 
         InputParameters=InputParameters, 
         MaximumExecutionFrequency=MaximumExecutionFrequency, 
         ResourceIdScope=ResourceIdScope, 
         ResourceTypesScope=ResourceTypesScope, 
         TagKeyScope=TagKeyScope, 
         TagValueScope=TagValueScope, **kwargs)
        (super(OrganizationCustomRuleMetadata, self).__init__)(**processed_kwargs)


class OrganizationManagedRuleMetadata(troposphere.config.OrganizationManagedRuleMetadata, Mixin):

    def __init__(self, title=None, RuleIdentifier=REQUIRED, Description=NOTHING, InputParameters=NOTHING, MaximumExecutionFrequency=NOTHING, ResourceIdScope=NOTHING, ResourceTypesScope=NOTHING, TagKeyScope=NOTHING, TagValueScope=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RuleIdentifier=RuleIdentifier, 
         Description=Description, 
         InputParameters=InputParameters, 
         MaximumExecutionFrequency=MaximumExecutionFrequency, 
         ResourceIdScope=ResourceIdScope, 
         ResourceTypesScope=ResourceTypesScope, 
         TagKeyScope=TagKeyScope, 
         TagValueScope=TagValueScope, **kwargs)
        (super(OrganizationManagedRuleMetadata, self).__init__)(**processed_kwargs)


class OrganizationConfigRule(troposphere.config.OrganizationConfigRule, Mixin):

    def __init__(self, title, template=None, validation=True, OrganizationConfigRuleName=REQUIRED, ExcludedAccounts=NOTHING, OrganizationCustomRuleMetadata=NOTHING, OrganizationManagedRuleMetadata=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         OrganizationConfigRuleName=OrganizationConfigRuleName, 
         ExcludedAccounts=ExcludedAccounts, 
         OrganizationCustomRuleMetadata=OrganizationCustomRuleMetadata, 
         OrganizationManagedRuleMetadata=OrganizationManagedRuleMetadata, **kwargs)
        (super(OrganizationConfigRule, self).__init__)(**processed_kwargs)


class SsmControls(troposphere.config.SsmControls, Mixin):

    def __init__(self, title=None, ConcurrentExecutionRatePercentage=NOTHING, ErrorPercentage=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ConcurrentExecutionRatePercentage=ConcurrentExecutionRatePercentage, 
         ErrorPercentage=ErrorPercentage, **kwargs)
        (super(SsmControls, self).__init__)(**processed_kwargs)


class ExecutionControls(troposphere.config.ExecutionControls, Mixin):

    def __init__(self, title=None, SsmControls=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SsmControls=SsmControls, **kwargs)
        (super(ExecutionControls, self).__init__)(**processed_kwargs)


class RemediationConfiguration(troposphere.config.RemediationConfiguration, Mixin):

    def __init__(self, title, template=None, validation=True, ConfigRuleName=REQUIRED, TargetId=REQUIRED, TargetType=REQUIRED, Automatic=NOTHING, ExecutionControls=NOTHING, MaximumAutomaticAttempts=NOTHING, Parameters=NOTHING, ResourceType=NOTHING, RetryAttemptSeconds=NOTHING, TargetVersion=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ConfigRuleName=ConfigRuleName, 
         TargetId=TargetId, 
         TargetType=TargetType, 
         Automatic=Automatic, 
         ExecutionControls=ExecutionControls, 
         MaximumAutomaticAttempts=MaximumAutomaticAttempts, 
         Parameters=Parameters, 
         ResourceType=ResourceType, 
         RetryAttemptSeconds=RetryAttemptSeconds, 
         TargetVersion=TargetVersion, **kwargs)
        (super(RemediationConfiguration, self).__init__)(**processed_kwargs)