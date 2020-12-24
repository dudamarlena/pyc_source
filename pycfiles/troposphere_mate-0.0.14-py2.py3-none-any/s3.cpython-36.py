# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/s3.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 35167 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.s3
from troposphere.s3 import AbortIncompleteMultipartUpload as _AbortIncompleteMultipartUpload, AccelerateConfiguration as _AccelerateConfiguration, AccessControlTranslation as _AccessControlTranslation, AnalyticsConfiguration as _AnalyticsConfiguration, BucketEncryption as _BucketEncryption, CorsConfiguration as _CorsConfiguration, CorsRules as _CorsRules, DataExport as _DataExport, DefaultRetention as _DefaultRetention, Destination as _Destination, EncryptionConfiguration as _EncryptionConfiguration, Filter as _Filter, InventoryConfiguration as _InventoryConfiguration, LambdaConfigurations as _LambdaConfigurations, LifecycleConfiguration as _LifecycleConfiguration, LifecycleRule as _LifecycleRule, LifecycleRuleTransition as _LifecycleRuleTransition, LoggingConfiguration as _LoggingConfiguration, MetricsConfiguration as _MetricsConfiguration, NoncurrentVersionTransition as _NoncurrentVersionTransition, NotificationConfiguration as _NotificationConfiguration, ObjectLockConfiguration as _ObjectLockConfiguration, ObjectLockRule as _ObjectLockRule, PublicAccessBlockConfiguration as _PublicAccessBlockConfiguration, QueueConfigurations as _QueueConfigurations, RedirectAllRequestsTo as _RedirectAllRequestsTo, RedirectRule as _RedirectRule, ReplicationConfiguration as _ReplicationConfiguration, ReplicationConfigurationRules as _ReplicationConfigurationRules, ReplicationConfigurationRulesDestination as _ReplicationConfigurationRulesDestination, RoutingRule as _RoutingRule, RoutingRuleCondition as _RoutingRuleCondition, Rules as _Rules, S3Key as _S3Key, ServerSideEncryptionByDefault as _ServerSideEncryptionByDefault, ServerSideEncryptionRule as _ServerSideEncryptionRule, SourceSelectionCriteria as _SourceSelectionCriteria, SseKmsEncryptedObjects as _SseKmsEncryptedObjects, StorageClassAnalysis as _StorageClassAnalysis, TagFilter as _TagFilter, Tags as _Tags, TopicConfigurations as _TopicConfigurations, VersioningConfiguration as _VersioningConfiguration, VpcConfiguration as _VpcConfiguration, WebsiteConfiguration as _WebsiteConfiguration
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class PublicAccessBlockConfiguration(troposphere.s3.PublicAccessBlockConfiguration, Mixin):

    def __init__(self, title=None, BlockPublicAcls=NOTHING, BlockPublicPolicy=NOTHING, IgnorePublicAcls=NOTHING, RestrictPublicBuckets=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BlockPublicAcls=BlockPublicAcls, 
         BlockPublicPolicy=BlockPublicPolicy, 
         IgnorePublicAcls=IgnorePublicAcls, 
         RestrictPublicBuckets=RestrictPublicBuckets, **kwargs)
        (super(PublicAccessBlockConfiguration, self).__init__)(**processed_kwargs)


class VpcConfiguration(troposphere.s3.VpcConfiguration, Mixin):

    def __init__(self, title=None, VpcId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         VpcId=VpcId, **kwargs)
        (super(VpcConfiguration, self).__init__)(**processed_kwargs)


class AccessPoint(troposphere.s3.AccessPoint, Mixin):

    def __init__(self, title, template=None, validation=True, Bucket=REQUIRED, CreationDate=NOTHING, Name=NOTHING, NetworkOrigin=NOTHING, Policy=NOTHING, PolicyStatus=NOTHING, PublicAccessBlockConfiguration=NOTHING, VpcConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Bucket=Bucket, 
         CreationDate=CreationDate, 
         Name=Name, 
         NetworkOrigin=NetworkOrigin, 
         Policy=Policy, 
         PolicyStatus=PolicyStatus, 
         PublicAccessBlockConfiguration=PublicAccessBlockConfiguration, 
         VpcConfiguration=VpcConfiguration, **kwargs)
        (super(AccessPoint, self).__init__)(**processed_kwargs)


