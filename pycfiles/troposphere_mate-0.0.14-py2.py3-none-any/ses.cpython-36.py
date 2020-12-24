# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/ses.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 15270 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.ses
from troposphere.ses import Action as _Action, AddHeaderAction as _AddHeaderAction, BounceAction as _BounceAction, CloudWatchDestination as _CloudWatchDestination, DimensionConfiguration as _DimensionConfiguration, EmailTemplate as _EmailTemplate, EventDestination as _EventDestination, Filter as _Filter, IpFilter as _IpFilter, KinesisFirehoseDestination as _KinesisFirehoseDestination, LambdaAction as _LambdaAction, Rule as _Rule, S3Action as _S3Action, SNSAction as _SNSAction, StopAction as _StopAction, WorkmailAction as _WorkmailAction
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class DimensionConfiguration(troposphere.ses.DimensionConfiguration, Mixin):

    def __init__(self, title=None, DefaultDimensionValue=REQUIRED, DimensionName=REQUIRED, DimensionValueSource=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DefaultDimensionValue=DefaultDimensionValue, 
         DimensionName=DimensionName, 
         DimensionValueSource=DimensionValueSource, **kwargs)
        (super(DimensionConfiguration, self).__init__)(**processed_kwargs)


class CloudWatchDestination(troposphere.ses.CloudWatchDestination, Mixin):

    def __init__(self, title=None, DimensionConfigurations=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DimensionConfigurations=DimensionConfigurations, **kwargs)
        (super(CloudWatchDestination, self).__init__)(**processed_kwargs)


class KinesisFirehoseDestination(troposphere.ses.KinesisFirehoseDestination, Mixin):

    def __init__(self, title=None, DeliveryStreamARN=REQUIRED, IAMRoleARN=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeliveryStreamARN=DeliveryStreamARN, 
         IAMRoleARN=IAMRoleARN, **kwargs)
        (super(KinesisFirehoseDestination, self).__init__)(**processed_kwargs)


class EventDestination(troposphere.ses.EventDestination, Mixin):

    def __init__(self, title=None, MatchingEventTypes=REQUIRED, CloudWatchDestination=NOTHING, Enabled=NOTHING, KinesisFirehoseDestination=NOTHING, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MatchingEventTypes=MatchingEventTypes, 
         CloudWatchDestination=CloudWatchDestination, 
         Enabled=Enabled, 
         KinesisFirehoseDestination=KinesisFirehoseDestination, 
         Name=Name, **kwargs)
        (super(EventDestination, self).__init__)(**processed_kwargs)


class ConfigurationSetEventDestination(troposphere.ses.ConfigurationSetEventDestination, Mixin):

    def __init__(self, title, template=None, validation=True, ConfigurationSetName=REQUIRED, EventDestination=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ConfigurationSetName=ConfigurationSetName, 
         EventDestination=EventDestination, **kwargs)
        (super(ConfigurationSetEventDestination, self).__init__)(**processed_kwargs)


class ConfigurationSet(troposphere.ses.ConfigurationSet, Mixin):

    def __init__(self, title, template=None, validation=True, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, **kwargs)
        (super(ConfigurationSet, self).__init__)(**processed_kwargs)


class IpFilter(troposphere.ses.IpFilter, Mixin):

    def __init__(self, title=None, Cidr=REQUIRED, Policy=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Cidr=Cidr, 
         Policy=Policy, **kwargs)
        (super(IpFilter, self).__init__)(**processed_kwargs)


class Filter(troposphere.ses.Filter, Mixin):

    def __init__(self, title=None, IpFilter=REQUIRED, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         IpFilter=IpFilter, 
         Name=Name, **kwargs)
        (super(Filter, self).__init__)(**processed_kwargs)


class ReceiptFilter(troposphere.ses.ReceiptFilter, Mixin):

    def __init__(self, title, template=None, validation=True, Filter=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Filter=Filter, **kwargs)
        (super(ReceiptFilter, self).__init__)(**processed_kwargs)


class ReceiptRuleSet(troposphere.ses.ReceiptRuleSet, Mixin):

    def __init__(self, title, template=None, validation=True, RuleSetName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         RuleSetName=RuleSetName, **kwargs)
        (super(ReceiptRuleSet, self).__init__)(**processed_kwargs)


class AddHeaderAction(troposphere.ses.AddHeaderAction, Mixin):

    def __init__(self, title=None, HeaderName=REQUIRED, HeaderValue=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HeaderName=HeaderName, 
         HeaderValue=HeaderValue, **kwargs)
        (super(AddHeaderAction, self).__init__)(**processed_kwargs)


