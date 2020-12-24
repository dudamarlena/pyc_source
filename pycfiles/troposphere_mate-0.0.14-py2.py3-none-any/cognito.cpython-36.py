# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/cognito.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 39387 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.cognito
from troposphere.cognito import AccountTakeoverActionType as _AccountTakeoverActionType, AccountTakeoverActionsType as _AccountTakeoverActionsType, AccountTakeoverRiskConfigurationType as _AccountTakeoverRiskConfigurationType, AdminCreateUserConfig as _AdminCreateUserConfig, AnalyticsConfiguration as _AnalyticsConfiguration, AttributeType as _AttributeType, CognitoIdentityProvider as _CognitoIdentityProvider, CognitoStreams as _CognitoStreams, CompromisedCredentialsActionsType as _CompromisedCredentialsActionsType, CompromisedCredentialsRiskConfigurationType as _CompromisedCredentialsRiskConfigurationType, CustomDomainConfigType as _CustomDomainConfigType, DeviceConfiguration as _DeviceConfiguration, EmailConfiguration as _EmailConfiguration, InviteMessageTemplate as _InviteMessageTemplate, LambdaConfig as _LambdaConfig, MappingRule as _MappingRule, NotifyConfigurationType as _NotifyConfigurationType, NotifyEmailType as _NotifyEmailType, NumberAttributeConstraints as _NumberAttributeConstraints, PasswordPolicy as _PasswordPolicy, Policies as _Policies, PushSync as _PushSync, ResourceServerScopeType as _ResourceServerScopeType, RiskExceptionConfigurationType as _RiskExceptionConfigurationType, RulesConfiguration as _RulesConfiguration, SchemaAttribute as _SchemaAttribute, SmsConfiguration as _SmsConfiguration, StringAttributeConstraints as _StringAttributeConstraints, UserPoolAddOns as _UserPoolAddOns, VerificationMessageTemplate as _VerificationMessageTemplate
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class CognitoIdentityProvider(troposphere.cognito.CognitoIdentityProvider, Mixin):

    def __init__(self, title=None, ClientId=NOTHING, ProviderName=NOTHING, ServerSideTokenCheck=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ClientId=ClientId, 
         ProviderName=ProviderName, 
         ServerSideTokenCheck=ServerSideTokenCheck, **kwargs)
        (super(CognitoIdentityProvider, self).__init__)(**processed_kwargs)


class CognitoStreams(troposphere.cognito.CognitoStreams, Mixin):

    def __init__(self, title=None, RoleArn=NOTHING, StreamingStatus=NOTHING, StreamName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RoleArn=RoleArn, 
         StreamingStatus=StreamingStatus, 
         StreamName=StreamName, **kwargs)
        (super(CognitoStreams, self).__init__)(**processed_kwargs)


class PushSync(troposphere.cognito.PushSync, Mixin):

    def __init__(self, title=None, ApplicationArns=NOTHING, RoleArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ApplicationArns=ApplicationArns, 
         RoleArn=RoleArn, **kwargs)
        (super(PushSync, self).__init__)(**processed_kwargs)


class IdentityPool(troposphere.cognito.IdentityPool, Mixin):

    def __init__(self, title, template=None, validation=True, AllowUnauthenticatedIdentities=REQUIRED, CognitoEvents=NOTHING, CognitoIdentityProviders=NOTHING, CognitoStreams=NOTHING, DeveloperProviderName=NOTHING, IdentityPoolName=NOTHING, OpenIdConnectProviderARNs=NOTHING, PushSync=NOTHING, SamlProviderARNs=NOTHING, SupportedLoginProviders=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AllowUnauthenticatedIdentities=AllowUnauthenticatedIdentities, 
         CognitoEvents=CognitoEvents, 
         CognitoIdentityProviders=CognitoIdentityProviders, 
         CognitoStreams=CognitoStreams, 
         DeveloperProviderName=DeveloperProviderName, 
         IdentityPoolName=IdentityPoolName, 
         OpenIdConnectProviderARNs=OpenIdConnectProviderARNs, 
         PushSync=PushSync, 
         SamlProviderARNs=SamlProviderARNs, 
         SupportedLoginProviders=SupportedLoginProviders, **kwargs)
        (super(IdentityPool, self).__init__)(**processed_kwargs)