class CorsRules(troposphere.s3.CorsRules, Mixin):

    def __init__(self, title=None, AllowedMethods=REQUIRED, AllowedOrigins=REQUIRED, AllowedHeaders=NOTHING, ExposedHeaders=NOTHING, Id=NOTHING, MaxAge=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AllowedMethods=AllowedMethods, 
         AllowedOrigins=AllowedOrigins, 
         AllowedHeaders=AllowedHeaders, 
         ExposedHeaders=ExposedHeaders, 
         Id=Id, 
         MaxAge=MaxAge, **kwargs)
        (super(CorsRules, self).__init__)(**processed_kwargs)


class CorsConfiguration(troposphere.s3.CorsConfiguration, Mixin):

    def __init__(self, title=None, CorsRules=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CorsRules=CorsRules, **kwargs)
        (super(CorsConfiguration, self).__init__)(**processed_kwargs)


class VersioningConfiguration(troposphere.s3.VersioningConfiguration, Mixin):

    def __init__(self, title=None, Status=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Status=Status, **kwargs)
        (super(VersioningConfiguration, self).__init__)(**processed_kwargs)


class AccelerateConfiguration(troposphere.s3.AccelerateConfiguration, Mixin):

    def __init__(self, title=None, AccelerationStatus=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AccelerationStatus=AccelerationStatus, **kwargs)
        (super(AccelerateConfiguration, self).__init__)(**processed_kwargs)


class RedirectAllRequestsTo(troposphere.s3.RedirectAllRequestsTo, Mixin):

    def __init__(self, title=None, HostName=REQUIRED, Protocol=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HostName=HostName, 
         Protocol=Protocol, **kwargs)
        (super(RedirectAllRequestsTo, self).__init__)(**processed_kwargs)


class RedirectRule(troposphere.s3.RedirectRule, Mixin):

    def __init__(self, title=None, HostName=NOTHING, HttpRedirectCode=NOTHING, Protocol=NOTHING, ReplaceKeyPrefixWith=NOTHING, ReplaceKeyWith=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HostName=HostName, 
         HttpRedirectCode=HttpRedirectCode, 
         Protocol=Protocol, 
         ReplaceKeyPrefixWith=ReplaceKeyPrefixWith, 
         ReplaceKeyWith=ReplaceKeyWith, **kwargs)
        (super(RedirectRule, self).__init__)(**processed_kwargs)


class RoutingRuleCondition(troposphere.s3.RoutingRuleCondition, Mixin):

    def __init__(self, title=None, HttpErrorCodeReturnedEquals=NOTHING, KeyPrefixEquals=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HttpErrorCodeReturnedEquals=HttpErrorCodeReturnedEquals, 
         KeyPrefixEquals=KeyPrefixEquals, **kwargs)
        (super(RoutingRuleCondition, self).__init__)(**processed_kwargs)


class RoutingRule(troposphere.s3.RoutingRule, Mixin):

    def __init__(self, title=None, RedirectRule=REQUIRED, RoutingRuleCondition=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RedirectRule=RedirectRule, 
         RoutingRuleCondition=RoutingRuleCondition, **kwargs)
        (super(RoutingRule, self).__init__)(**processed_kwargs)


class WebsiteConfiguration(troposphere.s3.WebsiteConfiguration, Mixin):

    def __init__(self, title=None, IndexDocument=NOTHING, ErrorDocument=NOTHING, RedirectAllRequestsTo=NOTHING, RoutingRules=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         IndexDocument=IndexDocument, 
         ErrorDocument=ErrorDocument, 
         RedirectAllRequestsTo=RedirectAllRequestsTo, 
         RoutingRules=RoutingRules, **kwargs)
        (super(WebsiteConfiguration, self).__init__)(**processed_kwargs)


