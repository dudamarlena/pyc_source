# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/backup.py
# Compiled at: 2020-02-12 18:15:54
# Size of source mod 2**32: 7594 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.backup
from troposphere.backup import BackupPlanResourceType as _BackupPlanResourceType, BackupRuleResourceType as _BackupRuleResourceType, BackupSelectionResourceType as _BackupSelectionResourceType, ConditionResourceType as _ConditionResourceType, LifecycleResourceType as _LifecycleResourceType, NotificationObjectType as _NotificationObjectType
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class LifecycleResourceType(troposphere.backup.LifecycleResourceType, Mixin):

    def __init__(self, title=None, DeleteAfterDays=NOTHING, MoveToColdStorageAfterDays=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeleteAfterDays=DeleteAfterDays, 
         MoveToColdStorageAfterDays=MoveToColdStorageAfterDays, **kwargs)
        (super(LifecycleResourceType, self).__init__)(**processed_kwargs)


class BackupRuleResourceType(troposphere.backup.BackupRuleResourceType, Mixin):

    def __init__(self, title=None, RuleName=REQUIRED, TargetBackupVault=REQUIRED, CompletionWindowMinutes=NOTHING, Lifecycle=NOTHING, RecoveryPointTags=NOTHING, ScheduleExpression=NOTHING, StartWindowMinutes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RuleName=RuleName, 
         TargetBackupVault=TargetBackupVault, 
         CompletionWindowMinutes=CompletionWindowMinutes, 
         Lifecycle=Lifecycle, 
         RecoveryPointTags=RecoveryPointTags, 
         ScheduleExpression=ScheduleExpression, 
         StartWindowMinutes=StartWindowMinutes, **kwargs)
        (super(BackupRuleResourceType, self).__init__)(**processed_kwargs)


class BackupPlanResourceType(troposphere.backup.BackupPlanResourceType, Mixin):

    def __init__(self, title=None, BackupPlanName=REQUIRED, BackupPlanRule=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BackupPlanName=BackupPlanName, 
         BackupPlanRule=BackupPlanRule, **kwargs)
        (super(BackupPlanResourceType, self).__init__)(**processed_kwargs)


class BackupPlan(troposphere.backup.BackupPlan, Mixin):

    def __init__(self, title, template=None, validation=True, BackupPlan=REQUIRED, BackupPlanTags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         BackupPlan=BackupPlan, 
         BackupPlanTags=BackupPlanTags, **kwargs)
        (super(BackupPlan, self).__init__)(**processed_kwargs)


class ConditionResourceType(troposphere.backup.ConditionResourceType, Mixin):

    def __init__(self, title=None, ConditionKey=REQUIRED, ConditionType=REQUIRED, ConditionValue=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ConditionKey=ConditionKey, 
         ConditionType=ConditionType, 
         ConditionValue=ConditionValue, **kwargs)
        (super(ConditionResourceType, self).__init__)(**processed_kwargs)


class BackupSelectionResourceType(troposphere.backup.BackupSelectionResourceType, Mixin):

    def __init__(self, title=None, IamRoleArn=REQUIRED, SelectionName=REQUIRED, ListOfTags=NOTHING, Resources=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         IamRoleArn=IamRoleArn, 
         SelectionName=SelectionName, 
         ListOfTags=ListOfTags, 
         Resources=Resources, **kwargs)
        (super(BackupSelectionResourceType, self).__init__)(**processed_kwargs)


class BackupSelection(troposphere.backup.BackupSelection, Mixin):

    def __init__(self, title, template=None, validation=True, BackupPlanId=REQUIRED, BackupSelection=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         BackupPlanId=BackupPlanId, 
         BackupSelection=BackupSelection, **kwargs)
        (super(BackupSelection, self).__init__)(**processed_kwargs)


class NotificationObjectType(troposphere.backup.NotificationObjectType, Mixin):

    def __init__(self, title=None, BackupVaultEvents=REQUIRED, SNSTopicArn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BackupVaultEvents=BackupVaultEvents, 
         SNSTopicArn=SNSTopicArn, **kwargs)
        (super(NotificationObjectType, self).__init__)(**processed_kwargs)


class BackupVault(troposphere.backup.BackupVault, Mixin):

    def __init__(self, title, template=None, validation=True, BackupVaultName=REQUIRED, AccessPolicy=NOTHING, BackupVaultTags=NOTHING, EncryptionKeyArn=NOTHING, Notifications=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         BackupVaultName=BackupVaultName, 
         AccessPolicy=AccessPolicy, 
         BackupVaultTags=BackupVaultTags, 
         EncryptionKeyArn=EncryptionKeyArn, 
         Notifications=Notifications, **kwargs)
        (super(BackupVault, self).__init__)(**processed_kwargs)