class MappingRule(troposphere.cognito.MappingRule, Mixin):

    def __init__(self, title=None, Claim=REQUIRED, MatchType=REQUIRED, RoleARN=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Claim=Claim, 
         MatchType=MatchType, 
         RoleARN=RoleARN, 
         Value=Value, **kwargs)
        (super(MappingRule, self).__init__)(**processed_kwargs)


class RulesConfiguration(troposphere.cognito.RulesConfiguration, Mixin):

    def __init__(self, title=None, Rules=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Rules=Rules, **kwargs)
        (super(RulesConfiguration, self).__init__)(**processed_kwargs)


class RoleMapping(troposphere.cognito.RoleMapping, Mixin):

    def __init__(self, title=None, Type=REQUIRED, AmbiguousRoleResolution=NOTHING, RulesConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         AmbiguousRoleResolution=AmbiguousRoleResolution, 
         RulesConfiguration=RulesConfiguration, **kwargs)
        (super(RoleMapping, self).__init__)(**processed_kwargs)


class IdentityPoolRoleAttachment(troposphere.cognito.IdentityPoolRoleAttachment, Mixin):

    def __init__(self, title, template=None, validation=True, IdentityPoolId=REQUIRED, RoleMappings=NOTHING, Roles=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         IdentityPoolId=IdentityPoolId, 
         RoleMappings=RoleMappings, 
         Roles=Roles, **kwargs)
        (super(IdentityPoolRoleAttachment, self).__init__)(**processed_kwargs)


class InviteMessageTemplate(troposphere.cognito.InviteMessageTemplate, Mixin):

    def __init__(self, title=None, EmailMessage=NOTHING, EmailSubject=NOTHING, SMSMessage=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EmailMessage=EmailMessage, 
         EmailSubject=EmailSubject, 
         SMSMessage=SMSMessage, **kwargs)
        (super(InviteMessageTemplate, self).__init__)(**processed_kwargs)


class AdminCreateUserConfig(troposphere.cognito.AdminCreateUserConfig, Mixin):

    def __init__(self, title=None, AllowAdminCreateUserOnly=NOTHING, InviteMessageTemplate=NOTHING, UnusedAccountValidityDays=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AllowAdminCreateUserOnly=AllowAdminCreateUserOnly, 
         InviteMessageTemplate=InviteMessageTemplate, 
         UnusedAccountValidityDays=UnusedAccountValidityDays, **kwargs)
        (super(AdminCreateUserConfig, self).__init__)(**processed_kwargs)


class DeviceConfiguration(troposphere.cognito.DeviceConfiguration, Mixin):

    def __init__(self, title=None, ChallengeRequiredOnNewDevice=NOTHING, DeviceOnlyRememberedOnUserPrompt=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ChallengeRequiredOnNewDevice=ChallengeRequiredOnNewDevice, 
         DeviceOnlyRememberedOnUserPrompt=DeviceOnlyRememberedOnUserPrompt, **kwargs)
        (super(DeviceConfiguration, self).__init__)(**processed_kwargs)


class EmailConfiguration(troposphere.cognito.EmailConfiguration, Mixin):

    def __init__(self, title=None, ConfigurationSet=NOTHING, EmailSendingAccount=NOTHING, From=NOTHING, ReplyToEmailAddress=NOTHING, SourceArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ConfigurationSet=ConfigurationSet, 
         EmailSendingAccount=EmailSendingAccount, 
         From=From, 
         ReplyToEmailAddress=ReplyToEmailAddress, 
         SourceArn=SourceArn, **kwargs)
        (super(EmailConfiguration, self).__init__)(**processed_kwargs)


class LambdaConfig(troposphere.cognito.LambdaConfig, Mixin):

    def __init__(self, title=None, CreateAuthChallenge=NOTHING, CustomMessage=NOTHING, DefineAuthChallenge=NOTHING, PostAuthentication=NOTHING, PostConfirmation=NOTHING, PreAuthentication=NOTHING, PreSignUp=NOTHING, PreTokenGeneration=NOTHING, UserMigration=NOTHING, VerifyAuthChallengeResponse=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CreateAuthChallenge=CreateAuthChallenge, 
         CustomMessage=CustomMessage, 
         DefineAuthChallenge=DefineAuthChallenge, 
         PostAuthentication=PostAuthentication, 
         PostConfirmation=PostConfirmation, 
         PreAuthentication=PreAuthentication, 
         PreSignUp=PreSignUp, 
         PreTokenGeneration=PreTokenGeneration, 
         UserMigration=UserMigration, 
         VerifyAuthChallengeResponse=VerifyAuthChallengeResponse, **kwargs)
        (super(LambdaConfig, self).__init__)(**processed_kwargs)