class LifecycleRuleTransition(troposphere.s3.LifecycleRuleTransition, Mixin):

    def __init__(self, title=None, StorageClass=REQUIRED, TransitionDate=NOTHING, TransitionInDays=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         StorageClass=StorageClass, 
         TransitionDate=TransitionDate, 
         TransitionInDays=TransitionInDays, **kwargs)
        (super(LifecycleRuleTransition, self).__init__)(**processed_kwargs)


class AbortIncompleteMultipartUpload(troposphere.s3.AbortIncompleteMultipartUpload, Mixin):

    def __init__(self, title=None, DaysAfterInitiation=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DaysAfterInitiation=DaysAfterInitiation, **kwargs)
        (super(AbortIncompleteMultipartUpload, self).__init__)(**processed_kwargs)


class NoncurrentVersionTransition(troposphere.s3.NoncurrentVersionTransition, Mixin):

    def __init__(self, title=None, StorageClass=REQUIRED, TransitionInDays=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         StorageClass=StorageClass, 
         TransitionInDays=TransitionInDays, **kwargs)
        (super(NoncurrentVersionTransition, self).__init__)(**processed_kwargs)


class TagFilter(troposphere.s3.TagFilter, Mixin):

    def __init__(self, title=None, Key=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Value=Value, **kwargs)
        (super(TagFilter, self).__init__)(**processed_kwargs)


class LifecycleRule(troposphere.s3.LifecycleRule, Mixin):

    def __init__(self, title=None, Status=REQUIRED, AbortIncompleteMultipartUpload=NOTHING, ExpirationDate=NOTHING, ExpirationInDays=NOTHING, Id=NOTHING, NoncurrentVersionExpirationInDays=NOTHING, NoncurrentVersionTransition=NOTHING, NoncurrentVersionTransitions=NOTHING, Prefix=NOTHING, TagFilters=NOTHING, Transition=NOTHING, Transitions=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Status=Status, 
         AbortIncompleteMultipartUpload=AbortIncompleteMultipartUpload, 
         ExpirationDate=ExpirationDate, 
         ExpirationInDays=ExpirationInDays, 
         Id=Id, 
         NoncurrentVersionExpirationInDays=NoncurrentVersionExpirationInDays, 
         NoncurrentVersionTransition=NoncurrentVersionTransition, 
         NoncurrentVersionTransitions=NoncurrentVersionTransitions, 
         Prefix=Prefix, 
         TagFilters=TagFilters, 
         Transition=Transition, 
         Transitions=Transitions, **kwargs)
        (super(LifecycleRule, self).__init__)(**processed_kwargs)


class LifecycleConfiguration(troposphere.s3.LifecycleConfiguration, Mixin):

    def __init__(self, title=None, Rules=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Rules=Rules, **kwargs)
        (super(LifecycleConfiguration, self).__init__)(**processed_kwargs)


class LoggingConfiguration(troposphere.s3.LoggingConfiguration, Mixin):

    def __init__(self, title=None, DestinationBucketName=NOTHING, LogFilePrefix=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DestinationBucketName=DestinationBucketName, 
         LogFilePrefix=LogFilePrefix, **kwargs)
        (super(LoggingConfiguration, self).__init__)(**processed_kwargs)


class Rules(troposphere.s3.Rules, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Value=Value, **kwargs)
        (super(Rules, self).__init__)(**processed_kwargs)


class S3Key(troposphere.s3.S3Key, Mixin):

    def __init__(self, title=None, Rules=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Rules=Rules, **kwargs)
        (super(S3Key, self).__init__)(**processed_kwargs)


class Filter(troposphere.s3.Filter, Mixin):

    def __init__(self, title=None, S3Key=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         S3Key=S3Key, **kwargs)
        (super(Filter, self).__init__)(**processed_kwargs)


