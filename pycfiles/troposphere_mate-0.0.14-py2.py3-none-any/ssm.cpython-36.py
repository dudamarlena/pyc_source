# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/ssm.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 21703 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.ssm
from troposphere.ssm import InstanceAssociationOutputLocation as _InstanceAssociationOutputLocation, LoggingInfo as _LoggingInfo, MaintenanceWindowAutomationParameters as _MaintenanceWindowAutomationParameters, MaintenanceWindowLambdaParameters as _MaintenanceWindowLambdaParameters, MaintenanceWindowRunCommandParameters as _MaintenanceWindowRunCommandParameters, MaintenanceWindowStepFunctionsParameters as _MaintenanceWindowStepFunctionsParameters, NotificationConfig as _NotificationConfig, PatchFilter as _PatchFilter, PatchFilterGroup as _PatchFilterGroup, PatchSource as _PatchSource, Rule as _Rule, RuleGroup as _RuleGroup, S3OutputLocation as _S3OutputLocation, Tags as _Tags, Targets as _Targets, TaskInvocationParameters as _TaskInvocationParameters
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class NotificationConfig(troposphere.ssm.NotificationConfig, Mixin):

    def __init__(self, title=None, NotificationArn=NOTHING, NotificationEvents=NOTHING, NotificationType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         NotificationArn=NotificationArn, 
         NotificationEvents=NotificationEvents, 
         NotificationType=NotificationType, **kwargs)
        (super(NotificationConfig, self).__init__)(**processed_kwargs)


class LoggingInfo(troposphere.ssm.LoggingInfo, Mixin):

    def __init__(self, title=None, Region=REQUIRED, S3Bucket=REQUIRED, S3Prefix=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Region=Region, 
         S3Bucket=S3Bucket, 
         S3Prefix=S3Prefix, **kwargs)
        (super(LoggingInfo, self).__init__)(**processed_kwargs)


class MaintenanceWindowAutomationParameters(troposphere.ssm.MaintenanceWindowAutomationParameters, Mixin):

    def __init__(self, title=None, DocumentVersion=NOTHING, Parameters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DocumentVersion=DocumentVersion, 
         Parameters=Parameters, **kwargs)
        (super(MaintenanceWindowAutomationParameters, self).__init__)(**processed_kwargs)


class MaintenanceWindowLambdaParameters(troposphere.ssm.MaintenanceWindowLambdaParameters, Mixin):

    def __init__(self, title=None, ClientContext=NOTHING, Payload=NOTHING, Qualifier=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ClientContext=ClientContext, 
         Payload=Payload, 
         Qualifier=Qualifier, **kwargs)
        (super(MaintenanceWindowLambdaParameters, self).__init__)(**processed_kwargs)


class MaintenanceWindowRunCommandParameters(troposphere.ssm.MaintenanceWindowRunCommandParameters, Mixin):

    def __init__(self, title=None, Comment=NOTHING, DocumentHash=NOTHING, DocumentHashType=NOTHING, NotificationConfig=NOTHING, OutputS3BucketName=NOTHING, OutputS3KeyPrefix=NOTHING, Parameters=NOTHING, ServiceRoleArn=NOTHING, TimeoutSeconds=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Comment=Comment, 
         DocumentHash=DocumentHash, 
         DocumentHashType=DocumentHashType, 
         NotificationConfig=NotificationConfig, 
         OutputS3BucketName=OutputS3BucketName, 
         OutputS3KeyPrefix=OutputS3KeyPrefix, 
         Parameters=Parameters, 
         ServiceRoleArn=ServiceRoleArn, 
         TimeoutSeconds=TimeoutSeconds, **kwargs)
        (super(MaintenanceWindowRunCommandParameters, self).__init__)(**processed_kwargs)


class MaintenanceWindowStepFunctionsParameters(troposphere.ssm.MaintenanceWindowStepFunctionsParameters, Mixin):

    def __init__(self, title=None, Input=NOTHING, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Input=Input, 
         Name=Name, **kwargs)
        (super(MaintenanceWindowStepFunctionsParameters, self).__init__)(**processed_kwargs)


class PatchFilter(troposphere.ssm.PatchFilter, Mixin):

    def __init__(self, title=None, Key=REQUIRED, Values=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Values=Values, **kwargs)
        (super(PatchFilter, self).__init__)(**processed_kwargs)


class PatchFilterGroup(troposphere.ssm.PatchFilterGroup, Mixin):

    def __init__(self, title=None, PatchFilters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PatchFilters=PatchFilters, **kwargs)
        (super(PatchFilterGroup, self).__init__)(**processed_kwargs)