class PasswordPolicy(troposphere.cognito.PasswordPolicy, Mixin):

    def __init__(self, title=None, MinimumLength=NOTHING, RequireLowercase=NOTHING, RequireNumbers=NOTHING, RequireSymbols=NOTHING, RequireUppercase=NOTHING, TemporaryPasswordValidityDays=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MinimumLength=MinimumLength, 
         RequireLowercase=RequireLowercase, 
         RequireNumbers=RequireNumbers, 
         RequireSymbols=RequireSymbols, 
         RequireUppercase=RequireUppercase, 
         TemporaryPasswordValidityDays=TemporaryPasswordValidityDays, **kwargs)
        (super(PasswordPolicy, self).__init__)(**processed_kwargs)


class Policies(troposphere.cognito.Policies, Mixin):

    def __init__(self, title=None, PasswordPolicy=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PasswordPolicy=PasswordPolicy, **kwargs)
        (super(Policies, self).__init__)(**processed_kwargs)


class NumberAttributeConstraints(troposphere.cognito.NumberAttributeConstraints, Mixin):

    def __init__(self, title=None, MaxValue=NOTHING, MinValue=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MaxValue=MaxValue, 
         MinValue=MinValue, **kwargs)
        (super(NumberAttributeConstraints, self).__init__)(**processed_kwargs)


class StringAttributeConstraints(troposphere.cognito.StringAttributeConstraints, Mixin):

    def __init__(self, title=None, MaxLength=NOTHING, MinLength=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MaxLength=MaxLength, 
         MinLength=MinLength, **kwargs)
        (super(StringAttributeConstraints, self).__init__)(**processed_kwargs)


class SchemaAttribute(troposphere.cognito.SchemaAttribute, Mixin):

    def __init__(self, title=None, AttributeDataType=NOTHING, DeveloperOnlyAttribute=NOTHING, Mutable=NOTHING, Name=NOTHING, NumberAttributeConstraints=NOTHING, StringAttributeConstraints=NOTHING, Required=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AttributeDataType=AttributeDataType, 
         DeveloperOnlyAttribute=DeveloperOnlyAttribute, 
         Mutable=Mutable, 
         Name=Name, 
         NumberAttributeConstraints=NumberAttributeConstraints, 
         StringAttributeConstraints=StringAttributeConstraints, 
         Required=Required, **kwargs)
        (super(SchemaAttribute, self).__init__)(**processed_kwargs)


class SmsConfiguration(troposphere.cognito.SmsConfiguration, Mixin):

    def __init__(self, title=None, SnsCallerArn=REQUIRED, ExternalId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SnsCallerArn=SnsCallerArn, 
         ExternalId=ExternalId, **kwargs)
        (super(SmsConfiguration, self).__init__)(**processed_kwargs)


class UserPoolAddOns(troposphere.cognito.UserPoolAddOns, Mixin):

    def __init__(self, title=None, AdvancedSecurityMode=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AdvancedSecurityMode=AdvancedSecurityMode, **kwargs)
        (super(UserPoolAddOns, self).__init__)(**processed_kwargs)


class VerificationMessageTemplate(troposphere.cognito.VerificationMessageTemplate, Mixin):

    def __init__(self, title=None, DefaultEmailOption=NOTHING, EmailMessage=NOTHING, EmailMessageByLink=NOTHING, EmailSubject=NOTHING, EmailSubjectByLink=NOTHING, SmsMessage=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DefaultEmailOption=DefaultEmailOption, 
         EmailMessage=EmailMessage, 
         EmailMessageByLink=EmailMessageByLink, 
         EmailSubject=EmailSubject, 
         EmailSubjectByLink=EmailSubjectByLink, 
         SmsMessage=SmsMessage, **kwargs)
        (super(VerificationMessageTemplate, self).__init__)(**processed_kwargs)