class LambdaConfigurations(troposphere.s3.LambdaConfigurations, Mixin):

    def __init__(self, title=None, Event=REQUIRED, Function=REQUIRED, Filter=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Event=Event, 
         Function=Function, 
         Filter=Filter, **kwargs)
        (super(LambdaConfigurations, self).__init__)(**processed_kwargs)


class QueueConfigurations(troposphere.s3.QueueConfigurations, Mixin):

    def __init__(self, title=None, Event=REQUIRED, Queue=REQUIRED, Filter=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Event=Event, 
         Queue=Queue, 
         Filter=Filter, **kwargs)
        (super(QueueConfigurations, self).__init__)(**processed_kwargs)


class TopicConfigurations(troposphere.s3.TopicConfigurations, Mixin):

    def __init__(self, title=None, Event=REQUIRED, Topic=REQUIRED, Filter=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Event=Event, 
         Topic=Topic, 
         Filter=Filter, **kwargs)
        (super(TopicConfigurations, self).__init__)(**processed_kwargs)


class MetricsConfiguration(troposphere.s3.MetricsConfiguration, Mixin):

    def __init__(self, title=None, Id=REQUIRED, Prefix=NOTHING, TagFilters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Id=Id, 
         Prefix=Prefix, 
         TagFilters=TagFilters, **kwargs)
        (super(MetricsConfiguration, self).__init__)(**processed_kwargs)


class NotificationConfiguration(troposphere.s3.NotificationConfiguration, Mixin):

    def __init__(self, title=None, LambdaConfigurations=NOTHING, QueueConfigurations=NOTHING, TopicConfigurations=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LambdaConfigurations=LambdaConfigurations, 
         QueueConfigurations=QueueConfigurations, 
         TopicConfigurations=TopicConfigurations, **kwargs)
        (super(NotificationConfiguration, self).__init__)(**processed_kwargs)


class AccessControlTranslation(troposphere.s3.AccessControlTranslation, Mixin):

    def __init__(self, title=None, Owner=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Owner=Owner, **kwargs)
        (super(AccessControlTranslation, self).__init__)(**processed_kwargs)


class EncryptionConfiguration(troposphere.s3.EncryptionConfiguration, Mixin):

    def __init__(self, title=None, ReplicaKmsKeyID=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ReplicaKmsKeyID=ReplicaKmsKeyID, **kwargs)
        (super(EncryptionConfiguration, self).__init__)(**processed_kwargs)


class ReplicationConfigurationRulesDestination(troposphere.s3.ReplicationConfigurationRulesDestination, Mixin):

    def __init__(self, title=None, Bucket=REQUIRED, AccessControlTranslation=NOTHING, Account=NOTHING, EncryptionConfiguration=NOTHING, StorageClass=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Bucket=Bucket, 
         AccessControlTranslation=AccessControlTranslation, 
         Account=Account, 
         EncryptionConfiguration=EncryptionConfiguration, 
         StorageClass=StorageClass, **kwargs)
        (super(ReplicationConfigurationRulesDestination, self).__init__)(**processed_kwargs)


class SseKmsEncryptedObjects(troposphere.s3.SseKmsEncryptedObjects, Mixin):

    def __init__(self, title=None, Status=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Status=Status, **kwargs)
        (super(SseKmsEncryptedObjects, self).__init__)(**processed_kwargs)


class SourceSelectionCriteria(troposphere.s3.SourceSelectionCriteria, Mixin):

    def __init__(self, title=None, SseKmsEncryptedObjects=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SseKmsEncryptedObjects=SseKmsEncryptedObjects, **kwargs)
        (super(SourceSelectionCriteria, self).__init__)(**processed_kwargs)