class Rule(troposphere.ssm.Rule, Mixin):

    def __init__(self, title=None, ApproveAfterDays=NOTHING, ComplianceLevel=NOTHING, EnableNonSecurity=NOTHING, PatchFilterGroup=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ApproveAfterDays=ApproveAfterDays, 
         ComplianceLevel=ComplianceLevel, 
         EnableNonSecurity=EnableNonSecurity, 
         PatchFilterGroup=PatchFilterGroup, **kwargs)
        (super(Rule, self).__init__)(**processed_kwargs)


class RuleGroup(troposphere.ssm.RuleGroup, Mixin):

    def __init__(self, title=None, PatchRules=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PatchRules=PatchRules, **kwargs)
        (super(RuleGroup, self).__init__)(**processed_kwargs)


class TaskInvocationParameters(troposphere.ssm.TaskInvocationParameters, Mixin):

    def __init__(self, title=None, MaintenanceWindowAutomationParameters=NOTHING, MaintenanceWindowLambdaParameters=NOTHING, MaintenanceWindowRunCommandParameters=NOTHING, MaintenanceWindowStepFunctionsParameters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MaintenanceWindowAutomationParameters=MaintenanceWindowAutomationParameters, 
         MaintenanceWindowLambdaParameters=MaintenanceWindowLambdaParameters, 
         MaintenanceWindowRunCommandParameters=MaintenanceWindowRunCommandParameters, 
         MaintenanceWindowStepFunctionsParameters=MaintenanceWindowStepFunctionsParameters, **kwargs)
        (super(TaskInvocationParameters, self).__init__)(**processed_kwargs)


class Targets(troposphere.ssm.Targets, Mixin):

    def __init__(self, title=None, Key=REQUIRED, Values=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Values=Values, **kwargs)
        (super(Targets, self).__init__)(**processed_kwargs)


class S3OutputLocation(troposphere.ssm.S3OutputLocation, Mixin):

    def __init__(self, title=None, OutputS3BucketName=NOTHING, OutputS3KeyPrefix=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         OutputS3BucketName=OutputS3BucketName, 
         OutputS3KeyPrefix=OutputS3KeyPrefix, **kwargs)
        (super(S3OutputLocation, self).__init__)(**processed_kwargs)


class InstanceAssociationOutputLocation(troposphere.ssm.InstanceAssociationOutputLocation, Mixin):

    def __init__(self, title=None, S3Location=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         S3Location=S3Location, **kwargs)
        (super(InstanceAssociationOutputLocation, self).__init__)(**processed_kwargs)


class Association(troposphere.ssm.Association, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, AssociationName=NOTHING, DocumentVersion=NOTHING, InstanceId=NOTHING, OutputLocation=NOTHING, Parameters=NOTHING, ScheduleExpression=NOTHING, Targets=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         AssociationName=AssociationName, 
         DocumentVersion=DocumentVersion, 
         InstanceId=InstanceId, 
         OutputLocation=OutputLocation, 
         Parameters=Parameters, 
         ScheduleExpression=ScheduleExpression, 
         Targets=Targets, **kwargs)
        (super(Association, self).__init__)(**processed_kwargs)


class Document(troposphere.ssm.Document, Mixin):

    def __init__(self, title, template=None, validation=True, Content=REQUIRED, DocumentType=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Content=Content, 
         DocumentType=DocumentType, 
         Tags=Tags, **kwargs)
        (super(Document, self).__init__)(**processed_kwargs)


class MaintenanceWindow(troposphere.ssm.MaintenanceWindow, Mixin):

    def __init__(self, title, template=None, validation=True, AllowUnassociatedTargets=REQUIRED, Cutoff=REQUIRED, Duration=REQUIRED, Name=REQUIRED, Schedule=REQUIRED, Description=NOTHING, EndDate=NOTHING, ScheduleTimezone=NOTHING, StartDate=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AllowUnassociatedTargets=AllowUnassociatedTargets, 
         Cutoff=Cutoff, 
         Duration=Duration, 
         Name=Name, 
         Schedule=Schedule, 
         Description=Description, 
         EndDate=EndDate, 
         ScheduleTimezone=ScheduleTimezone, 
         StartDate=StartDate, 
         Tags=Tags, **kwargs)
        (super(MaintenanceWindow, self).__init__)(**processed_kwargs)