class UserPool(troposphere.cognito.UserPool, Mixin):

    def __init__(self, title, template=None, validation=True, AdminCreateUserConfig=NOTHING, AliasAttributes=NOTHING, AutoVerifiedAttributes=NOTHING, DeviceConfiguration=NOTHING, EmailConfiguration=NOTHING, EmailVerificationMessage=NOTHING, EmailVerificationSubject=NOTHING, EnabledMfas=NOTHING, LambdaConfig=NOTHING, MfaConfiguration=NOTHING, Policies=NOTHING, Schema=NOTHING, SmsAuthenticationMessage=NOTHING, SmsConfiguration=NOTHING, SmsVerificationMessage=NOTHING, UserPoolAddOns=NOTHING, UserPoolName=NOTHING, UserPoolTags=NOTHING, UsernameAttributes=NOTHING, VerificationMessageTemplate=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AdminCreateUserConfig=AdminCreateUserConfig, 
         AliasAttributes=AliasAttributes, 
         AutoVerifiedAttributes=AutoVerifiedAttributes, 
         DeviceConfiguration=DeviceConfiguration, 
         EmailConfiguration=EmailConfiguration, 
         EmailVerificationMessage=EmailVerificationMessage, 
         EmailVerificationSubject=EmailVerificationSubject, 
         EnabledMfas=EnabledMfas, 
         LambdaConfig=LambdaConfig, 
         MfaConfiguration=MfaConfiguration, 
         Policies=Policies, 
         Schema=Schema, 
         SmsAuthenticationMessage=SmsAuthenticationMessage, 
         SmsConfiguration=SmsConfiguration, 
         SmsVerificationMessage=SmsVerificationMessage, 
         UserPoolAddOns=UserPoolAddOns, 
         UserPoolName=UserPoolName, 
         UserPoolTags=UserPoolTags, 
         UsernameAttributes=UsernameAttributes, 
         VerificationMessageTemplate=VerificationMessageTemplate, **kwargs)
        (super(UserPool, self).__init__)(**processed_kwargs)


class AnalyticsConfiguration(troposphere.cognito.AnalyticsConfiguration, Mixin):

    def __init__(self, title=None, ApplicationId=NOTHING, ExternalId=NOTHING, RoleArn=NOTHING, UserDataShared=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ApplicationId=ApplicationId, 
         ExternalId=ExternalId, 
         RoleArn=RoleArn, 
         UserDataShared=UserDataShared, **kwargs)
        (super(AnalyticsConfiguration, self).__init__)(**processed_kwargs)


class UserPoolClient(troposphere.cognito.UserPoolClient, Mixin):

    def __init__(self, title, template=None, validation=True, UserPoolId=REQUIRED, AllowedOAuthFlows=NOTHING, AllowedOAuthFlowsUserPoolClient=NOTHING, AllowedOAuthScopes=NOTHING, AnalyticsConfiguration=NOTHING, CallbackURLs=NOTHING, ClientName=NOTHING, DefaultRedirectURI=NOTHING, ExplicitAuthFlows=NOTHING, GenerateSecret=NOTHING, LogoutURLs=NOTHING, PreventUserExistenceErrors=NOTHING, ReadAttributes=NOTHING, RefreshTokenValidity=NOTHING, SupportedIdentityProviders=NOTHING, WriteAttributes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         UserPoolId=UserPoolId, 
         AllowedOAuthFlows=AllowedOAuthFlows, 
         AllowedOAuthFlowsUserPoolClient=AllowedOAuthFlowsUserPoolClient, 
         AllowedOAuthScopes=AllowedOAuthScopes, 
         AnalyticsConfiguration=AnalyticsConfiguration, 
         CallbackURLs=CallbackURLs, 
         ClientName=ClientName, 
         DefaultRedirectURI=DefaultRedirectURI, 
         ExplicitAuthFlows=ExplicitAuthFlows, 
         GenerateSecret=GenerateSecret, 
         LogoutURLs=LogoutURLs, 
         PreventUserExistenceErrors=PreventUserExistenceErrors, 
         ReadAttributes=ReadAttributes, 
         RefreshTokenValidity=RefreshTokenValidity, 
         SupportedIdentityProviders=SupportedIdentityProviders, 
         WriteAttributes=WriteAttributes, **kwargs)
        (super(UserPoolClient, self).__init__)(**processed_kwargs)