class ReplicationConfigurationRules(troposphere.s3.ReplicationConfigurationRules, Mixin):

    def __init__(self, title=None, Destination=REQUIRED, Prefix=REQUIRED, Status=REQUIRED, Id=NOTHING, SourceSelectionCriteria=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Destination=Destination, 
         Prefix=Prefix, 
         Status=Status, 
         Id=Id, 
         SourceSelectionCriteria=SourceSelectionCriteria, **kwargs)
        (super(ReplicationConfigurationRules, self).__init__)(**processed_kwargs)


class ReplicationConfiguration(troposphere.s3.ReplicationConfiguration, Mixin):

    def __init__(self, title=None, Role=REQUIRED, Rules=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Role=Role, 
         Rules=Rules, **kwargs)
        (super(ReplicationConfiguration, self).__init__)(**processed_kwargs)


class Destination(troposphere.s3.Destination, Mixin):

    def __init__(self, title=None, BucketArn=REQUIRED, Format=REQUIRED, BucketAccountId=NOTHING, Prefix=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BucketArn=BucketArn, 
         Format=Format, 
         BucketAccountId=BucketAccountId, 
         Prefix=Prefix, **kwargs)
        (super(Destination, self).__init__)(**processed_kwargs)


class DataExport(troposphere.s3.DataExport, Mixin):

    def __init__(self, title=None, Destination=REQUIRED, OutputSchemaVersion=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Destination=Destination, 
         OutputSchemaVersion=OutputSchemaVersion, **kwargs)
        (super(DataExport, self).__init__)(**processed_kwargs)


class StorageClassAnalysis(troposphere.s3.StorageClassAnalysis, Mixin):

    def __init__(self, title=None, DataExport=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DataExport=DataExport, **kwargs)
        (super(StorageClassAnalysis, self).__init__)(**processed_kwargs)


class AnalyticsConfiguration(troposphere.s3.AnalyticsConfiguration, Mixin):

    def __init__(self, title=None, Id=REQUIRED, StorageClassAnalysis=REQUIRED, Prefix=NOTHING, TagFilters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Id=Id, 
         StorageClassAnalysis=StorageClassAnalysis, 
         Prefix=Prefix, 
         TagFilters=TagFilters, **kwargs)
        (super(AnalyticsConfiguration, self).__init__)(**processed_kwargs)


class ServerSideEncryptionByDefault(troposphere.s3.ServerSideEncryptionByDefault, Mixin):

    def __init__(self, title=None, SSEAlgorithm=REQUIRED, KMSMasterKeyID=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SSEAlgorithm=SSEAlgorithm, 
         KMSMasterKeyID=KMSMasterKeyID, **kwargs)
        (super(ServerSideEncryptionByDefault, self).__init__)(**processed_kwargs)


class ServerSideEncryptionRule(troposphere.s3.ServerSideEncryptionRule, Mixin):

    def __init__(self, title=None, ServerSideEncryptionByDefault=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ServerSideEncryptionByDefault=ServerSideEncryptionByDefault, **kwargs)
        (super(ServerSideEncryptionRule, self).__init__)(**processed_kwargs)


class BucketEncryption(troposphere.s3.BucketEncryption, Mixin):

    def __init__(self, title=None, ServerSideEncryptionConfiguration=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ServerSideEncryptionConfiguration=ServerSideEncryptionConfiguration, **kwargs)
        (super(BucketEncryption, self).__init__)(**processed_kwargs)


class InventoryConfiguration(troposphere.s3.InventoryConfiguration, Mixin):

    def __init__(self, title=None, Destination=REQUIRED, Enabled=REQUIRED, Id=REQUIRED, IncludedObjectVersions=REQUIRED, OptionalFields=REQUIRED, ScheduleFrequency=REQUIRED, Prefix=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Destination=Destination, 
         Enabled=Enabled, 
         Id=Id, 
         IncludedObjectVersions=IncludedObjectVersions, 
         OptionalFields=OptionalFields, 
         ScheduleFrequency=ScheduleFrequency, 
         Prefix=Prefix, **kwargs)
        (super(InventoryConfiguration, self).__init__)(**processed_kwargs)