class BounceAction(troposphere.ses.BounceAction, Mixin):

    def __init__(self, title=None, Message=REQUIRED, Sender=REQUIRED, SmtpReplyCode=REQUIRED, StatusCode=NOTHING, TopicArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Message=Message, 
         Sender=Sender, 
         SmtpReplyCode=SmtpReplyCode, 
         StatusCode=StatusCode, 
         TopicArn=TopicArn, **kwargs)
        (super(BounceAction, self).__init__)(**processed_kwargs)


class LambdaAction(troposphere.ses.LambdaAction, Mixin):

    def __init__(self, title=None, FunctionArn=REQUIRED, InvocationType=NOTHING, TopicArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FunctionArn=FunctionArn, 
         InvocationType=InvocationType, 
         TopicArn=TopicArn, **kwargs)
        (super(LambdaAction, self).__init__)(**processed_kwargs)


class S3Action(troposphere.ses.S3Action, Mixin):

    def __init__(self, title=None, BucketName=REQUIRED, KmsKeyArn=NOTHING, ObjectKeyPrefix=NOTHING, TopicArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BucketName=BucketName, 
         KmsKeyArn=KmsKeyArn, 
         ObjectKeyPrefix=ObjectKeyPrefix, 
         TopicArn=TopicArn, **kwargs)
        (super(S3Action, self).__init__)(**processed_kwargs)


class SNSAction(troposphere.ses.SNSAction, Mixin):

    def __init__(self, title=None, Encoding=NOTHING, TopicArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Encoding=Encoding, 
         TopicArn=TopicArn, **kwargs)
        (super(SNSAction, self).__init__)(**processed_kwargs)


class StopAction(troposphere.ses.StopAction, Mixin):

    def __init__(self, title=None, Scope=REQUIRED, TopicArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Scope=Scope, 
         TopicArn=TopicArn, **kwargs)
        (super(StopAction, self).__init__)(**processed_kwargs)


class WorkmailAction(troposphere.ses.WorkmailAction, Mixin):

    def __init__(self, title=None, OrganizationArn=REQUIRED, TopicArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         OrganizationArn=OrganizationArn, 
         TopicArn=TopicArn, **kwargs)
        (super(WorkmailAction, self).__init__)(**processed_kwargs)


class Action(troposphere.ses.Action, Mixin):

    def __init__(self, title=None, AddHeaderAction=NOTHING, BounceAction=NOTHING, LambdaAction=NOTHING, S3Action=NOTHING, SNSAction=NOTHING, StopAction=NOTHING, WorkmailAction=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AddHeaderAction=AddHeaderAction, 
         BounceAction=BounceAction, 
         LambdaAction=LambdaAction, 
         S3Action=S3Action, 
         SNSAction=SNSAction, 
         StopAction=StopAction, 
         WorkmailAction=WorkmailAction, **kwargs)
        (super(Action, self).__init__)(**processed_kwargs)


class Rule(troposphere.ses.Rule, Mixin):

    def __init__(self, title=None, Actions=NOTHING, Enabled=NOTHING, Name=NOTHING, Recipients=NOTHING, ScanEnabled=NOTHING, TlsPolicy=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Actions=Actions, 
         Enabled=Enabled, 
         Name=Name, 
         Recipients=Recipients, 
         ScanEnabled=ScanEnabled, 
         TlsPolicy=TlsPolicy, **kwargs)
        (super(Rule, self).__init__)(**processed_kwargs)


class ReceiptRule(troposphere.ses.ReceiptRule, Mixin):

    def __init__(self, title, template=None, validation=True, Rule=REQUIRED, RuleSetName=REQUIRED, After=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Rule=Rule, 
         RuleSetName=RuleSetName, 
         After=After, **kwargs)
        (super(ReceiptRule, self).__init__)(**processed_kwargs)


class EmailTemplate(troposphere.ses.EmailTemplate, Mixin):

    def __init__(self, title=None, HtmlPart=NOTHING, SubjectPart=NOTHING, TemplateName=NOTHING, TextPart=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HtmlPart=HtmlPart, 
         SubjectPart=SubjectPart, 
         TemplateName=TemplateName, 
         TextPart=TextPart, **kwargs)
        (super(EmailTemplate, self).__init__)(**processed_kwargs)


class Template(troposphere.ses.Template, Mixin):

    def __init__(self, title, template=None, validation=True, Template=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Template=Template, **kwargs)
        (super(Template, self).__init__)(**processed_kwargs)