class CustomDomainConfigType(troposphere.cognito.CustomDomainConfigType, Mixin):

    def __init__(self, title=None, CertificateArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CertificateArn=CertificateArn, **kwargs)
        (super(CustomDomainConfigType, self).__init__)(**processed_kwargs)


class UserPoolDomain(troposphere.cognito.UserPoolDomain, Mixin):

    def __init__(self, title, template=None, validation=True, Domain=REQUIRED, UserPoolId=REQUIRED, CustomDomainConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Domain=Domain, 
         UserPoolId=UserPoolId, 
         CustomDomainConfig=CustomDomainConfig, **kwargs)
        (super(UserPoolDomain, self).__init__)(**processed_kwargs)


class UserPoolGroup(troposphere.cognito.UserPoolGroup, Mixin):

    def __init__(self, title, template=None, validation=True, GroupName=REQUIRED, UserPoolId=REQUIRED, Description=NOTHING, Precedence=NOTHING, RoleArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         GroupName=GroupName, 
         UserPoolId=UserPoolId, 
         Description=Description, 
         Precedence=Precedence, 
         RoleArn=RoleArn, **kwargs)
        (super(UserPoolGroup, self).__init__)(**processed_kwargs)


class UserPoolIdentityProvider(troposphere.cognito.UserPoolIdentityProvider, Mixin):

    def __init__(self, title, template=None, validation=True, ProviderName=REQUIRED, ProviderType=REQUIRED, UserPoolId=REQUIRED, AttributeMapping=NOTHING, IdpIdentifiers=NOTHING, ProviderDetails=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ProviderName=ProviderName, 
         ProviderType=ProviderType, 
         UserPoolId=UserPoolId, 
         AttributeMapping=AttributeMapping, 
         IdpIdentifiers=IdpIdentifiers, 
         ProviderDetails=ProviderDetails, **kwargs)
        (super(UserPoolIdentityProvider, self).__init__)(**processed_kwargs)


class ResourceServerScopeType(troposphere.cognito.ResourceServerScopeType, Mixin):

    def __init__(self, title=None, ScopeDescription=REQUIRED, ScopeName=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ScopeDescription=ScopeDescription, 
         ScopeName=ScopeName, **kwargs)
        (super(ResourceServerScopeType, self).__init__)(**processed_kwargs)


class UserPoolResourceServer(troposphere.cognito.UserPoolResourceServer, Mixin):

    def __init__(self, title, template=None, validation=True, Identifier=REQUIRED, Name=REQUIRED, UserPoolId=REQUIRED, Scopes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Identifier=Identifier, 
         Name=Name, 
         UserPoolId=UserPoolId, 
         Scopes=Scopes, **kwargs)
        (super(UserPoolResourceServer, self).__init__)(**processed_kwargs)


class AccountTakeoverActionType(troposphere.cognito.AccountTakeoverActionType, Mixin):

    def __init__(self, title=None, EventAction=REQUIRED, Notify=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EventAction=EventAction, 
         Notify=Notify, **kwargs)
        (super(AccountTakeoverActionType, self).__init__)(**processed_kwargs)


class AccountTakeoverActionsType(troposphere.cognito.AccountTakeoverActionsType, Mixin):

    def __init__(self, title=None, HighAction=NOTHING, LowAction=NOTHING, MediumAction=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HighAction=HighAction, 
         LowAction=LowAction, 
         MediumAction=MediumAction, **kwargs)
        (super(AccountTakeoverActionsType, self).__init__)(**processed_kwargs)


class NotifyEmailType(troposphere.cognito.NotifyEmailType, Mixin):

    def __init__(self, title=None, Subject=REQUIRED, HtmlBody=NOTHING, TextBody=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Subject=Subject, 
         HtmlBody=HtmlBody, 
         TextBody=TextBody, **kwargs)
        (super(NotifyEmailType, self).__init__)(**processed_kwargs)


class NotifyConfigurationType(troposphere.cognito.NotifyConfigurationType, Mixin):

    def __init__(self, title=None, SourceArn=REQUIRED, BlockEmail=NOTHING, From=NOTHING, MfaEmail=NOTHING, NoActionEmail=NOTHING, ReplyTo=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SourceArn=SourceArn, 
         BlockEmail=BlockEmail, 
         From=From, 
         MfaEmail=MfaEmail, 
         NoActionEmail=NoActionEmail, 
         ReplyTo=ReplyTo, **kwargs)
        (super(NotifyConfigurationType, self).__init__)(**processed_kwargs)