class DefaultRetention(troposphere.s3.DefaultRetention, Mixin):

    def __init__(self, title=None, Days=NOTHING, Mode=NOTHING, Years=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Days=Days, 
         Mode=Mode, 
         Years=Years, **kwargs)
        (super(DefaultRetention, self).__init__)(**processed_kwargs)


class ObjectLockRule(troposphere.s3.ObjectLockRule, Mixin):

    def __init__(self, title=None, DefaultRetention=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DefaultRetention=DefaultRetention, **kwargs)
        (super(ObjectLockRule, self).__init__)(**processed_kwargs)


class ObjectLockConfiguration(troposphere.s3.ObjectLockConfiguration, Mixin):

    def __init__(self, title=None, ObjectLockEnabled=NOTHING, Rule=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ObjectLockEnabled=ObjectLockEnabled, 
         Rule=Rule, **kwargs)
        (super(ObjectLockConfiguration, self).__init__)(**processed_kwargs)


class PublicAccessBlockConfiguration(troposphere.s3.PublicAccessBlockConfiguration, Mixin):

    def __init__(self, title=None, BlockPublicAcls=NOTHING, BlockPublicPolicy=NOTHING, IgnorePublicAcls=NOTHING, RestrictPublicBuckets=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BlockPublicAcls=BlockPublicAcls, 
         BlockPublicPolicy=BlockPublicPolicy, 
         IgnorePublicAcls=IgnorePublicAcls, 
         RestrictPublicBuckets=RestrictPublicBuckets, **kwargs)
        (super(PublicAccessBlockConfiguration, self).__init__)(**processed_kwargs)


class Bucket(troposphere.s3.Bucket, Mixin):

    def __init__(self, title, template=None, validation=True, AccessControl=NOTHING, AccelerateConfiguration=NOTHING, AnalyticsConfigurations=NOTHING, BucketEncryption=NOTHING, BucketName=NOTHING, CorsConfiguration=NOTHING, InventoryConfigurations=NOTHING, LifecycleConfiguration=NOTHING, LoggingConfiguration=NOTHING, MetricsConfigurations=NOTHING, NotificationConfiguration=NOTHING, ObjectLockConfiguration=NOTHING, ObjectLockEnabled=NOTHING, PublicAccessBlockConfiguration=NOTHING, ReplicationConfiguration=NOTHING, Tags=NOTHING, WebsiteConfiguration=NOTHING, VersioningConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AccessControl=AccessControl, 
         AccelerateConfiguration=AccelerateConfiguration, 
         AnalyticsConfigurations=AnalyticsConfigurations, 
         BucketEncryption=BucketEncryption, 
         BucketName=BucketName, 
         CorsConfiguration=CorsConfiguration, 
         InventoryConfigurations=InventoryConfigurations, 
         LifecycleConfiguration=LifecycleConfiguration, 
         LoggingConfiguration=LoggingConfiguration, 
         MetricsConfigurations=MetricsConfigurations, 
         NotificationConfiguration=NotificationConfiguration, 
         ObjectLockConfiguration=ObjectLockConfiguration, 
         ObjectLockEnabled=ObjectLockEnabled, 
         PublicAccessBlockConfiguration=PublicAccessBlockConfiguration, 
         ReplicationConfiguration=ReplicationConfiguration, 
         Tags=Tags, 
         WebsiteConfiguration=WebsiteConfiguration, 
         VersioningConfiguration=VersioningConfiguration, **kwargs)
        (super(Bucket, self).__init__)(**processed_kwargs)


class BucketPolicy(troposphere.s3.BucketPolicy, Mixin):

    def __init__(self, title, template=None, validation=True, Bucket=REQUIRED, PolicyDocument=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Bucket=Bucket, 
         PolicyDocument=PolicyDocument, **kwargs)
        (super(BucketPolicy, self).__init__)(**processed_kwargs)