class MaintenanceWindowTarget(troposphere.ssm.MaintenanceWindowTarget, Mixin):

    def __init__(self, title, template=None, validation=True, ResourceType=REQUIRED, Targets=REQUIRED, WindowId=REQUIRED, Description=NOTHING, Name=NOTHING, OwnerInformation=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ResourceType=ResourceType, 
         Targets=Targets, 
         WindowId=WindowId, 
         Description=Description, 
         Name=Name, 
         OwnerInformation=OwnerInformation, **kwargs)
        (super(MaintenanceWindowTarget, self).__init__)(**processed_kwargs)


class MaintenanceWindowTask(troposphere.ssm.MaintenanceWindowTask, Mixin):

    def __init__(self, title, template=None, validation=True, MaxErrors=REQUIRED, Priority=REQUIRED, ServiceRoleArn=REQUIRED, Targets=REQUIRED, TaskArn=REQUIRED, TaskType=REQUIRED, Description=NOTHING, LoggingInfo=NOTHING, MaxConcurrency=NOTHING, Name=NOTHING, TaskInvocationParameters=NOTHING, TaskParameters=NOTHING, WindowId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         MaxErrors=MaxErrors, 
         Priority=Priority, 
         ServiceRoleArn=ServiceRoleArn, 
         Targets=Targets, 
         TaskArn=TaskArn, 
         TaskType=TaskType, 
         Description=Description, 
         LoggingInfo=LoggingInfo, 
         MaxConcurrency=MaxConcurrency, 
         Name=Name, 
         TaskInvocationParameters=TaskInvocationParameters, 
         TaskParameters=TaskParameters, 
         WindowId=WindowId, **kwargs)
        (super(MaintenanceWindowTask, self).__init__)(**processed_kwargs)


class Parameter(troposphere.ssm.Parameter, Mixin):

    def __init__(self, title, template=None, validation=True, Type=REQUIRED, Value=REQUIRED, AllowedPattern=NOTHING, Description=NOTHING, Name=NOTHING, Policies=NOTHING, Tags=NOTHING, Tier=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Type=Type, 
         Value=Value, 
         AllowedPattern=AllowedPattern, 
         Description=Description, 
         Name=Name, 
         Policies=Policies, 
         Tags=Tags, 
         Tier=Tier, **kwargs)
        (super(Parameter, self).__init__)(**processed_kwargs)


class PatchSource(troposphere.ssm.PatchSource, Mixin):

    def __init__(self, title=None, Configuration=NOTHING, Name=NOTHING, Products=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Configuration=Configuration, 
         Name=Name, 
         Products=Products, **kwargs)
        (super(PatchSource, self).__init__)(**processed_kwargs)


class PatchBaseline(troposphere.ssm.PatchBaseline, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, ApprovalRules=NOTHING, ApprovedPatches=NOTHING, ApprovedPatchesComplianceLevel=NOTHING, ApprovedPatchesEnableNonSecurity=NOTHING, Description=NOTHING, GlobalFilters=NOTHING, OperatingSystem=NOTHING, PatchGroups=NOTHING, RejectedPatches=NOTHING, RejectedPatchesAction=NOTHING, Sources=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         ApprovalRules=ApprovalRules, 
         ApprovedPatches=ApprovedPatches, 
         ApprovedPatchesComplianceLevel=ApprovedPatchesComplianceLevel, 
         ApprovedPatchesEnableNonSecurity=ApprovedPatchesEnableNonSecurity, 
         Description=Description, 
         GlobalFilters=GlobalFilters, 
         OperatingSystem=OperatingSystem, 
         PatchGroups=PatchGroups, 
         RejectedPatches=RejectedPatches, 
         RejectedPatchesAction=RejectedPatchesAction, 
         Sources=Sources, 
         Tags=Tags, **kwargs)
        (super(PatchBaseline, self).__init__)(**processed_kwargs)


class ResourceDataSync(troposphere.ssm.ResourceDataSync, Mixin):

    def __init__(self, title, template=None, validation=True, BucketName=REQUIRED, BucketRegion=REQUIRED, SyncFormat=REQUIRED, SyncName=REQUIRED, BucketPrefix=NOTHING, KMSKeyArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         BucketName=BucketName, 
         BucketRegion=BucketRegion, 
         SyncFormat=SyncFormat, 
         SyncName=SyncName, 
         BucketPrefix=BucketPrefix, 
         KMSKeyArn=KMSKeyArn, **kwargs)
        (super(ResourceDataSync, self).__init__)(**processed_kwargs)