class AccountTakeoverRiskConfigurationType(troposphere.cognito.AccountTakeoverRiskConfigurationType, Mixin):

    def __init__(self, title=None, Actions=REQUIRED, NotifyConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Actions=Actions, 
         NotifyConfiguration=NotifyConfiguration, **kwargs)
        (super(AccountTakeoverRiskConfigurationType, self).__init__)(**processed_kwargs)


class CompromisedCredentialsActionsType(troposphere.cognito.CompromisedCredentialsActionsType, Mixin):

    def __init__(self, title=None, EventAction=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EventAction=EventAction, **kwargs)
        (super(CompromisedCredentialsActionsType, self).__init__)(**processed_kwargs)


class CompromisedCredentialsRiskConfigurationType(troposphere.cognito.CompromisedCredentialsRiskConfigurationType, Mixin):

    def __init__(self, title=None, Actions=REQUIRED, EventFilter=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Actions=Actions, 
         EventFilter=EventFilter, **kwargs)
        (super(CompromisedCredentialsRiskConfigurationType, self).__init__)(**processed_kwargs)


class RiskExceptionConfigurationType(troposphere.cognito.RiskExceptionConfigurationType, Mixin):

    def __init__(self, title=None, BlockedIPRangeList=NOTHING, SkippedIPRangeList=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BlockedIPRangeList=BlockedIPRangeList, 
         SkippedIPRangeList=SkippedIPRangeList, **kwargs)
        (super(RiskExceptionConfigurationType, self).__init__)(**processed_kwargs)


class UserPoolRiskConfigurationAttachment(troposphere.cognito.UserPoolRiskConfigurationAttachment, Mixin):

    def __init__(self, title, template=None, validation=True, ClientId=REQUIRED, UserPoolId=REQUIRED, AccountTakeoverRiskConfiguration=NOTHING, CompromisedCredentialsRiskConfiguration=NOTHING, RiskExceptionConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ClientId=ClientId, 
         UserPoolId=UserPoolId, 
         AccountTakeoverRiskConfiguration=AccountTakeoverRiskConfiguration, 
         CompromisedCredentialsRiskConfiguration=CompromisedCredentialsRiskConfiguration, 
         RiskExceptionConfiguration=RiskExceptionConfiguration, **kwargs)
        (super(UserPoolRiskConfigurationAttachment, self).__init__)(**processed_kwargs)


class UserPoolUICustomizationAttachment(troposphere.cognito.UserPoolUICustomizationAttachment, Mixin):

    def __init__(self, title, template=None, validation=True, ClientId=REQUIRED, UserPoolId=REQUIRED, CSS=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ClientId=ClientId, 
         UserPoolId=UserPoolId, 
         CSS=CSS, **kwargs)
        (super(UserPoolUICustomizationAttachment, self).__init__)(**processed_kwargs)


class AttributeType(troposphere.cognito.AttributeType, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Value=Value, **kwargs)
        (super(AttributeType, self).__init__)(**processed_kwargs)


class UserPoolUser(troposphere.cognito.UserPoolUser, Mixin):

    def __init__(self, title, template=None, validation=True, UserPoolId=REQUIRED, ClientMetadata=NOTHING, DesiredDeliveryMediums=NOTHING, ForceAliasCreation=NOTHING, UserAttributes=NOTHING, MessageAction=NOTHING, Username=NOTHING, ValidationData=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         UserPoolId=UserPoolId, 
         ClientMetadata=ClientMetadata, 
         DesiredDeliveryMediums=DesiredDeliveryMediums, 
         ForceAliasCreation=ForceAliasCreation, 
         UserAttributes=UserAttributes, 
         MessageAction=MessageAction, 
         Username=Username, 
         ValidationData=ValidationData, **kwargs)
        (super(UserPoolUser, self).__init__)(**processed_kwargs)


class UserPoolUserToGroupAttachment(troposphere.cognito.UserPoolUserToGroupAttachment, Mixin):

    def __init__(self, title, template=None, validation=True, GroupName=REQUIRED, Username=REQUIRED, UserPoolId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         GroupName=GroupName, 
         Username=Username, 
         UserPoolId=UserPoolId, **kwargs)
        (super(UserPoolUserToGroupAttachment, self).__init__)(**processed_kwargs)